from source.data_objects.cl import ControllerLinks, Key
from unittest import TestCase

class TestLinksObject(TestCase):

    def test_init(self):
        cl = ControllerLinks()
        self.assertEqual(cl.links, {})

    def test_add_link_good_data_key(self):
        cl = ControllerLinks()
        data = (0, 127, 127, 127, 127, 8, 0)
        key = Key("A")
        cl.add_link(data, key)
        self.assertEqual(cl.links[data], key)

    def test_add_link_bad_data(self):
        cl = ControllerLinks()
        data = [0, 127, 127, 127, 127, 8, 0]
        key = Key("A")

        with self.assertRaises(AttributeError) as ae:
            cl.add_link(data, key)    
        
        self.assertEqual(ae.exception.message, "Parameter data must be a tuple")

    def test_add_link_bad_key(self):
        cl = ControllerLinks()
        data = (0, 127, 127, 127, 127, 8, 0)
        key = "A"

        with self.assertRaises(AttributeError) as ae:
            cl.add_link(data, key)    
        
        self.assertEqual(ae.exception.message,
                         "Parameter key must be of type Key")

    def test_rem_link_in_links(self):
        cl = ControllerLinks()
        data = (0, 127, 127, 127, 127, 8, 0)
        key = Key("A")
        cl.add_link(data, key)

        response = cl.rem_link(data)

        self.assertEqual(response, key)

        
    def test_rem_link_not_in_links(self):
        cl = ControllerLinks()

        data = (0, 127, 127, 127, 127, 8, 0)
        response = cl.rem_link(data)
        self.assertEqual(response, None)

    def test_get_links(self):
        cl = ControllerLinks()
        data = (0, 127, 127, 127, 127, 8, 0)
        key = Key("A")
        cl.add_link(data, key)

        response = cl.get_links()

        self.assertEqual(response, {data: key})
