from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.clock import Clock

from core.sequence import Sequence


## ======================================
class Viewer(BoxLayout):
    """
    A Widget that looks like a video player, but
    works on loaded textures to show a preview of the
    timelapse video
    """
    
    ## Clocks
    load_clock = None
    play_clock = None
    reverse_clock = None

    load_screen = None
    screen = ObjectProperty(None)
    slider = ObjectProperty(None)
    controls = ObjectProperty(None)
    parameters = ObjectProperty(None)
    sequence = None
    current_frame_index = 0



    ## ---------------------------------------
    def load(self, path):
        """
        Loads the video
        """
        self.sequence   = Sequence(path)
        self.slider.max = self.sequence.n_frames
        self.load_clock = Clock.schedule_interval(self.update_load, 0)

        with self.screen.canvas.after:
            self.load_screen = Rectangle(source='img/load_screen.png', pos=self.pos, size=self.size)


    ## ---------------------------------------
    def update_frame(self, value=None):
        """
        Update the frame on the screen
        """

        if not value is None:
            self.current_frame_index = int(value)

        if self.current_frame_index < 0:
            if not self.reverse_clock is None:
                Clock.unschedule(self.reverse_clock)
                self.reverse_clock = None
                return

        if self.current_frame_index >= self.sequence.n_frames - 1:
            self.current_frame_index = self.sequence.n_frames - 1
            if not self.play_clock is None:
                Clock.unschedule(self.play_clock)
                self.play_clock = None
                return

        if not self.loaded:
            self.screen.texture = self.sequence.get_blurred_frame(self.current_frame_index)
        else:
            self.screen.texture = self.sequence.textures[self.current_frame_index]


    ## ---------------------------------------
    def update_load(self, dt):
        """
        Updates the screen while loading
        """

        self.loaded = not self.sequence.load_one_frame()
        self.current_frame_index = self.sequence.loaded_frames - 1
        self.slider.value = self.current_frame_index

        ## If the sequence is done loading
        if self.loaded:

            ## Unschedule and remove the loading clock
            if not self.load_clock is None:
                Clock.unschedule(self.load_clock)
                self.load_clock = None

            self.enable()

            ## Bind buttons
            self.controls.button_begin.bind(on_press=self.begin)
            self.controls.button_back.bind(on_press=self.back)
            self.controls.button_reverse.bind(on_press=self.reverse)
            self.controls.button_pause.bind(on_press=self.pause)
            self.controls.button_play.bind(on_press=self.play)
            self.controls.button_forward.bind(on_press=self.forward)
            self.controls.button_end.bind(on_press=self.end)

            ## Clear the load screen
            self.screen.canvas.after.remove(self.load_screen)

            ## Return the slider to the beginning
            self.slider.value = 0

            ## Pass on parameters
            self.parameters.width_default = self.sequence.width
            self.parameters.width_current = self.sequence.width

            self.parameters.height_default = self.sequence.height
            self.parameters.height_current = self.sequence.height

            self.parameters.aspect_ratio_default = self.sequence.aspect_ratio
            self.parameters.aspect_ratio_current = self.sequence.aspect_ratio

            self.parameters.update_fields()



    ## ---------------------------------------
    def begin(self, *args):
        """
        Goes to beginning of video, stops playing
        """

        self.pause()
        self.slider.value = 0


    ## ---------------------------------------
    def back(self, *args):
        """
        Goes back one frame in video, stops playing
        """

        self.current_frame_index -= 1
        self.slider.value = self.current_frame_index


    ## ---------------------------------------
    def reverse(self, *args):
        """
        Plays video in reverse at the specified frame rate
        """

        self.pause()
        self.reverse_clock = Clock.schedule_interval(self.back, 1.0/self.parameters.fps_current)


    ## ---------------------------------------
    def play(self, *args):
        """
        Plays video
        """

        self.pause()
        self.play_clock = Clock.schedule_interval(self.forward, 1.0/self.parameters.fps_current)


    ## ---------------------------------------
    def pause(self, *args):
        """
        Pauses video
        """

        if not self.reverse_clock is None:
            Clock.unschedule(self.reverse_clock)
            self.reverse_clock = None

        if not self.play_clock is None:
            Clock.unschedule(self.play_clock)
            self.play_clock = None

        if not self.load_clock is None:
            Clock.unschedule(self.load_clock)
            self.load_clock = None


    ## ---------------------------------------
    def forward(self, *args):
        """
        Goes forward one frame in video, stops playing
        """
        self.current_frame_index += 1
        self.slider.value = self.current_frame_index


    ## ---------------------------------------
    def end(self, *args):
        """
        Goes to end of video, stops playing
        """

        self.pause()
        self.slider.value = self.sequence.n_frames - 1


    ## ---------------------------------------
    def enable(self, *args):
        """
        enable the viewer controls
        """

        ## Enable slider
        self.slider.disabled = False

        ## Enable buttons
        self.controls.button_begin.disabled = False
        self.controls.button_back.disabled = False
        self.controls.button_reverse.disabled = False
        self.controls.button_pause.disabled = False
        self.controls.button_play.disabled = False
        self.controls.button_forward.disabled = False
        self.controls.button_end.disabled = False


    ## ---------------------------------------
    def disable(self, *args):
        """
        disable the viewer controls
        """

        ## Enable slider
        self.slider.disabled = True

        ## Enable buttons
        self.controls.button_begin.disabled =   True
        self.controls.button_back.disabled =    True
        self.controls.button_reverse.disabled = True
        self.controls.button_pause.disabled =   True
        self.controls.button_play.disabled =    True
        self.controls.button_forward.disabled = True
        self.controls.button_end.disabled =     True



## ======================================
class Controls(BoxLayout):
    """
    Houses buttons to control the video player
    """

    button_begin   = ObjectProperty(None)
    button_back    = ObjectProperty(None)
    button_reverse = ObjectProperty(None)
    button_pause   = ObjectProperty(None)
    button_play    = ObjectProperty(None)
    button_forward = ObjectProperty(None)
    button_end     = ObjectProperty(None)
