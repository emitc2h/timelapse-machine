from kivy.uix.boxlayout import  BoxLayout
from kivy.properties import ObjectProperty

## ==================================
class TopBar(BoxLayout):
    """
    The top bar in the TLM interface
    """
    path          = ObjectProperty(None)
    button_open   = ObjectProperty(None)
    button_save   = ObjectProperty(None)
    button_render = ObjectProperty(None)