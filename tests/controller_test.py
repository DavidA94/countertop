__author__ = 'johnhar1'

from unittest import TestCase
from source.logic.controller import Controller

class ControllerTest(TestCase):
    def __init__(self):
        self.cont = Controller()

    def setUp(self):
        self.c = Controller()

    def tearDown(self):
        self.c.StopThread.set()

    #Test whether or not a button can be pressed and a keyevent raised
    def test_press_button(self):


    def test_set_device(self):
        pass

    def test_hid_handler(self):
        self.c.poll = False #set the device to not poll
        self.

    def test_make_link(self):
        data = [1, 128, 127, 127, 128, 72, 0, 0]
        self.c.data_to_make_link = data
        self.c.make_link('a')
        self.assertIn(data,self.c.cl.links.keys())
        self.assertEqual(self.c.cl.links[data].key,'a')

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




