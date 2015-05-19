import wx
import wx.animate
import tray
from wx.lib.pubsub import pub
from bc import ButtonControl
import threading


class CGUI(wx.Frame):

    EVENT_LOAD = "LOAD"
    EVENT_EXIT = "EXIT"
    EVENT_TO_TRAY = "TO_TRAY"
    EVENT_FROM_TRAY = "FROM_TRAY"
    GET_DEVICES = "GET_DEVICES"

    SYSTEM_NAME = "Countertop Controller"
    KBD_WAIT = "Waiting for keyboard key press . . ."
    CRL_WAIT = "Waiting for controller button press . . ."
    SUC_MAP = "Mapping Successful"

    def __init__(self, parent, title):
        """
        Create a CGUI Object
        :param parent: The parent of the gui
        :param title: The title of the GUI
        """

        # Set up the parent Frame as a window that can't be re-sized.
        wx.Frame.__init__(self, parent, title=title, size=(400, 225),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Set the icon
        self.SetIcon(wx.Icon('graphics/controller_icon.ico',
                             wx.BITMAP_TYPE_ICO))

        # Misc Data
        self.has_said_at_tray = False  # Only show the "still open" msg once
        self.bkk_ctrl = None  # Initialized in init_gui
        self.bcb_ctrl = None  # Initialized in init_gui
        self.instr = None  # Initialized in init_gui
        self.heading = None  # Initialized in init_gui
        self.gif = None  # Used to show that a mapping has been successful

        # Create the tray version
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

        # Initialize the UI
        self.init_ui()
        # Show the UI
        self.Show()

    def init_ui(self):
        """
        Initializes a CGUI with the proper elements
        """

        # Create the menu
        menubar = wx.MenuBar()  # The menu bar
        filemenu = wx.Menu()  # The file menu in the menu bar

        # The fil menu has two options, load and exit
        load_item = filemenu.Append(wx.ID_OPEN, "&Load Config...\tCtrl + L",
                                    "Load Configuration")
        slct_item = filemenu.Append(wx.ID_SETUP, "&Select Device...\tCtrl + D",
                                    "Select Device")
        exit_item = filemenu.Append(wx.ID_EXIT, "E&xit\tAlt + F4",
                                    "Exit Application")

        # Add the file menu to the menu bar
        menubar.Append(filemenu, "&File")

        # Bind events for when the menu options are clicked.
        self.Bind(wx.EVT_MENU, self.on_load, load_item)
        self.Bind(wx.EVT_MENU, self.on_slct, slct_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        # Add keyboard shortcuts
        shortcut_table = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('L'),
                                               load_item.GetId()),  # Ctrl + L
                                              (wx.ACCEL_CTRL, ord('D'),
                                               slct_item.GetId()),  # Ctrl + D
                                              (wx.ACCEL_ALT, wx.WXK_F4,
                                               exit_item.GetId())])  # Alt + F4
        self.SetAcceleratorTable(shortcut_table)

        # Set the menu bar for the window
        self.SetMenuBar(menubar)

        # Back Color
        self.SetBackgroundColour("White")

        # Close / Minimize Events (They just make it minimize to the tray)
        self.Bind(wx.EVT_CLOSE, self.min_to_tray)
        self.Bind(wx.EVT_ICONIZE, self.min_to_tray)

        # --- GUI Objects --- #
        # Place the top heading
        self.heading = wx.StaticText(self, id=0,
                                     label=self.SYSTEM_NAME,
                                     pos=(0, 10),
                                     size=(self.GetVirtualSizeTuple()[0], 20),
                                     style=wx.ALIGN_CENTRE)
        # Set that heading's font
        self.heading.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        # Line below the heading
        wx.StaticLine(self, id=2, pos=(40, 40),
                      size=(self.GetVirtualSizeTuple()[0] - 80, 1))

        # Initialize the blank controller button
        self.bcb_ctrl = ButtonControl(parent=self, img=self.bcb,
                                      font=self.cb_font, color=(255, 255, 255),
                                      id=3, pos=(60, 60)
        )

        # Initialize the blank keyboard key
        self.bkk_ctrl = ButtonControl(parent=self, img=self.bkk,
                                      font=self.kk_font, id=3,
                                      pos=(400 - 60 - 72, 60)
        )

        # Initialize the instruction label
        self.instr = wx.StaticText(self, id=0, label="", pos=(0, 150),
                                   size=(self.GetVirtualSizeTuple()[0], 20),
                                   style=wx.ALIGN_CENTRE)
        # Set the font for the instruction label
        self.instr.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    def on_load(self, e):
        pub.sendMessage(self.EVENT_LOAD)

    def on_slct(self, e):
        dlg = wx.SingleChoiceDialog(parent=self, message="Select a Device",
                                    caption="Select a Device",
                                    choices=("1", "2", "3"))

        dlg.ShowModal()
        pub.sendMessage(self.GET_DEVICES)

    def on_exit(self, e):
        self.tray.RemoveIcon()
        self.tray.Destroy()
        self.Destroy()
        pub.sendMessage(self.EVENT_EXIT)
        self.Close()
        raise Exception("Remove self.Close() from GUI.")

    def min_to_tray(self, e):
        """
        Minimizes the window to the system tray

        :param e: Event - Unused
        """

        # Hide the main GUI
        self.Hide()

        # Set the tray icon from it's data.
        self.tray.SetIcon(*self.tray.icon_data)

        # If we haven't put the "Still open" message before, do so
        if self.has_said_at_tray is False:
            # Show a balloon with the message
            self.tray.ShowBalloon(title=self.SYSTEM_NAME + " is still open.\n",
                                  text="You can restore " + self.SYSTEM_NAME +
                                       " by double clicking the icon.")
            # And don't show it again.
            self.has_said_at_tray = True

        # Send an event saying that we've been minimized.
        pub.sendMessage(self.EVENT_TO_TRAY)

    def max_from_tray(self, e):
        """
        Return the GUI from the system tray.
        :param e: Event - unused.
        """

        self.Restore()  # Restore the main GUI
        self.Show()  # Show the main GUI
        self.Raise()  # Raise the main GUI (Just in case)
        self.tray.RemoveIcon()  # Remove the tray icon

        # Send an event saying we've come back from the tray.
        pub.sendMessage(self.EVENT_FROM_TRAY)

    def show_kbd_key(self, char=""):
        """
        Shows the keyboard key, and displays a waiting message if no char
        is supplied.

        :param char: The character to be displayed on top of they key
        """

        # If no char was supplied
        if char == "":
            # Then set the instruction label to be the waiting message.
            self.instr.SetLabel(self.KBD_WAIT)

        # Make the key visible
        self.bkk_ctrl.make_visible(char)

    def hide_kbd_key(self):
        """ Hides the keyboard key. """
        self.bkk_ctrl.make_hidden()
        self.instr.SetLabel("")

    def show_crl_key(self, char=""):
        """
        Shows the controller button, and displays a waiting message if no char
        is supplied.

        :param char: The character to be displayed on top of they button
        """

        # If no char was supplied
        if char == "":
            # Then set the instruction label to be the waiting message.
            self.instr.SetLabel(self.CRL_WAIT)

        # Make the button visible
        self.bcb_ctrl.make_visible(char)

    def hide_crl_key(self):
        """ Hides the controller button. """
        self.bcb_ctrl.make_hidden()
        self.instr.SetLabel("")

    def show_tick(self):
        """
        Shows an animated check mark and displays a message saying that the
        mapping has been successful.
        :return:
        """
        # Set the label to say successful
        self.instr.SetLabel(self.SUC_MAP)

        # Create the animation control
        self.gif = wx.animate.AnimationCtrl(self, pos=(175, 55))
        # Load the tick file
        self.gif.LoadFile('graphics/animated_tick.gif')
        # Get the last frame of the animation
        inactive = self.gif.GetAnimation().GetFrame(29).ConvertToBitmap()
        # Set the inactive to be the last frame
        self.gif.SetInactiveBitmap(inactive)
        # Play the animation
        self.gif.Play()
        # After two seconds stop it (so it never repeats)
        threading.Timer(2, self.gif.Stop).start()

    def hide_tick(self):
        """ Hides the check mark. """
        self.gif.Destroy()

    #def select_device

ex = wx.App(False, None, True, True)
CGUI(None, title=CGUI.SYSTEM_NAME)
ex.MainLoop()


