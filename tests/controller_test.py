__author__ = 'johnhar1'

from unittest import TestCase
from source.logic.controller import Controller
import pywinusb.hid as hid
import mock

class Data:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ControllerTest(TestCase):
    def setUp(self):
        self.c = Controller(None)

    def tearDown(self):

    def test_get_devices(self):
        temp1 = hid.find_all_hid_devices

        hid.find_all_hid_devices = mock.Mock(return_value=Data(product_name="ABC"))
        self.assertEqual(self.c.get_devices(), ("ABC",))

    #Test whether or not a button can be pressed and a keyevent raised
    def test_press_button(self):
        pass

    def test_set_device(self):
        pass

    def test_hid_handler(self):
        pass

    def test_make_link(self):
        pass

    def test_save_config(self):
        pass

    def test_load_config(self):
        pass

    def test_gen_key_events(self):
        pass


