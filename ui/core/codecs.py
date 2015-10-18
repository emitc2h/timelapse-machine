import cv2

## A small class to group information pertaining to a particular codec
## ===========================================
class Codec:

    ## -------------------------------------------
    def __init__(self, fourcc, ext, rename_ext = None):
        """
        Constructor
        """
        self.fourcc     = cv2.VideoWriter_fourcc(*fourcc)
        self.ext        = '.' + ext
        if not rename_ext is None:
            self.rename_ext = '.' + rename_ext
        else:
            self.rename_ext = self.ext
            

RAW  = Codec('raw ', 'raw', 'mov')
XVID = Codec('XVID', 'avi')
MJPG = Codec('MJPG', 'mov')
X264 = Codec('X264', 'mp4')

codecs = {
    'raw'  : RAW,
    'xvid' : XVID,
    'mpeg' : MJPG,
    'h.264' : X264
}