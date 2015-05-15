import wx
import tray
from wx.lib.pubsub import pub
from bc import ButtonControl


class CGUI(wx.Frame):

    EVENT_LOAD = "LOAD"
    EVENT_SAVE = "SAVE"
    EVENT_EXIT = "EXIT"
    EVENT_TO_TRAY = "TO_TRAY"
    EVENT_FROM_TRAY = "FROM_TRAY"
    SYSTEM_NAME = "Countertop Controller"



    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 400),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Set the icon
        self.SetIcon(wx.Icon('graphics/controller_icon.ico',
                             wx.BITMAP_TYPE_ICO))

        # Misc Data
        self.has_said_at_tray = False
        self.bkk_ctrl = None
        self.bcb_ctrl = None


        # GUI Objects
        self.heading = None

        # Tray icon
        self.tray = tray.TrayIcon(self)

        # Keyboard and Controller key icons
        self.bkk = wx.Image('graphics/BKK.png', wx.BITMAP_TYPE_ANY)
        self.bcb = wx.Image('graphics/BCB.png', wx.BITMAP_TYPE_ANY)

        # Create the fonts for the keyboard key and controller button
        self.kk_font = wx.Font(pointSize=36, family=wx.FONTFAMILY_DEFAULT,
                               style=wx.FONTSTYLE_NORMAL,
                               weight=wx.FONTWEIGHT_NORMAL,
                               underline=False, face="Arial",
                               encoding=wx.FONTENCODING_DEFAULT)

        self.cb_font = wx.Font(pointSize=28, family=wx.FONTFAMILY_DEFAULT,
                               style=wx.FONTSTYLE_NORMAL,
                               weight=wx.FONTWEIGHT_NORMAL,
                               underline=False, face="Arial",
                               encoding=wx.FONTENCODING_DEFAULT)

        self.init_ui()
        self.Show()

    def init_ui(self):

        ## Menu ##
        menubar = wx.MenuBar()
        filemenu = wx.Menu()

        load_item = filemenu.Append(wx.ID_OPEN, "&Load Config...\tCtrl + L",
                                    "Load Configuration")
        exit_item = filemenu.Append(wx.ID_EXIT, "E&xit\tAlt + F4",
                                    "Exit Application")

        menubar.Append(filemenu, "&File")

        self.Bind(wx.EVT_MENU, self.on_load, load_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.SetMenuBar(menubar)

        ## Back Color ##
        self.SetBackgroundColour("White")

        ## Close / Minimize Events ##
        self.Bind(wx.EVT_CLOSE, self.min_to_tray)
        self.Bind(wx.EVT_ICONIZE, self.min_to_tray)


        ## GUI Object ##
        # Get a font
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        # Put the top heading
        self.heading = wx.StaticText(self, id=-0,
                                     label=self.SYSTEM_NAME,
                                     pos=(0, 10),
                                     size=(self.GetVirtualSizeTuple()[0], 20),
                                     style=wx.ALIGN_CENTRE)
        # Set that heading's font
        self.heading.SetFont(font)

        # Line below the heading
        wx.StaticLine(self, id=2, pos=(40, 40),
                      size=(self.GetVirtualSizeTuple()[0] - 80, 1))


        wx.StaticBitmap(self, -1, self.bkk.ConvertToBitmap(), (60, 60), (72, 72))
        # Blank keyboard key
        self.bkk_ctrl = ButtonControl(parent=self, img=self.bkk,
                                      font=self.kk_font, id=3,
                                      pos=(60, 60)
        )


        self.bcb_ctrl = ButtonControl(parent=self, img=self.bcb,
                                      font=self.cb_font, color=(255,255,255),
                                      id=3, pos=(400 - 60 - 72, 60)
        )

        self.bkk_ctrl.make_visible()
        self.bcb_ctrl.make_visible()

    def on_load(self, e):
        self.bkk_ctrl.set_char("A")
        self.bcb_ctrl.set_char("0")
        pub.sendMessage(self.EVENT_LOAD)

    def on_exit(self, e):
        self.tray.RemoveIcon()
        self.tray.Destroy()
        self.Destroy()
        pub.sendMessage(self.EVENT_EXIT)
        self.Close()
        raise Exception("Remove self.Close() from GUI.")

    def min_to_tray(self, e):
        self.Hide()
        self.tray.SetIcon(*self.tray.icon_data)
        if(self.has_said_at_tray is False):
            self.tray.ShowBalloon(title=self.SYSTEM_NAME + " is still open.\n",
                                  text="You can restore " + self.SYSTEM_NAME +
                                       " by double clicking the icon.")
            self.has_said_at_tray = True
        pub.sendMessage(self.EVENT_TO_TRAY)

    def max_from_tray(self, e):
        self.Restore()
        self.Show()
        self.Raise()
        self.tray.RemoveIcon()
        pub.sendMessage(self.EVENT_FROM_TRAY)


ex = wx.App(False, None, True, True)
CGUI(None, title=CGUI.SYSTEM_NAME)
ex.MainLoop()
