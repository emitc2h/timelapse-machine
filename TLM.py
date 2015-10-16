from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout

## Load external UI elements
Builder.load_file('ui/topbar.kv')
Builder.load_file('ui/selector.kv')
Builder.load_file('ui/configuration.kv')
Builder.load_file('ui/viewer.kv')
Builder.load_file('ui/curveeditor.kv')


## ==================================
class TLM(AnchorLayout):
    pass

## ==================================
class TLMApp(App):
    def build(self):
        return TLM()

## ==================================
if __name__=="__main__":
    TLMApp().run()