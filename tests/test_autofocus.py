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
        event_data.images[0]  # should be the hologram

        # use qpimage to process the hologram
        qpi = qpimage.QPImage(data=self.hologram, which_data="hologram")
        field = qpi.field

        # example nrefocus parameters
        focus_range = (30e-6, 35e-6)
        pixel_size = 0.34e-6
        light_wavelength = 532e-9
        default_focus = 0
        # use nrefocus to calculate autofocus
        afocus = nrefocus.RefocusNumpy(
            field, light_wavelength, pixel_size, distance=default_focus)
        focus_distance = afocus.autofocus(focus_range)

        assert np.isclose(focus_distance, 3.3086177092746745e-05)

        return False


def test_run_plugin_with_user_defined_trace_features(hologram=img_crop):
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None, "tcp://localhost:6669", 0)
                          )

    # setup plugin
    p = AutofocusHologramFakeShapeLinkPlugin(
        bind_to='tcp://*:6669', hologram=hologram)
    # start simulator
    th.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()


def test_calculate_focus_after_propagation():
    # open jpg
    holo_im = data_dir / "hologram_cell_curved_bg.jpg"
    img = cv2.imread(str(holo_im), cv2.IMREAD_GRAYSCALE)
    img_crop = img[300:500, 100:300]

    # defocus image
    qpi = qpimage.QPImage(data=img_crop,
                          which_data="hologram")
    field = qpi.field
    focus_range = (0, 40e-6)
    pixel_size = 0.34e-6
    light_wavelength = 532e-9
    initial_distance = 0.0
    afocus = nrefocus.RefocusNumpy(
        field, light_wavelength, pixel_size, distance=initial_distance)
    focus1 = afocus.autofocus(focus_range)
    assert np.isclose(focus1, 3.3086177092746745e-05)

    # move it by 10e-6
    prop_val = 10e-6
    prop_field = afocus.propagate(prop_val)

    # save in temp file
    tpath = pathlib.Path(tempfile.mkdtemp())
    expath = tpath / "exported.npy"
    with expath as exp:
        np.save(exp, prop_field)
        # open defocused field
        prop_loaded = np.load(str(expath))
        qpi2 = qpimage.QPImage(data=prop_loaded, which_data="field")
        field2 = qpi2.field
        afocus2 = nrefocus.RefocusNumpy(
            field2, light_wavelength, pixel_size, distance=prop_val)
        # find focus of defocused image
        focus2 = afocus2.autofocus(focus_range)
        # focus2 is different to focus1 for some reason.
        # Reported in github.com/RI-imaging/nrefocus/issues/13
        assert np.isclose(focus2, 3.060066446129425e-05)
        assert not np.isclose(focus1, focus2)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
