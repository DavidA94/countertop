"""
Holds information about a controller button, and what key it is linked to
"""


"""
Holds the dictionary of created links
"""
class ControllerLinks(object):
    """
    Controller Links class
    """
    def __init__(self):
        """
        Init function
        """

        self.links = {}

    def add_link(self, data, key):
        '''
        Adds a link to the dictionary
        :param data: data to be linked
        :param key: Key class object
        :return: N/A
        '''
        if type(data) is not tuple:
            raise AttributeError("Parameter data must be a tuple")
        elif type(key) is not Key:
            raise AttributeError("Parameter key must be of type Key")
        else:
            self.links[data] = key

    def rem_link(self, data):
        """
        Removes a link
        :param data: Data to be removed
        :return: The link that was popped, otherwise None
        """

        if data in self.links:
            return self.links.pop(data)
        else:
            return None

    def get_links(self):
        """
        Gets the links
        :return: The dictionary of links
        """
        return self.links
                            

"""
Holds information about a key, and it's pressed status
"""
class Key(object):
    """
    Key class, this wraps a string or char
    """
    def __init__(self, key, is_pressed=False, friendly=None):
        """
        Init function
        :param key: String/Char to be mapped
        :param is_pressed: State of the button
        :param friendly: Name for it, (FUTURE USE)
        """
        self.key = key
        self.is_pressed = is_pressed
        self.friendly_name = friendly

    def state_change(self):
        """
        Method that can be called to flip the state of the key
        """
        self.is_pressed = not self.is_pressed
