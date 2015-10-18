import cv2, numpy, os, math
from kivy.graphics.texture import Texture
from os.path import expanduser
home = expanduser("~")

## ======================================
class Sequence:

    frames = []
    textures = []

    ## --------------------------------------
    def __init__(self, path, img_ext='.jpg', img_range=(None, None)):
        """
        Constructor
        """

        self.path  = path
        self.path  = path.replace('~', home)
        self.files = os.listdir(self.path)
        self.files = sorted([f for f in self.files if f.lower().endswith(img_ext)])

        if img_range[0] is None: img_range = (0, img_range[1])
        if img_range[1] is None: img_range = (img_range[0], len(self.files))

        self.range    = img_range
        self.n_frames = img_range[1]
        self.loaded_frames = 0


    ## --------------------------------------
    def load_one_frame(self):
        """
        Loads a single frame
        """

        if self.loaded_frames >= self.n_frames: return False

        frame = cv2.imread(os.path.join(self.path, self.files[self.loaded_frames]))

        aspect_ratio = float(frame.shape[1])/frame.shape[0]

        ## Calculate total video size
        total_size = self.n_frames * float(frame.shape[0]*frame.shape[1]*frame.shape[2]*8) / (1024)**3
        x = 2.0/math.sqrt(total_size)

        frame = cv2.resize(frame, (int(x * frame.shape[1]), int(x * frame.shape[0])), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 0)

        self.frames.append(frame)

        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tostring(), bufferfmt="ubyte", colorfmt="bgr")

        self.textures.append(texture)

        self.loaded_frames += 1

        return True


    ## --------------------------------------
    def get_blurred_frame(self, frame_index):
        """
        returns a blurred frame texture
        """

        frame = self.frames[frame_index]
        blurred_frame = cv2.GaussianBlur(frame, (101, 101), 0)

        texture = Texture.create(size=(blurred_frame.shape[1], blurred_frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(blurred_frame.tostring(), bufferfmt="ubyte", colorfmt="bgr")

        return texture

