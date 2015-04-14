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

    def test_key_friendly_name_not_set(self):
        k = Key('d')
        self.assertEqual(k.friendly_name, None)

    def test_key_friendly_name(self):
        k = Key('d', friendly="BackLeftButton")
        self.assertEqual(k.friendly_name, "BackLeftButton")
