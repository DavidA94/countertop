"""
Holds information about a controller button, and what key it is linked to
"""


"""
Holds the dictionary of created links
"""
class ControllerLinks(object):
    
    def __init__(self):
        self.links = {}

    def add_link(self, data, key):
        if type(data) is not tuple:
            raise AttributeError("Parameter data must be a tuple")
        elif type(key) is not Key:
            raise AttributeError("Parameter key must be of type Key")
        else:
            self.links[data] = key

    def rem_link(self, data):
        if data in self.links:
            return self.links.pop(data)
        else:
            return None

    def get_links(self):
        return self.links
                            

"""
Holds information about a key, and it's pressed status
"""
class Key(object):
    def __init__(self, key, is_pressed = False):
        self.key = key
        self.is_pressed = is_pressed
