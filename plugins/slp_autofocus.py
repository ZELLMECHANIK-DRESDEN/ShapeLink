import shutil

import numpy as np
import nrefocus

from shapelink import ShapeLinkPlugin

# We use the terminal width to make sure a line doesn't get cluttered
# with prints from a previous line.
TERMINAL_WIDTH = shutil.get_terminal_size((80, 20))[0]


class AutofocusPlugin(ShapeLinkPlugin):
    """Displays a rolling mean of a few scalar features"""
    def __init__(self, *args, **kwargs):
        super(AutofocusPlugin, self).__init__(*args, **kwargs)

    def after_register(self):
        print(" Preparing for transmission")

    def after_transmission(self):
        print("\n End of transmission\n")

    def choose_features(self):
        feats = ["image"]
        return feats

    def handle_event(self, event_data):
        """Handle a new event"""

        # gather image, create fft to get fake phase
        # use nrefocus to autofocus it
        # get direction and magnitude of defocus needed
        # how to pass this value to another program?

        image = event_data.images[0]
        # fake a complex image
        fft = np.fft.fft2(image)
        ifft = np.fft.ifft2(fft)

        # how to feed these? or default?
        focus_range = (-20, 20)
        pixel_size = 0.34
        light_wavelength = 0.532

        afocus = nrefocus.RefocusNumpy(
            ifft, light_wavelength, pixel_size)
        focus_distance = afocus.autofocus(focus_range)
        # send to objective
        #  via a log file? Write the focus values to log?
        # What is the direction of the focus? Or is it an absolute value?

        return False


info = {
    "class": AutofocusPlugin,
    "description": "Autofocus hologram images using nrefocus",
    "name": "Autofocus",
    "version": "0.1.1",
}
