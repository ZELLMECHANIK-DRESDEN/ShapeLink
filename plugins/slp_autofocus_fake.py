
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
        # We are using img_crop in this plugin, but we still would like
        # Shape-In to send us something to simulate our workflow.
        # This is why this is a "fake" plugin.
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
        # would be faster if this interval was smaller, see the tests
        focus_range = (20e-6, 30e-6)
        pixel_size = 0.34e-6
        light_wavelength = 532e-9
        # use nrefocus to calculate autofocus
        afocus = nrefocus.RefocusPyFFTW(
            field, light_wavelength, pixel_size, padding=False)
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
