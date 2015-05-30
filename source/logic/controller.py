__author__ = 'johnhar1'

from time import sleep
from msvcrt import kbhit
import pywinusb.hid as hid
import SendKeys
import threading
import time
from source.data_objects.cl import *


class Controller(object):
    def __init__(self, button_pressed_func):
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

        #launch thread to generate keys
        self.StopThread = threading.Event()
        self.GenerateThread = threading.Thread(target=self.generate_key_events)
        #self.GenerateThread.start()


    #Get the list and return it so a device can be selected
    def get_devices(self):
        self.devices = hid.find_all_hid_devices()
        device_names = []
        for device in self.devices:
            device_names.append(device.product_name)
        return tuple(device_names)

    #event to be called whena device is chosen to be the usb device
    def set_device(self,device_id = None):
        if not isinstance(device_id,int):
            return
        self.device = self.devices[device_id]
        try:
            self.device.open()
            self.device.set_raw_data_handler(self.hid_handler)

        except hid.core.HIDError():
            self.device.close()

    # method called by
    def hid_handler(self, data):
        #Collect a key
        if not self.poll and self.wait_for_button:
            self.wait_for_button = False
            self.data_to_make_link = data
            self.BPF()
        elif self.poll:
            button = self.get_delta(data,self.last_USB)
            if button in self.cl.links.keys():
                self.cl.links[button].state_change()#change the state of the button

        self.last_USB = data

    def get_delta(self,current,last):
        ret = []
        if current is not None and last is not None:
            if(len(current) == len(last)):
                for ndx in xrange(0,len(current)):
                    dif = current[ndx] - last[ndx]
                    if dif == 0:
                        ret.append(current[ndx])
                    else:
                        ret.append(abs(dif))
            return tuple(ret)
        else:# something was None, so we will just return current
            return current

    def make_link(self,key):
        self.cl.add_link(tuple(self.data_to_make_link),Key(key))

    def get_btn_press(self):
        self.wait_for_button = True
        self.data_to_make_link = None

    def generate_key_events(self):
        while not self.StopThread.isSet():
            if self.poll:
                #iterate the list and generate any keys that are down
                for zelda in self.cl.links.values():
                    if zelda.is_pressed:
                        SendKeys.SendKeys(zelda.key)
                time.sleep(.1)#maybe change this?
            else:
                time.sleep(2)

    #Save and load config TBA
    def save_config(self):
        pass

    def load_config(self):
        pass

