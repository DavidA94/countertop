import wx


class ButtonControl(wx.PyControl):
    """
    A Custom class for handling individual buttons. Allows the button (image)
    to be hidden/shown, and have a single character placed on top of it.
    """

    def __init__(self, parent, img, font, color=(0,0,0), id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="ButtonControl"):
        """
        Default class constructor.

        @param parent: Parent window. Must not be None.
        @param id: ButtonControl identifier. A -1 indicates a default value.
        @param img: The image to be displayed (of type wx.Image).
        @param font: The font for the text on top of the button
        @param color: The color to be used for the text (Of type tuple)
        @param pos: ButtonControl position. If the position (-1, -1) is
                    specified then a default position is chosen.
        @param size: ButtonControl size. If the default size (-1, -1) is
                     specified then a default size is chosen.
        @param style: Not used
        @param validator: Window validator.
        @param name: Window name.
        """

        # Call the parent
        wx.PyControl.__init__(self, parent, id, pos, size, style, validator,
                              name)
        self._parent = parent  # So we can get the background color
        self._visible = False  # Hidden by default
        self._char = ""  # No default character
        self._image = img  # Remember the image
        self._font = font  # Remember the font
        self._color = color  # For the color of the char font

        # Set the size to the size of the image
        self.SetInitialSize((img.GetWidth(), img.GetHeight()))

        # Bind ourselves to on_paint so we can handle that.
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):

        # Reduce flicker by by using BufferedPaintDC
        dc = wx.BufferedPaintDC(self)
        dc.SetFont(self._font)

        # Initialize the wx.BufferedPaintDC, assigning a background
        # color and a foreground color (to draw the text)
        back_color = self._parent.GetBackgroundColour()
        back_brush = wx.Brush(back_color, wx.SOLID)
        dc.SetBackground(back_brush)
        dc.Clear()

        # If we're visible
        if self._visible is True:
            # Draw the image
            dc.DrawBitmap(self._image.ConvertToBitmap(), 0, 0, True)

            # Measure the size of the character
            w, h = dc.GetTextExtent(self._char)

            # If it has a width and height
            if w > 0 and h > 0:
                # Set the text color
                dc.SetTextForeground(self._color)
                # Draw the text
                dc.DrawText(text=self._char,
                            x=(self._image.GetWidth() - w) / 2,
                            y=(self._image.GetHeight() - h) / 2)

    def make_visible(self):
        """
        Causes the button to be visible
        """
        self._visible = True
        self.Refresh()

    def make_hidden(self):
        """
        Causes the button to be hidden
        """

        self._visible = False
        self.Refresh()

    def set_char(self, char):
        """
        Sets the character to be displayed with the button
        :param char: The character to be displayed (must be len() == 0)
        """

        if len(char) > 0:
            self._char = char[0]
            self.Refresh()