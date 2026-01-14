import subprocess, json, os
from uc_explore import run_experiment

def run_sweep():
    params = [
        {"n":4, "max":None, "out":"uc_n4.csv"},
        {"n":5, "max":200, "out":"uc_n5_sample.csv"},
    ]
    for p in params:
        print("Running n=", p["n"])
        run_experiment(p["n"], max_families=p["max"], output_csv=p["out"])
        print("Finished", p["out"])

if __name__ == "__main__":
    run_sweep()
