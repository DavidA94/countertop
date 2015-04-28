import wx
from wx.lib.pubsub import pub
import tray

class CGUI(wx.Frame):

    EVENT_OPEN = "OPEN"
    EVENT_SAVE = "SAVE"
    EVENT_EXIT = "EXIT"
    EVENT_TO_TRAY = "TO_TRAY"
    EVENT_FROM_TRAY = "FROM_TRAY"



    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 400),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Misc Data
        self.has_said_at_tray = False


        # GUI Objects
        self.heading = None


        self.tray = tray.TrayIcon(self)

        self.init_ui()
        self.Show()

    def init_ui(self):

        ## Menu ##
        menubar = wx.MenuBar()
        filemenu = wx.Menu()

        open_item = filemenu.Append(wx.ID_OPEN, "&Open Config...\tCtrl + O",
                                    "Open Configuration")
        save_item = filemenu.Append(wx.ID_SAVE, "&Save Config...\tCtrl + S",
                                    "Save Configuration")
        exit_item = filemenu.Append(wx.ID_EXIT, "E&xit\tAlt + F4",
                                    "Exit Application")

        menubar.Append(filemenu, "&File")

        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.SetMenuBar(menubar)


        ## Back Color ##
        self.SetBackgroundColour("White")

        ## Close / Minimize Events ##
        self.Bind(wx.EVT_CLOSE, self.min_to_tray)
        self.Bind(wx.EVT_ICONIZE, self.min_to_tray)


        ## GUI Object ##

        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.heading = wx.StaticText(self, id=-0,
                                     label='Countertop Controller',
                                     pos=(0, 10),
                                     size=(self.GetVirtualSizeTuple()[0], 20),
                                     style=wx.ALIGN_CENTRE)
        self.heading.SetFont(font)

        wx.StaticLine(self, id=2, pos=(40, 40),
                      size=(self.GetVirtualSizeTuple()[0] - 80, 1))

    def on_open(self, e):
        pub.sendMessage(self.EVENT_OPEN)

    def on_save(self, e):
        pub.sendMessage(self.EVENT_SAVE)

    def on_exit(self, e):
        self.tray.RemoveIcon()
        self.tray.Destroy()
        self.Destroy()
        pub.sendMessage(self.EVENT_EXIT)
        self.Close()

    def min_to_tray(self, e):
        self.Hide()
        self.tray.SetIcon(*self.tray.icon_data)
        pub.sendMessage(self.EVENT_TO_TRAY)

    def max_from_tray(self, e):
        self.Restore()
        self.Show()
        self.Raise()
        self.tray.RemoveIcon()
        pub.sendMessage(self.EVENT_FROM_TRAY)


ex = wx.App(False, None, True, True)
CGUI(None, title="Countertop")
ex.MainLoop()
