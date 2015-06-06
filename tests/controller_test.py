__author__ = 'johnhar1'

from unittest import TestCase
from source.logic.controller import Controller
import pywinusb.hid as hid
import mock
import threading
import time
from source.data_objects.cl import Key, ControllerLinks


def useless():
    pass


class Data:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ControllerTest(TestCase):
    def setUp(self):
        self.c = Controller(Data)
        self.data = [1, 128, 127, 127, 128, 72, 0, 0]

    def tearDown(self):
        self.c.StopThread.set()


    def test_get_devices(self):
        temp = hid.find_all_hid_devices

        hid.find_all_hid_devices = mock.Mock(return_value=[Data(product_name="ABC")])
        self.assertEqual(self.c.get_devices(), ("ABC",))

        hid.find_all_hid_devices = temp


    def test_set_device_fail(self):
        self.assertFalse(self.c.set_device("A"))

    def test_set_device_fail_open(self):
        self.c.devices = [hid.core.HidDevice(None), hid.core.HidDevice(None)]

        with self.assertRaises(hid.core.HIDError) as e:
            self.c.set_device(1)

        self.assertEqual(e.exception.message, "Failure to get HID pre parsed data")

    def test_set_device_pass(self):
        dev0 = hid.core.HidDevice(None)
        dev1 = hid.core.HidDevice(None)
        self.c.devices = [dev0, dev1]
        dev1.open = mock.Mock()

        self.c.set_device(1)

        self.assertEqual(self.c.device, dev1)


    #Test whether or not a button can be pressed and a keyevent raised
    def test_press_button(self):
        pass

    def test_set_device(self):
        pass

    def test_hid_handler(self):
        self.c.poll = False #set the device to not poll
        self.c.data_to_make_link = None
        self.c.hid_handler(self.data) #call with data

        self.assertEqual(self.c.data_to_make_link,None)
        self.assertEqual(self.c.last_USB,self.data)

        self.c.get_btn_press()
        self.assertTrue(self.c.wait_for_button)

        self.c.hid_handler(self.data)
        self.assertFalse(self.c.wait_for_button)
        self.assertEqual(self.c.data_to_make_link,self.data)

        self.c.poll = True
        self.c.cl.add_link(tuple(self.data),Key('c'))
        self.c.hid_handler(self.data)


    def test_make_link(self):
        self.c.data_to_make_link = self.data
        self.c.make_link('a')
        self.assertIn(tuple(self.data),self.c.cl.links.keys())
        self.assertEqual(self.c.cl.links[tuple(self.data)].key,'a')

    def test_gen_key_events(self):
        testThread = threading.Thread(target=self.c.generate_key_events)
        testThread.start()
        #Do some test here....not really
        ispressedkey = Key('a')
        ispressedkey.is_pressed = True
        self.c.cl.add_link(tuple([123,123,123]),ispressedkey)
        self.c.cl.add_link(tuple([123,143,123]),Key('c'))
        self.c.cl.add_link(tuple([123,123,112]),Key('b'))

        self.c.poll = False
        time.sleep(.1)
        self.c.poll = True
        time.sleep(5)#need to wait for it to start...
        self.c.StopThread.set()


    def test_get_delta(self):
        data1 = [1, 128, 127, 127, 128, 72, 0, 0]
        data2 = [1, 128, 127, 127, 128, 8, 0, 0]

        #test default
        delta = self.c.get_delta(data1,data2)
        self.assertEqual(delta[0],tuple([1, 128, 127, 127, 128, 64, 0, 0]))
        self.assertFalse(delta[1])

        #test that state changes to pressed if delta is positive
        delta = self.c.get_delta(data2,data1)
        self.assertTrue(delta[1])

        #test start case where no other data point is available
        delta = self.c.get_delta(data1,None)
        self.assertEqual(delta[0],tuple(data1))


    def test_get_bnt_press(self):
        self.c.data_to_make_link = 5
        self.c.wait_for_button = False
        self.c.get_btn_press()
        self.assertTrue(self.c.wait_for_button)
        self.assertIsNone(self.c.data_to_make_link)
