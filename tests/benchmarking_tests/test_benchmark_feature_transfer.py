
from tests import test_feature_transfer_speed as fts


def test_benchmark_simulator_fts_scalar_single(benchmark):
    """Benchmark `test_feature_transfer_speed_single_scalar`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_single_scalar,
                       rounds=5, iterations=1)


def test_benchmark_simulator_fts_scalar_multiple(benchmark):
    """Benchmark `test_feature_transfer_speed_multiple_scalar`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_multiple_scalar,
                       rounds=5, iterations=1)


def test_benchmark_simulator_fts_scalar_multiple_2(benchmark):
    """Benchmark `test_feature_transfer_speed_multiple_scalar_2`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_multiple_scalar_2,
                       rounds=5, iterations=1)


def test_benchmark_simulator_fts_image_single(benchmark):
    """Benchmark `test_feature_transfer_speed_single_image`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_single_image,
                       rounds=5, iterations=1)


def test_benchmark_simulator_fts_image_multiple(benchmark):
    """Benchmark `test_feature_transfer_speed_multiple_image`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_multiple_image,
                       rounds=5, iterations=1)


def test_benchmark_simulator_fts_all_available_features(benchmark):
    """Benchmark `test_feature_transfer_speed_all_available_features`"""
    benchmark.pedantic(fts.test_feature_transfer_speed_all_available_features,
                       rounds=5, iterations=1)
