import pathlib
import threading

from shapelink import shapein_simulator
from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"


class ExampleShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        return list()

    def handle_event(self, event_data: EventData) -> bool:
        return False


def test_run_plugin_with_multiple_clients():
    # create new thread for simulator
    th1 = threading.Thread(target=shapein_simulator.start_simulator,
                           args=(str(data_dir / "calibration_beads_47.rtdc"),
                                 ["deform", "area_um"],
                                 "tcp://localhost:6666", 0)
                           )
    th2 = threading.Thread(target=shapein_simulator.start_simulator,
                           args=(str(data_dir / "calibration_beads_47.rtdc"),
                                 ["deform", "area_um"],
                                 "tcp://localhost:6666", 0)
                           )
    # setup plugin
    p = ExampleShapeLinkPlugin(bind_to='tcp://*:6666')
    # start simulator
    th1.start()
    th2.start()
    # start plugin
    for ii in range(49):
        p.handle_messages()
    th1.join()
    th2.join()
