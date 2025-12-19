#!/usr/bin/env python3
import json
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Measured CPU averaged baseline
BASELINE_AVG = {
    "0": 31.22,
    "1": 33.12,
    "2": 31.28,
    "3": 32.08,
}


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

# This averages the jitterdebugger data across 3 runs 
def average_cpu_avgs(json_paths):
    sums = {}    # cpu_id -> sum of avg
    counts = {}  # cpu_id -> number of samples

    for path in json_paths:
        results = load_json(path)
        res_cpus = results.get("cpu", {})

        for cpu_id, cpu_info in res_cpus.items():
            if "avg" not in cpu_info:
                continue
            try:
                val = float(cpu_info["avg"])
            except (TypeError, ValueError):
                continue

            sums[cpu_id] = sums.get(cpu_id, 0.0) + val
            counts[cpu_id] = counts.get(cpu_id, 0) + 1

    averages = {}
    for cpu_id in sums:
        if counts[cpu_id] > 0:
            averages[cpu_id] = sums[cpu_id] / counts[cpu_id]

    return averages

# This averages the PTP baseline and the watchdog policies and measures the inferred CPU overhead
def main():
    if len(sys.argv) != 1 + 6:
        print(f"Usage: {sys.argv[0]} N1.json N2.json N3.json W1.json W2.json W3.json")
        sys.exit(1)

    normal_paths = sys.argv[1:4]
    watchdog_paths = sys.argv[4:7]

    normal_avgs = average_cpu_avgs(normal_paths)
    watchdog_avgs = average_cpu_avgs(watchdog_paths)

    cpu_labels = []
    normal_overhead_pct = []
    watchdog_overhead_pct = []

    print("Using system baseline (no-PTP) averages:", BASELINE_AVG)

    for cpu_id in sorted(BASELINE_AVG.keys(), key=int):
        base_avg = float(BASELINE_AVG[cpu_id])

        if cpu_id not in normal_avgs:
            print(f"Warning: CPU {cpu_id} missing from NORMAL averages, skipping.")
            continue
        if cpu_id not in watchdog_avgs:
            print(f"Warning: CPU {cpu_id} missing from WATCHDOG averages, skipping.")
            continue

        n_avg = normal_avgs[cpu_id]
        w_avg = watchdog_avgs[cpu_id]

        n_pct = (n_avg - base_avg) / base_avg * 100.0
        w_pct = (w_avg - base_avg) / base_avg * 100.0

        cpu_labels.append(f"CPU {cpu_id}")
        normal_overhead_pct.append(n_pct)
        watchdog_overhead_pct.append(w_pct)

    print("\nPercentage overhead per CPU (avg latency) vs system baseline:")
    print("CPU    Normal PTP     PTP + Watchdog")
    print("--------------------------------------")
    for label, n_pct, w_pct in zip(cpu_labels, normal_overhead_pct, watchdog_overhead_pct):
        n_sign = "+" if n_pct >= 0 else ""
        w_sign = "+" if w_pct >= 0 else ""
        print(f"{label:5s} {n_sign}{n_pct:7.2f}%      {w_sign}{w_pct:7.2f}%")

    x = np.arange(len(cpu_labels))  
    width = 0.35                    

    plt.figure(figsize=(8, 4))
    plt.bar(x - width/2, normal_overhead_pct, width, label="Normal PTP")
    plt.bar(x + width/2, watchdog_overhead_pct, width, label="Watchdog")

    plt.axhline(0, linewidth=1)
    plt.xticks(x, cpu_labels)
    plt.xlabel("CPU Core")
    plt.ylabel("Overhead vs System Baseline (%)")
    plt.title("PTP Baseline Run: Overhead per CPU Core\nNormal vs Watchdog")
    plt.legend()
    plt.tight_layout()

    out_name = "ptp_no_attack_overhead.png"
    plt.savefig(out_name, dpi=150)
    print(f"\nSaved plot → {out_name}")


if __name__ == "__main__":
    main()
