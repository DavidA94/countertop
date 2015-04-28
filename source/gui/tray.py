import wx


class TrayIcon(wx.TaskBarIcon):

    def __init__(self, frame):

        # Not sure why this is needed, but it is.
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        # Initialized the base class
        wx.TaskBarIcon.__init__(self)

        # Remember which window was the opened one
        self.frame = frame

        self.icon_data = (wx.Icon('graphics/controller_icon.ico',
                                  wx.BITMAP_TYPE_ICO), "Countertop Controller")

        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.show_right_click_menu)

        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.restore_main_window)



    def show_right_click_menu(self, e):
        self.PopupMenu(self.make_menu())

    def make_menu(self):
        # Create a menu
        menu = wx.Menu()

        # Create the "Open" menu item. We do it this weird way so the
        # font can be set as bold.
        menu_open = wx.MenuItem(menu, wx.ID_OPEN, "Open")
        font = menu_open.GetFont()
        font.SetWeight(wx.BOLD)
        menu_open.SetFont(font)

        # Add the "Open" and "Exit" options to the menu
        menu_open = menu.AppendItem(menu_open)
        menu_exit = menu.Append(wx.ID_EXIT, "Exit")

        # Take care of the events when the buttons are clicked.
        self.Bind(wx.EVT_MENU, self.restore_main_window, menu_open)
        self.Bind(wx.EVT_MENU, self.frame.on_exit, menu_exit)

        return menu

    def restore_main_window(self, e):
        self.frame.max_from_tray(e)
