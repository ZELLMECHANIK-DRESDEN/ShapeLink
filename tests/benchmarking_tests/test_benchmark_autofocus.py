
from tests import test_autofocus as af


def test_benchmark_simulator_autofocus_coarse(benchmark):
    """Benchmark `test_feature_transfer_speed_single_scalar`"""
    benchmark.pedantic(af.test_autofocus_fake_hologram_coarse,
                       rounds=5, iterations=1)


def test_benchmark_simulator_autofocus_no_coarse(benchmark):
    """Benchmark `test_feature_transfer_speed_single_scalar`"""
    benchmark.pedantic(af.test_autofocus_fake_hologram_no_coarse,
                       rounds=5, iterations=1)
