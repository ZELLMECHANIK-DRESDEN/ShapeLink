
from tests import test_autofocus as af


def test_benchmark_simulator_autofocus(benchmark):
    """Benchmark `test_feature_transfer_speed_single_scalar`"""
    benchmark.pedantic(af.test_run_plugin_with_user_defined_trace_features,
                       rounds=5, iterations=1)
