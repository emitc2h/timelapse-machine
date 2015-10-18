from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty



## ==================================
class Parameters(BoxLayout):

    fps_default = 24.0
    fps_current = fps_default

    set_codec            = ObjectProperty(None)
    set_fps              = ObjectProperty(None)
    keep_aspect_ratio    = ObjectProperty(None)
    set_width            = ObjectProperty(None)
    set_height           = ObjectProperty(None)
    button_original_size = ObjectProperty(None)


    ## ---------------------------------------
    def enter_fps(self):
        """
        Seize the FPS value upon pressing Enter while the focus is on the text field
        """

        fps_text = self.set_fps.text
        new_fps = self.fps_current
        try:
            new_fps = float(fps_text)
        except TypeError:
            pass

        if not new_fps > 0.0:
            new_fps = self.fps_current

        self.fps_current = new_fps
        self.set_fps.text = str(self.fps_current)