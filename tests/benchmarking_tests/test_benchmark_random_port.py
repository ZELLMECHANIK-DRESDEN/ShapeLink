
from tests import test_random_port


def test_benchmark_simulator_random_port(benchmark):
    benchmark.pedantic(test_random_port.test_run_plugin_with_random_port,
                       rounds=5, iterations=1)
