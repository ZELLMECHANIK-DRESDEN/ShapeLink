import pathlib
import tempfile
import threading
import numpy as np
import cv2
import nrefocus
import qpimage

from shapelink import shapein_simulator
from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"
# open and crop hologram image
holo_im = data_dir / "hologram_cell_curved_bg.jpg"
img = cv2.imread(str(holo_im), cv2.IMREAD_GRAYSCALE)
img_crop = img[300:500, 100:300]


class AutofocusHologramFakeShapeLinkPlugin(ShapeLinkPlugin):
    """A guiding plugin for autofocussing with a hologram"""
    def __init__(self, hologram, coarse_search, *args, **kwargs):
        super(AutofocusHologramFakeShapeLinkPlugin, self).__init__(
            *args, **kwargs)
        self.hologram = hologram
        self.coarse_search = coarse_search

    def choose_features(self):
        feats = ["image"]
        # We are using img_crop in this plugin, but we still would like
        # Shape-In to send us something to simulate our workflow.
        # This is why this is a "fake" plugin.
        return feats

    def handle_event(self, event_data: EventData) -> bool:
        """Check that the chosen features were transferred"""

        # retrieve the hologram image
        # here is just an example, as our rtdc file does
        # not have a hologram, so we use a fake dataset (see above)
        event_data.images[0]  # should be the hologram

        # use qpimage to process the hologram
        qpi = qpimage.QPImage(data=self.hologram, which_data="hologram")
        field = qpi.field

        # example nrefocus parameters
        if self.coarse_search:
            focus_range = (20.0e-6, 30.0e-6)
        else:
            focus_range = (26.0e-6, 26.3e-6)
        pixel_size = 0.34e-6
        light_wavelength = 532e-9
        default_focus = 0
        # use nrefocus to calculate autofocus
        afocus = nrefocus.RefocusPyFFTW(
            field, light_wavelength, pixel_size,
            distance=default_focus, padding=False)
        focus_distance = afocus.autofocus(focus_range)

        assert np.isclose(focus_distance, 2.61756e-05)

        return False


def test_autofocus_fake_hologram_coarse(hologram=img_crop,
                                        coarse_search=True):
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None, "tcp://localhost:6669", 0)
                          )

    # setup plugin
    p = AutofocusHologramFakeShapeLinkPlugin(
        bind_to='tcp://*:6669', hologram=hologram,
        coarse_search=coarse_search)
    # start simulator
    th.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()


def test_autofocus_fake_hologram_no_coarse(hologram=img_crop,
                                           coarse_search=False):
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None, "tcp://localhost:6669", 0)
                          )

    # setup plugin
    p = AutofocusHologramFakeShapeLinkPlugin(
        bind_to='tcp://*:6669', hologram=hologram,
        coarse_search=coarse_search)
    # start simulator
    th.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()


def test_calculate_focus_after_propagation():
    # defocus image
    qpi = qpimage.QPImage(data=img_crop,
                          which_data="hologram")
    field = qpi.field
    focus_range = (0, 30e-6)
    pixel_size = 0.34e-6
    light_wavelength = 532e-9
    initial_distance = 0.0
    # padding must be False for reproducible defocus values between
    # the first and second autofocus
    padding = False
    afocus1 = nrefocus.RefocusPyFFTW(
        field, light_wavelength, pixel_size,
        distance=initial_distance, padding=padding)
    focus1 = afocus1.autofocus(focus_range)
    assert np.isclose(focus1, 2.61756e-05)

    # move it by 10e-6
    prop_val = 20e-6
    prop_field = afocus1.propagate(prop_val)

    # save in temp file
    tpath = pathlib.Path(tempfile.mkdtemp())
    expath = tpath / "exported.npy"
    with expath as exp:
        np.save(exp, prop_field)
        # open defocused field
        prop_loaded = np.load(str(expath))
        qpi2 = qpimage.QPImage(data=prop_loaded, which_data="field")
        field2 = qpi2.field
        afocus2 = nrefocus.RefocusPyFFTW(
            field2, light_wavelength, pixel_size,
            distance=prop_val, padding=padding)
        focus2 = afocus2.autofocus(focus_range)
        assert np.isclose(focus2, 2.61756e-05)
        assert np.isclose(focus1, focus2)

        # show that for a distance of zero, the focus is shifted by prop_val
        afocus3 = nrefocus.RefocusPyFFTW(
            field2, light_wavelength, pixel_size,
            distance=0, padding=padding)
        focus3 = afocus3.autofocus(focus_range)
        assert np.isclose(focus3, 0.61756e-05)
        assert np.isclose(focus3, focus1-prop_val)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
