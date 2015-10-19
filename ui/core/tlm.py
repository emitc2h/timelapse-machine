from kivy.uix.boxlayout import  BoxLayout
from kivy.properties import ObjectProperty

## ==================================
class TLM(BoxLayout):
    """
    The TLM interface root widget
    """

    ## Relations to interface modules
    viewer     = ObjectProperty(None)
    parameters = ObjectProperty(None)

    ## Topbar ui elements
    ui_open   = ObjectProperty(None)
    ui_path   = ObjectProperty(None)
    ui_cancel = ObjectProperty(None)
    ui_save   = ObjectProperty(None)
    ui_render = ObjectProperty(None)

    ## Parameters ui elements
    ui_codec    = ObjectProperty(None)
    ui_fps      = ObjectProperty(None)
    ui_ratio    = ObjectProperty(None)
    ui_width    = ObjectProperty(None)
    ui_height   = ObjectProperty(None)
    ui_original = ObjectProperty(None)

    ## Viewer ui elements
    ui_screen  = ObjectProperty(None)
    ui_slider  = ObjectProperty(None)
    ui_begin   = ObjectProperty(None)
    ui_back    = ObjectProperty(None)
    ui_reverse = ObjectProperty(None)
    ui_pause   = ObjectProperty(None)
    ui_play    = ObjectProperty(None)
    ui_forward = ObjectProperty(None)
    ui_end     = ObjectProperty(None)