__author__ = 'johnhar1'

from time import sleep
from msvcrt import kbhit
import pywinusb.hid as hid
import SendKeys
from source.data_objects.cl import *

class Controller(object):
    #
    def __init__(self):
        self.LKP = None
        self.poll = False
        self.cl = ControllerLinks()
        self.device = None
        self.devices = hid.find_all_hid_devices()

    #Get the list and return it so a device can be selected
    def get_devices(self):
        self.devices = hid.find_all_hid_devices()
        return self.devices

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

    def hid_handler(self, data):
        #if self.
        #print("Raw data: {0}".format(data))
        pass

    #Save and load config TBA
    def save_config(self):
        pass

    def load_config(self,config):
        pass



