
# General tools for viewing benchmark statistics

import pathlib
from glob import glob
import json
import matplotlib.pyplot as plt
import pandas as pd


this_dir = pathlib.Path(__file__).parent
bm_data_dir = this_dir / "../../.benchmarks*/**/*.json"


def _get_benchmark_paths():
    data_dirs = glob(str(bm_data_dir), recursive=True)
    local_paths, ghactions_paths = [], []
    for path_name in data_dirs:
        if "github" in path_name:
            ghactions_paths.append(path_name)
        else:
            local_paths.append(path_name)
    return local_paths, ghactions_paths


def parse_benchmark_json(json_paths, stat='median', verbose=False):
    """Get the value of a stat for each benchmark in ms (millisecond)"""
    stat_data = {}
    for json_path in json_paths:
        json_path_dir = pathlib.Path(json_path)
        with open(json_path, "r") as json_file:
            json_content = json.load(json_file)
            n_test_dict = {}
            for n_test in json_content["benchmarks"]:
                # divide by 49 because our tests loop 49 times
                per_hit = n_test["stats"][stat] / 49 * 1000
                n_test_name = n_test['name']
                if verbose:
                    print(f"{json_path_dir.name}::{n_test_name} : "
                          f"{per_hit:.3f} ms")
                n_test_dict[n_test_name[25:]] = per_hit
        stat_data[json_path.split('\\')[-1]] = n_test_dict
    return stat_data


def plot_benchmark_statistics(local=True, stat='median', verbose=True):
    """Visualise the json benchmark statistics"""
    local_paths, ghactions_paths = _get_benchmark_paths()
    if local:
        json_paths = local_paths
        save_name = "local"
    else:
        json_paths = ghactions_paths
        save_name = "gh-actions"
    stat_data = parse_benchmark_json(json_paths, stat, verbose=verbose)
    df = pd.DataFrame.from_dict(stat_data)
    df.plot(figsize=(15, 9), kind='bar', rot=15, fontsize=16)
    plt.ylabel("Transfer Speed per hit (ms)", fontsize=24)
    plt.legend(fontsize=16)
    plt.savefig(f"{this_dir.resolve()}/"
                f"benchmark_comparison_{save_name}_{stat}.png")


if __name__ == "__main__":
    # Run plotting of statistics
    plot_benchmark_statistics()
    plot_benchmark_statistics(local=False)
    plt.show()
