import wx
import wx.animate
import tray
from bc import ButtonControl
from source.logic.controller import Controller
from source.logic.vk2sk import Vk2Sk
import threading

class CGUI(wx.Frame):

    # region Constants

    SYSTEM_NAME = "Countertop Controller"
    KBD_WAIT = "Waiting for keyboard key press . . ."
    CRL_WAIT = "Waiting for controller button press . . ."
    SUC_MAP = "Mapping Successful"

    # endregion

    # region Constructor

    def __init__(self, parent, title):
        """
        Create a CGUI Object
        :param parent: The parent of the gui
        :param title: The title of the GUI
        """

        # region Window Setup & Tray Setup

        # Set up the parent Frame as a window that can't be re-sized.
        wx.Frame.__init__(self, parent, title=title, size=(400, 225),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER |
                                wx.WANTS_CHARS)

        # Set the icon
        self.SetIcon(wx.Icon('graphics/controller_icon.ico',
                             wx.BITMAP_TYPE_ICO))

        # Back Color
        self.SetBackgroundColour("White")

        # Create the tray version
        self.tray = tray.TrayIcon(self)

        # endregion

        # region Data member variables

        # Data Setup
        self.controller = Controller(self.crl_btn_pressed, self.device_unplugged)  # The controller
        self.device_selected = False
        self.has_said_at_tray = False  # Only show the "still open" msg once
        self.waiting_for_crl_btn = True  # Waiting for a controller button?
        self.waiting_for_kbd_key = False  # Waiting for a keyboard key?

        # endregion

        # region GUI member initialized in init_gui

        # GUI stuff
        self.bkk_ctrl = None  # Initialized in init_gui
        self.bcb_ctrl = None  # Initialized in init_gui
        self.instr = None  # Initialized in init_gui
        self.heading = None  # Initialized in init_gui
        self.select_dev_btn = None  # Initialized in init_gui
        self.gif = None  # Used to show that a mapping has been successful
        # self.key_capture = None  # Used to capture key strokes

        # endregion

        # region Keyboard and Controller graphics and fonts

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

        # endregion

        # region Keyboard Shortcuts

        # self.shortcuts = None

        # endregion

        # Initialize the UI
        self.init_ui()

        # Show the UI
        self.Show()

    # endregion

    # region GUI Initialization

    def init_ui(self):
        """ Initializes a CGUI with the proper elements """

        # region Menu Setup
        #
        # # Create the menu
        #
        # menu_bar = wx.MenuBar()  # The menu bar
        # file_menu = wx.Menu()  # The file menu in the menu bar
        #
        # # The file menu has Load, Select, and Exit
        # load_item = file_menu.Append(wx.ID_OPEN, "&Load Config...\tCtrl + L",
        #                              "Load Configuration")
        # select_item = file_menu.Append(wx.ID_SETUP,
        #                                "&Select Device...\tCtrl + D",
        #                                "Select Device")
        # exit_item = file_menu.Append(wx.ID_EXIT, "E&xit\tAlt + F4",
        #                              "Exit Application")
        #
        # # Add the file menu to the menu bar
        # menu_bar.Append(file_menu, "&File")
        #
        # # Set the menu bar for the window
        # self.SetMenuBar(menu_bar)
        #
        # region Menu Bindings
        #
        # # Bind events for when the menu options are clicked.
        # self.Bind(wx.EVT_MENU, self.on_load, load_item)
        # self.Bind(wx.EVT_MENU, self.on_select, select_item)
        # self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        #
        # # endregion
        #
        # # endregion

        # region Keyboard Shortcuts / AcceleratorTable
        #
        # self.shortcuts = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('L'),
        #                                        load_item.GetId()),  # Ctrl + L
        #                                       (wx.ACCEL_CTRL, ord('D'),
        #                                        select_item.GetId()),  # Ctrl+D
        #                                       (wx.ACCEL_ALT, wx.WXK_F4,
        #                                        exit_item.GetId())])  # Alt + F4
        #
        # # Add keyboard shortcuts
        # self.SetAcceleratorTable(self.shortcuts)
        #
        # # endregion

        # region Always Present GUI Objects

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

        # Hidden text box for getting key strokes
        # self.key_capture = wx.TextCtrl(parent=self, pos=(0,-000))

        # endregion

        # region Dynamic GUI Objects

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

        # region Select Device Button

        # Create the Select Device button
        self.select_dev_btn = wx.Button(parent=self, id=4,
                                        label="&Select Device", pos=(0, 0))

        # Get the size of the window and the size of the button
        win_size = self.GetVirtualSizeTuple()
        btn_size = self.select_dev_btn.GetSize()

        # Reposition the button to be in the middle(ish)
        self.select_dev_btn.SetPosition((win_size[0] / 2 - btn_size[0] / 2,
                                         win_size[1] / 2 - 5))

        # endregion

        # endregion

        # region Event Bindings

        # Close / Minimize Events (They just make it minimize to the tray)
        self.Bind(wx.EVT_CLOSE, self.min_to_tray)

        # Capture keystrokes
        self.Bind(wx.EVT_KEY_UP, self.key_up)

        # Bind an event to the Select Device button shown at startup
        self.Bind(wx.EVT_BUTTON, self.on_select, self.select_dev_btn)
        # endregion

    # endregion

    # region Bound Events

    def on_load(self, e):
        """ Loads the last configuration """

        # Try to load the configuration
        try:
            # Load it
            self.controller.load_config()

            # And if we make it this far, then we can tell them it loaded.
            wx.MessageBox("Last configuration successfully loaded.",
                          "Config Loaded", wx.OK | wx.ICON_INFORMATION)

        # If something goes wrong
        except Exception as e:
            # Tell the user what
            wx.MessageBox(e.message, "Error", wx.OK | wx.ICON_EXCLAMATION)

    def on_select(self, e):
        """
        Allows the user to select a device

        :param e: event - Not used
        """

        # Create a single choice dialog with the available devices
        dlg = wx.SingleChoiceDialog(parent=self, message="Select a Device",
                                    caption="Select a Device",
                                    choices=self.controller.get_devices())

        # Show the dialog as modal, and if the OK button is pressed,
        # and a valid option was selected
        if dlg.ShowModal() == wx.ID_OK and dlg.GetSelection >= 0:
            # Tell the controller the selected
            self.controller.set_device(dlg.GetSelection())

            # Remember that we've selected a device now
            self.device_selected = True

            # Reset the system so it will now ask
            self.reset_asking()

        # Else if a device is already selected
        elif self.device_selected:
            # Then just reset the asking state
            self.reset_asking()

    def on_exit(self, e):
        """
        Quits the application

        :param e: Event - not used
        """

        # Remove and destroy the tray
        self.tray.RemoveIcon()
        self.tray.Destroy()
        # Destroy ourself
        self.Destroy()
        self.controller.StopThread.set()
        exit()

    def min_to_tray(self, e):
        """
        Minimizes the window to the system tray

        :param e: Event - Unused
        """

        # If no device has been selected yet
        if not self.device_selected:
            # Just exit
            self.on_exit(e)
            return

        # Otherwise, hide the main GUI
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

        # Tell the controller it's minimized
        self.controller.poll = True

    def max_from_tray(self, e):
        """
        Return the GUI from the system tray.

        :param e: Event - unused.
        """

        # Reset so it's asking for the controller button
        self.reset_asking()

        self.Restore()  # Restore the main GUI
        self.Show()  # Show the main GUI
        self.Raise()  # Raise the main GUI (Just in case)
        self.tray.RemoveIcon()  # Remove the tray icon

        # Tell the controller it's maximized
        self.controller.poll = False

    def key_up(self, e):
        if self.waiting_for_kbd_key:
            val = Vk2Sk.convert(e.GetRawKeyCode(), e.AltDown(), e.CmdDown(),
                                e.ShiftDown())
            if val is not None:
                self.controller.make_link(val)
                # self.SetAcceleratorTable(self.shortcuts)
                self.show_kbd_key(val)
            else:
                self.instr.SetLabel("Bad key combination.")

    # endregion

    # region Show / Hide Graphics

    # region Keyboard Key

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

        else:
            self.show_tick()
            threading.Timer(2, self.reset_asking).start()

        # Make the key visible
        self.bkk_ctrl.make_visible(char)

    def hide_kbd_key(self):
        """ Hides the keyboard key. """

        self.bkk_ctrl.make_hidden()
        self.instr.SetLabel("")

    # endregion

    # region Controller Key

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

    # endregion

    # region Tick

    def show_tick(self):
        """
        Shows an animated check mark and displays a message saying that the
        mapping has been successful.
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
        # After 1.1 seconds stop it (so it never repeats)
        threading.Timer(1.1, self.gif.Stop).start()

    def hide_tick(self):
        """ Hides the check mark. """
        try:
            if self.gif is not None:
                self.gif.Hide()
                self.gif.Destroy()
        except wx.PyDeadObjectError:
            pass

    # endregion

    # endregion

    # region Reset GUI

    def reset_asking(self):
        """
        Resets the GUI to either be asking for a controller button press
        or put up the Select Device button
        """

        self.hide_crl_key()  # Hide the controller key
        self.hide_kbd_key()  # Hide the keyboard key
        self.hide_tick()  # Hide the tick
        self.waiting_for_crl_btn = False  # Don't be waiting for anything
        self.waiting_for_kbd_key = False

        # If a device has been selected
        if self.device_selected:
            self.select_dev_btn.Hide()  # Hide the Select Device button

            # Be waiting for the controller button press
            self.waiting_for_crl_btn = True  # Yes we want a controller button
            self.controller.get_btn_press()

            # And show the controller key
            self.show_crl_key()  # Make the controller button visible

        # Else, ensure the Select Device button is visible
        else:
            self.select_dev_btn.Show()

    # endregion

    # region Callable from Controller

    def crl_btn_pressed(self):
        """ Called whenever the controller button has been pressed. """

        # If we're waiting for a controller key press
        if self.waiting_for_crl_btn:
            self.show_crl_key("X")  # Show an X
            self.show_kbd_key()  # Make the keyboard button visible
            self.waiting_for_crl_btn = False
            self.waiting_for_kbd_key = True
            # self.SetAcceleratorTable(wx.NullAcceleratorTable)
            self.SetFocus()

    def device_unplugged(self):
        """ Resets the app to to have a device selected. """
        import antigravity
        self.device_selected = False  # Set that no device has been selected.
        self.max_from_tray(None)  # And maximize from the tray

        # Recreate the controller, since the thread has been stopped now.
        self.controller = Controller(self.crl_btn_pressed, self.device_unplugged)

    # endregion


ex = wx.App(False, None, True, True)
CGUI(None, title=CGUI.SYSTEM_NAME)
ex.MainLoop()


