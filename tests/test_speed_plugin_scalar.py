import pathlib
import threading
import time
import dclab

from shapelink import shapein_simulator
from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"
ds_test = dclab.new_dataset(data_dir / "calibration_beads_47.rtdc")


class ChooseScalarFeaturesShapeLinkPlugin(ShapeLinkPlugin):
    """Checks if only the chosen features are transferred"""
    def __init__(self, *args, **kwargs):
        super(ChooseScalarFeaturesShapeLinkPlugin, self).__init__(
            *args, **kwargs)

    def choose_features(self):
        user_feats = ['area_cvx', 'area_msd', 'area_ratio', 'area_um',
                      'aspect', 'bright_avg', 'bright_sd', 'circ', 'deform',
                      'pos_x', 'pos_y', 'size_x', 'size_y',
                      'tilt', 'time', 'volume']
        return user_feats

    def handle_event(self, event_data: EventData) -> bool:
        """Check that the chosen scalar features were transferred"""
        for feat in event_data.scalars:
            assert isinstance(feat, float)
        time.sleep(0.5)

        return False


def test_speed_of_scalar_transfer():
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None, "tcp://localhost:6668", 0)
                          )
    # setup plugin
    p = ChooseScalarFeaturesShapeLinkPlugin(bind_to='tcp://*:6668')
    # start simulator
    th.start()
    # initalize variables, otherwise first time measurement is too long
    # because variables are initalized there
    counter = 0
    time_sum = 0
    # start plugin
    for ii in range(49):
        # setup initial time
        time1 = time.time_ns()
        p.handle_messages()
        time2 = time.time_ns()

        # calculation of mean value
        counter += 1
        dt_us = (time2 - time1) / 1000
        time_sum += dt_us
        print(f"Times: {time1}, {time2}, {dt_us}")
        print(f"Data transferred in {dt_us} µs, mean: {time_sum/counter})")
        time.sleep(0.5)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
