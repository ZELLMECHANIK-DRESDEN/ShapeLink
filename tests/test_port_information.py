import pathlib

import random
import time
import zmq

from shapelink import ShapeLinkPlugin
from shapelink.shapelink_plugin import EventData

data_dir = pathlib.Path(__file__).parent / "data"


class ExampleShapeLinkPlugin(ShapeLinkPlugin):
    def choose_features(self):
        return list()

    def handle_event(self, event_data: EventData) -> bool:
        return False


def test_default_port_and_IP(random_port=False):
    # Because the CI runs four systems simultaneously, we need to wait for
    # this port to be available before connecting.
    for i in range(10):
        try:
            p = ExampleShapeLinkPlugin(random_port=random_port)
            assert p.port_address == "6666"
            assert p.ip_address == "tcp://*"
        except zmq.error.ZMQError:
            time.sleep(random.randint(1, 5))
        else:
            break


def test_random_IP(random_port=True):
    # setup plugin
    p = ExampleShapeLinkPlugin(random_port=random_port)
    assert p.ip_address == "tcp://*"
    assert isinstance(p.port_address, int)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
