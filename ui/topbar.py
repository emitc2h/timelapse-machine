from kivy.uix.boxlayout import  BoxLayout
from kivy.properties import ObjectProperty

## ==================================
class TopBar(BoxLayout):
    """
    The top bar in the TLM interface
    """

    ## Upstream reference to TLM
    tlm = ObjectProperty(None)

    ## ui elements
    ui_path   = ObjectProperty(None)
    ui_open   = ObjectProperty(None)
    ui_cancel = ObjectProperty(None)
    ui_save   = ObjectProperty(None)
    ui_render = ObjectProperty(None)