__author__ = 'johnhar1'
"""
Controller class, this handles receiving and generating events
"""

from time import sleep
from msvcrt import kbhit
import pywinusb.hid as hid
import SendKeys
import thread
import threading
import time
from source.data_objects.cl import *


class Controller(object):

    def __init__(self, button_pressed_func, device_unplugged):
        """
        Init Function
        :param button_pressed_func: function that will be called after get_btn_press is called
        :return:
        """
        self.cl = ControllerLinks()
        self.wait_for_button = False
        self.poll = False
        self.last_USB = None
        self.data_to_make_link = None

        # Hid device stuff
        self.devices = hid.find_all_hid_devices()
        self.device = None

        #return func to notify UI that a key has been captured
        self.BPF = button_pressed_func

        # Called if the device is unplugged
        self.device_unplugged = device_unplugged

        #launch thread to generate keys
        self.GenerateThread = threading.Thread(target=self.generate_key_events,name="Bob")
        self.StopThread = threading.Event()
        self.GenerateThread.start()

    #Get the list and return it so a device can be selected
    def get_devices(self):
        """
        Called to get the usb devices on the machine
        :return: List of the HIDDevices
        """
        self.devices = hid.find_all_hid_devices()
        device_names = []
        for device in self.devices:
            device_names.append(device.product_name)
        return tuple(device_names)

    #event to be called whena device is chosen to be the usb device
    def set_device(self,device_id = None):
        """
        Sets the device to the given index
        :param device_id:
        :return: False if incorrect param
        """
        if not isinstance(device_id,int):
            return False
        self.device = self.devices[device_id]
        try:
            self.device.open()
            self.device.set_raw_data_handler(self.hid_handler)

        except hid.core.HIDError():
            pass

    # method called by
    def hid_handler(self, data):
        """
        Method that handles HID Device events
        :param data: List of data
        :return: N/a
        """
        #Collect a key
        if not self.poll and self.wait_for_button:
            self.wait_for_button = False
            self.data_to_make_link = data
            self.BPF()
        elif self.poll:
            result = self.get_delta(data,self.last_USB)
            button = result[0]
            if button in self.cl.links.keys():
                self.cl.links[button].is_pressed = result[1]#This is the state of the button
        self.last_USB = data

    def get_delta(self,current,last):
        """
        Calculates the key that was pressed, and its state
        :param current: current USB data
        :param last: Last USB data
        :return: tuple containing the button pressed, and the state (button,state)
        """
        pressed = False
        ret = []
        if current is not None and last is not None:
            if(len(current) == len(last)):
                for ndx in xrange(0,len(current)):
                    dif = current[ndx] - last[ndx]
                    if dif == 0:
                        ret.append(current[ndx])
                    else:
                        pressed = True if dif < 0 else False
                        ret.append(abs(dif))
            return tuple(ret), pressed
        else:# something was None, so we will just return current
            return tuple(current), pressed

    def make_link(self,key):
        """
        Makes a connection link
        :param key: character or string to be made into a link
        :return: N/A
        """
        self.cl.add_link(tuple(self.data_to_make_link), Key(key))

    def get_btn_press(self):
        """
        Call to get make the next button press be saved and call self.BPF (Button press function)
        :return:
        """
        self.wait_for_button = True
        self.data_to_make_link = None

    def generate_key_events(self):
        """
        Thread run method that generates key events based on current state of the keys (Do not Call)
        :return: N/A
        """
        while not self.StopThread.isSet():
            if self.device is not None and not self.device.is_plugged():
                self.device_unplugged()
                break
            if self.poll:
                #iterate the list and generate any keys that are down
                for zelda in self.cl.links.values():
                    if zelda.is_pressed:
                        SendKeys.SendKeys(zelda.key)
                time.sleep(.1)#maybe change this?
            else:
                time.sleep(2)

