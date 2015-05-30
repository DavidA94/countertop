__author__ = 'johnhar1'

from unittest import TestCase
from source.logic.controller import Controller

class ControllerTest(TestCase):
    def __init__(self, *args, **kwargs):
        self.cont = Controller(None)
        self.data = [1, 128, 127, 127, 128, 72, 0, 0]

    def setUp(self):
        self.c = Controller(None)

    def tearDown(self):
        self.c.StopThread.set()

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

    def test_make_link(self):
        self.c.data_to_make_link = self.data
        self.c.make_link('a')
        self.assertIn(self.data,self.c.cl.links.keys())
        self.assertEqual(self.c.cl.links[self.data].key,'b')


    def test_save_config(self):
        pass

    def test_load_config(self):
        pass

    def test_gen_key_events(self):
        pass

    def test_get_delta(self):
        pass

    def test_get_bnt_press(self):
        pass




