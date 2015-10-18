from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

codec_selector_height = 40
codecs = ['raw', 'mpeg', 'h264', 'xvid', 'more', 'codecs', 'available']

## ==================================
class CodecSelector(BoxLayout):

    ## ----------------------------------
    def __init__(self, **kwargs):
        """
        Constructor
        """

        super(CodecSelector, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = codec_selector_height
        self.build()

    ## ----------------------------------
    def build(self):
        """
        Build the CodecSelector
        """

        ## Button to bring out the drop-down menu
        self.button_main = Button(
            text='select video codec',
            size_hint_y=None,
            height=codec_selector_height
            )

        ## The drop-down menu itself
        self.dropdown = DropDown()

        ## The codec options
        self.buttons_codec = {}
        for codec in codecs:
            button_codec = Button(
                background_normal='',
                color=(0,0,0,1),
                text=codec,
                size_hint_y=None,
                height=self.height,
                )

            ## when clicking on one of the drop-down menu items, select it
            button_codec.bind(on_release=self.dropdown.select)

            self.buttons_codec[codec] = button_codec
            self.dropdown.add_widget(button_codec)

        ## Bind button releasing to opening the drop-down menu
        self.button_main.bind(on_release=self.dropdown.open)

        ## Click anywhere to dimiss the drop-down menu
        self.dropdown.bind(on_parent=self.dropdown.dismiss)

        ## Put the text of the selected item on the main button
        def f_dropdown_label(*args):
            self.button_main.text = args[1].text
        self.dropdown.bind(on_select=f_dropdown_label)

        ## Group items
        self.add_widget(self.button_main)
