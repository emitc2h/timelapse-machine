from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty



## ==================================
class Parameters(BoxLayout):

    fps_default   = 24.0
    fps_current   = fps_default

    width_default  = None
    width_current  = None

    height_default = None
    height_current = None

    aspect_ratio_default = None
    aspect_ratio_current = None

    ## Upstream reference to TLM
    tlm = ObjectProperty(None)

    ## ui elements
    ui_codec    = ObjectProperty(None)
    ui_fps      = ObjectProperty(None)
    ui_ratio    = ObjectProperty(None)
    ui_width    = ObjectProperty(None)
    ui_height   = ObjectProperty(None)
    ui_original = ObjectProperty(None)


    ## ---------------------------------------
    def enter_fps(self):
        """
        Seize the FPS value upon pressing Enter while the focus is on the text field
        """

        fps_text = self.ui_fps.text
        new_fps = self.fps_current
        try:
            new_fps = float(fps_text)
        except TypeError:
            pass

        if not new_fps > 0.0:
            new_fps = self.fps_current

        self.fps_current = new_fps
        self.ui_fps.text = str(self.fps_current)


    ## ---------------------------------------
    def update_fields(self):
        """
        update fields
        """

        self.ui_width.text = str(self.width_current)
        self.ui_height.text = str(self.height_current)


    ## ---------------------------------------
    def default(self):
        """
        back to default size
        """

        self.width_current = self.width_default
        self.height_current = self.height_default
        self.aspect_ratio_current = self.aspect_ratio_default
        self.update_fields()


    ## ---------------------------------------
    def enter_width(self):
        """
        Enter the width
        """

        self.width_current = int(self.ui_width.text)
        if self.ui_ratio.active:
            self.height_current = int(self.width_current/self.aspect_ratio_current)
        else:
            self.aspect_ratio_current = float(self.width_current)/self.height_current
        self.update_fields()


    ## ---------------------------------------
    def enter_height(self):
        """
        Enter the width
        """

        self.height_current = int(self.ui_height.text)
        if self.ui_ratio.active:
            self.width_current = int(self.height_current*self.aspect_ratio_current)
        else:
            self.aspect_ratio_current = float(self.width_current)/self.height_current
        self.update_fields()


