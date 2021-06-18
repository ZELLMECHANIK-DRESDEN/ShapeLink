
import pathlib

import cv2
import nrefocus
import qpimage
import numpy as np

from shapelink import ShapeLinkPlugin


# open and crop hologram image
holo_im = pathlib.Path(__file__).parents[1] / \
          "tests" / "data" / "hologram_cell_curved_bg.jpg"
img = cv2.imread(str(holo_im), cv2.IMREAD_GRAYSCALE)
img_crop = img[300:500, 100:300]


class AutofocusFakePlugin(ShapeLinkPlugin):
    """Display the defocus calculated from a hologram"""
    def __init__(self, *args, **kwargs):
        super(AutofocusFakePlugin, self).__init__(*args, **kwargs)

    def after_register(self):
        print(" Preparing for transmission")

    def after_transmission(self):
        print("\n End of transmission\n")

    def choose_features(self):
        feats = ["image"]
        # image will simulate the time take for a hologram
        return feats

    def handle_event(self, event_data):
        """Handle a new event"""

        # retrieve the hologram image
        # here is just an example, as our rtdc file does
        # not have a hologram, so we use a fake dataset (see above)
        event_data.images[0]  # should be the hologram

        # create some fake noise
        noise = np.random.rand(img_crop.shape[-1], img_crop.shape[-2])
        # use qpimage to process the hologram
        qpi = qpimage.QPImage(data=img_crop+noise,
                              which_data="hologram")
        field = qpi.field

        # example nrefocus parameters
        focus_range = (30, 35)
        pixel_size = 0.34
        light_wavelength = 0.532
        # use nrefocus to calculate autofocus
        afocus = nrefocus.RefocusNumpy(
            field, light_wavelength, pixel_size)
        focus_distance = afocus.autofocus(focus_range)

        # send to objective the absolute focus value
        # this value must first be calibrated with the z-stage
        # via a log file? Write the focus values to log?
        # emulate here with print
        print(focus_distance)

        return False


info = {
    "class": AutofocusFakePlugin,
    "description": "Autofocus a fake hologram image using "
                   "nrefocus and qpimage",
    "name": "Autofocus",
    "version": "0.1.1",
}
