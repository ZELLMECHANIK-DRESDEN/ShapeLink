import pathlib
import threading

from shapelink import shapein_simulator
from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"


def run_plugin_feature_transfer(shapelink_plugin, random_port=True):
    # setup plugin
    p = shapelink_plugin(random_port=random_port)
    port_address = p.port_address
    # create new thread for simulator
    th = threading.Thread(target=shapein_simulator.start_simulator,
                          args=(str(data_dir / "calibration_beads_47.rtdc"),
                                None,
                                "tcp://localhost:{}".format(port_address), 0)
                          )
    # start simulator
    th.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()


class SingleScalarTransferSpeedShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        return ["circ"]

    def handle_event(self, event_data: EventData) -> bool:
        return False


class MultipleScalarTransferSpeedShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        user_feats = ['area_cvx', 'aspect', 'bright_avg',
                      'circ', 'deform']
        return user_feats

    def handle_event(self, event_data: EventData) -> bool:
        return False


class MultipleScalarTransferSpeedShapeLinkPlugin2(ShapeLinkPlugin):
    def choose_features(self):
        user_feats = ['area_cvx', 'area_msd', 'area_ratio', 'area_um',
                      'aspect', 'bright_avg', 'bright_sd', 'circ',
                      'deform', 'pos_x', 'pos_y', 'size_x', 'size_y',
                      'tilt', 'time', 'volume']
        return user_feats

    def handle_event(self, event_data: EventData) -> bool:
        return False


class SingleImageTransferSpeedShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        return ["image"]

    def handle_event(self, event_data: EventData) -> bool:
        return False


class MultipleImageTransferSpeedShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        user_feats = ["image", "mask", "contour"]
        return user_feats

    def handle_event(self, event_data: EventData) -> bool:
        return False


class AllAvailableFeaturesTransferSpeedShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        return list()

    def handle_event(self, event_data: EventData) -> bool:
        return False


def test_feature_transfer_speed_all_available_features():
    """Transfer all available dclab (innate) features"""
    run_plugin_feature_transfer(
        AllAvailableFeaturesTransferSpeedShapeLinkPlugin)


def test_feature_transfer_speed_single_scalar():
    """Transfer a single scalar feature

    Notes
    -----
    Speed of tests (kernprof) with Eoghan's laptop on different battery options
    each value is per hit (average) not including the first transfer.
    HP :  0.52 ms
    Cst : 0.79 ms
    Bal : 2.83 ms
    """
    run_plugin_feature_transfer(SingleScalarTransferSpeedShapeLinkPlugin)


def test_feature_transfer_speed_multiple_scalar():
    """Transfer multiple (five) scalar features"""
    run_plugin_feature_transfer(MultipleScalarTransferSpeedShapeLinkPlugin)


def test_feature_transfer_speed_multiple_scalar_2():
    """Transfer multiple (sixteen) dclab scalar features

    Notes
    -----
    Speed of tests (kernprof) with Eoghan's laptop on different battery options
    each value is per hit (average) not including the first transfer.
    HP :  4.13 ms
    Cst : 5.85 ms
    Bal : 19.27 ms
    """
    run_plugin_feature_transfer(MultipleScalarTransferSpeedShapeLinkPlugin2)


def test_feature_transfer_speed_single_image():
    """Transfer a single image feature

    Notes
    -----
    Speed of tests (kernprof) with Eoghan's laptop on different battery options
    each value is per hit (average) not including the first transfer.
    HP :  3.39 ms
    Cst : 4.99 ms
    Bal : 14.56 ms
    """
    run_plugin_feature_transfer(SingleImageTransferSpeedShapeLinkPlugin)


def test_feature_transfer_speed_multiple_image():
    """Transfer image features: "image", "mask", "contour"

    Notes
    -----
    Speed of tests (kernprof) with Eoghan's laptop on different battery options
    each value is per hit (average) not including the first transfer.
    These values are for "image" and "mask"
    HP :  5.03 ms
    Cst : 7.08 ms
    Bal : 20.99 ms
    """
    run_plugin_feature_transfer(MultipleImageTransferSpeedShapeLinkPlugin)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
