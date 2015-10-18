from kivy.config import Config
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '900')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import  BoxLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.garden.filebrowser import FileBrowser

import os

## Load external UI elements
Builder.load_file('ui/topbar.kv')
Builder.load_file('ui/configuration.kv')
Builder.load_file('ui/viewer.kv')
Builder.load_file('ui/curveeditor.kv')
Builder.load_file('ui/parameters.kv')


## ==================================
class OpenDialog(FloatLayout):
    """
    A class to group properties of the open dialog
    """
    filebrowser   = ObjectProperty(None)
    button_load   = ObjectProperty(None)
    button_cancel = ObjectProperty(None)



 ## ==================================
class TLM(AnchorLayout):
    """
    The main TLM interface
    """
    topbar = ObjectProperty(None)
    viewer = ObjectProperty(None)



## ==================================
class Root(FloatLayout):
    """
    The master widget
    """

    tlm        = ObjectProperty(None)
    opendialog = ObjectProperty(None)


    ## ----------------------------------
    def dismiss_popup(self, *args, **kwargs):
        self._popup.dismiss()


    ## ----------------------------------
    def show_load(self, *args, **kwargs):
        """
        Creates and show the open dialog
        """

        ## Create the open dialog
        self.opendialog = OpenDialog()

        ## Bind the buttons
        def f_load(*args, **kwargs):
            self.load(self.opendialog.filebrowser.path, self.opendialog.filebrowser.selection)
        self.opendialog.filebrowser.bind(on_canceled=self.dismiss_popup, on_success=f_load)

        ## Create and open the popup in which the open dialog is placed
        self._popup = Popup(title="locate directory", content=self.opendialog, size_hint=(0.9, 0.9))
        self._popup.open()


    ## ----------------------------------
    def load(self, path, filename, *args, **kwargs):
        """
        specify the path to load
        """
        if len(filename) > 0:
            path = os.path.join(path, filename[0])
            self.tlm.topbar.path.text = '    ' + path
            self.tlm.viewer.load(path)

        self.dismiss_popup()



## ==================================
class TLMApp(App):
    """
    The App
    """
    
    ## ----------------------------------
    def build(self):
        """
        Builds the App
        """

        tlm = TLM()
        root = Root()
        root.add_widget(tlm)
        root.tlm = tlm
        tlm.topbar.button_open.bind(on_release=root.show_load)
        return root


## Register all widgets to be shown in the factory
Factory.register('Root', cls=Root)
Factory.register('OpenDialog', cls=OpenDialog)
Factory.register('TLM', cls=TLM)
Factory.register('FileBrowser', cls=FileBrowser)



## ==================================
if __name__=="__main__":
    TLMApp().run()