from source.data_objects.cl import Key
from unittest import TestCase

class TestKeyObject(TestCase):

    def test_key_data(self):
        k = Key('a')
        self.assertEqual(k.key, "a")

    def test_key_state_false(self):
        k = Key('b')
        self.assertFalse(k.is_pressed)

    def test_key_state_true(self):
        k = Key('c', True)
        self.assertTrue(k.is_pressed)

    def test_key_state_changed(self):
        k = Key('d')
        self.assertFalse(k.is_pressed)
        k.is_pressed = True
        self.assertTrue(k.is_pressed)
