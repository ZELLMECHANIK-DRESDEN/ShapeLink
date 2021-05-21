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
                                ["deform", "area_um"],
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
        user_feats = ['area_cvx', 'area_msd', 'area_ratio', 'area_um',
                      'aspect', 'bright_avg', 'bright_sd', 'circ', 'deform',
                      'pos_x', 'pos_y', 'size_x', 'size_y',
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
        user_feats = ["image", "mask"]
        return user_feats

    def handle_event(self, event_data: EventData) -> bool:
        return False


@profile
def test_feature_transfer_speed_single_scalar():
    run_plugin_feature_transfer(SingleScalarTransferSpeedShapeLinkPlugin)


# def test_feature_transfer_speed_multiple_scalar():
#     run_plugin_feature_transfer(MultipleScalarTransferSpeedShapeLinkPlugin)
#
#
# def test_feature_transfer_speed_single_image():
#     run_plugin_feature_transfer(SingleImageTransferSpeedShapeLinkPlugin)
#
#
# def test_feature_transfer_speed_multiple_image():
#     run_plugin_feature_transfer(MultipleImageTransferSpeedShapeLinkPlugin)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
