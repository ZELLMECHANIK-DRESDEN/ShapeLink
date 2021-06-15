import pathlib
import threading
import numpy as np
import cv2
import nrefocus
import qpimage

from shapelink import shapein_simulator
from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"


class AutofocusHologramFakeShapeLinkPlugin(ShapeLinkPlugin):
    """All FLUOR_TRACES are transferred because "trace" is provided"""
    def __init__(self, hologram, *args, **kwargs):
        super(AutofocusHologramFakeShapeLinkPlugin, self).__init__(
            *args, **kwargs)
        self.hologram = hologram

    def choose_features(self):
        feats = ["image"]
        # image will simulate the time take for a hologram
        return feats

    def handle_event(self, event_data: EventData) -> bool:
        """Check that the chosen features were transferred"""

        # retrieve the hologram image
        # here is just an example, as our rtdc file does
        # not have a hologram, so we use a fake dataset (see above)
        should_be_the_hologram = event_data.images[0]

        # use qpimage to process the hologram
        qpi = qpimage.QPImage(data=self.hologram,
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

        assert np.isclose(focus_distance, 33.086177092746745)

        return False


def test_run_plugin_with_user_defined_trace_features():
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None, "tcp://localhost:6668", 0)
                          )

    # open and crop hologram image
    holo_im = data_dir / "hologram_cell_curved_bg.jpg"
    img = cv2.imread(str(holo_im), cv2.IMREAD_GRAYSCALE)
    img_crop = img[300:500, 100:300]

    # setup plugin
    p = AutofocusHologramFakeShapeLinkPlugin(
        bind_to='tcp://*:6668', hologram=img_crop)
    # start simulator
    th.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
