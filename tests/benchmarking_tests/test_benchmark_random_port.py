
from tests import test_random_port
from tests import test_feature_transfer_speed as fts


def test_benchmark_simulator_random_port(benchmark):
    benchmark(test_random_port.test_run_plugin_with_random_port,
              random_port=True)


def test_benchmark_simulator_fts_single_scalar(benchmark):
    benchmark(fts.test_feature_transfer_speed_single_scalar)


def test_benchmark_simulator_fts_multiple_scalar(benchmark):
    benchmark(fts.test_feature_transfer_speed_multiple_scalar)


def test_benchmark_simulator_fts_single_image(benchmark):
    benchmark(fts.test_feature_transfer_speed_single_image)


def test_benchmark_simulator_fts_multiple_image(benchmark):
    benchmark(fts.test_feature_transfer_speed_multiple_image)
