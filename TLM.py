#!/usr/bin/env kivy

## Set initial window size
from kivy.config import Config
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '900')

## kivy imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import  BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.garden.filebrowser import FileBrowser
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.clock import Clock

## python imports
import os

## image processing imports
import cv2

## TLM imports
from ui.core.codecs import codecs

## Load kivy configurations for other objects
Builder.load_file('ui/topbar.kv')
Builder.load_file('ui/configuration.kv')
Builder.load_file('ui/viewer.kv')
Builder.load_file('ui/curveeditor.kv')
Builder.load_file('ui/parameters.kv')

from ui.core.tlm import TLM



## ==================================
class OpenDialog(FloatLayout):
    """
    The dialog that pops up to open a new sequence
    """
    filebrowser   = ObjectProperty(None)
    button_load   = ObjectProperty(None)
    button_cancel = ObjectProperty(None)



## ==================================
class Root(FloatLayout):
    """
    The true root widget, which handles the TLM widget and the open dialog widget,
    takes care of the master functionalities of the program in the top bar.
    """

    out           = None
    path          = None
    tlm           = ObjectProperty(None)
    opendialog    = ObjectProperty(None)
    render_clock  = None
    render_screen = None


    ## ----------------------------------
    def dismiss_popup(self, *args, **kwargs):
        """
        dismiss the open dialog
        """
        self.popup.dismiss()


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
        self.popup = Popup(title="locate directory", content=self.opendialog, size_hint=(0.9, 0.9))
        self.popup.open()


    ## ----------------------------------
    def load(self, path, filename, *args, **kwargs):
        """
        specify the path to load
        """
        if len(filename) > 0:
            self.path = os.path.join(path, filename[0])
            self.tlm.ui_path.text = '    ' + self.path
            self.tlm.viewer.load(self.path)

        self.dismiss_popup()


    ## ----------------------------------
    def render(self, *args, **kwargs):
        """
        render the time-lapse
        """

        if self.path is None: return

        self.codec = codecs[self.tlm.ui_codec.selected_codec]

        self.out = cv2.VideoWriter(
            '{0}{1}'.format(self.path.rstrip('/'), self.codec.ext),
            self.codec.fourcc,
            self.tlm.parameters.fps_current,
            (self.tlm.parameters.width_current, self.tlm.parameters.height_current),
            isColor=True
            )

        self.tlm.ui_slider.value = 0

        self.render_clock = Clock.schedule_interval(self.render_frame, 0)

        with self.tlm.ui_screen.canvas.after:
            self.render_screen = Rectangle(
                source='img/render_screen.png',
                pos=self.tlm.viewer.pos,
                size=self.tlm.viewer.size)

        self.tlm.viewer.disable()


    ## ----------------------------------
    def render_frame(self, *args, **kwargs):
        """
        Add one frame to the movie
        """

        frame_path = self.tlm.viewer.sequence.files[self.tlm.ui_slider.value]

        img = cv2.imread(frame_path)
        img = cv2.resize(
            img,
            (self.tlm.parameters.width_current, self.tlm.parameters.height_current),
            interpolation=cv2.INTER_AREA
            )

        self.out.write(img)

        self.tlm.ui_slider.value +=1

        ## When done, do the following
        if self.tlm.ui_slider.value > self.tlm.viewer.sequence.n_frames -1:
            self.out.release()
            os.rename(
                '{0}{1}'.format(self.path.rstrip('/'), self.codec.ext),
                '{0}{1}'.format(self.path.rstrip('/'), self.codec.rename_ext)
                )

            Clock.unschedule(self.render_clock)
            self.render_clock = None

            self.tlm.ui_screen.canvas.after.remove(self.render_screen)
            self.tlm.viewer.enable()





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
        tlm.ui_open.bind(on_release=root.show_load)
        tlm.ui_render.bind(on_release=root.render)

        return root


## Register all widgets to be shown in the factory
Factory.register('Root', cls=Root)
Factory.register('OpenDialog', cls=OpenDialog)
Factory.register('TLM', cls=TLM)
Factory.register('FileBrowser', cls=FileBrowser)



## ==================================
if __name__=="__main__":
    TLMApp().run()