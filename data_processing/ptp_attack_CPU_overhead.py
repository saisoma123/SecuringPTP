#!/usr/bin/env python3
import json
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

BASELINE_AVG = {
    "0": 31.22,
    "1": 33.12,
    "2": 31.28,
    "3": 32.08,
}


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def average_cpu_avgs(json_paths):
    sums = {}    
    counts = {} 

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


def main():
    if len(sys.argv) != 1 + 12:
        print(
            f"Usage: {sys.argv[0]} "
            "N1.json N2.json N3.json "
            "A1.json A2.json A3.json "
            "B1.json B2.json B3.json "
            "C1.json C2.json C3.json"
        )
        sys.exit(1)

    normal_paths   = sys.argv[1:4]
    policyA_paths  = sys.argv[4:7]
    policyB_paths  = sys.argv[7:10]
    policyC_paths  = sys.argv[10:13]

    normal_avgs  = average_cpu_avgs(normal_paths)
    policyA_avgs = average_cpu_avgs(policyA_paths)
    policyB_avgs = average_cpu_avgs(policyB_paths)
    policyC_avgs = average_cpu_avgs(policyC_paths)

    cpu_labels = []
    normal_overhead_pct  = []
    policyA_overhead_pct = []
    policyB_overhead_pct = []
    policyC_overhead_pct = []

    print("Using system baseline (no-PTP) averages:", BASELINE_AVG)

    for cpu_id in sorted(BASELINE_AVG.keys(), key=int):
        base_avg = float(BASELINE_AVG[cpu_id])

        missing = []
        if cpu_id not in normal_avgs:
            missing.append("Normal")
        if cpu_id not in policyA_avgs:
            missing.append("Policy A")
        if cpu_id not in policyB_avgs:
            missing.append("Policy B")
        if cpu_id not in policyC_avgs:
            missing.append("Policy C")

        if missing:
            print(
                f"Warning: CPU {cpu_id} missing from {', '.join(missing)} averages, "
                "skipping this CPU."
            )
            continue

        n_avg = normal_avgs[cpu_id]
        a_avg = policyA_avgs[cpu_id]
        b_avg = policyB_avgs[cpu_id]
        c_avg = policyC_avgs[cpu_id]

        n_pct = (n_avg - base_avg) / base_avg * 100.0
        a_pct = (a_avg - base_avg) / base_avg * 100.0
        b_pct = (b_avg - base_avg) / base_avg * 100.0
        c_pct = (c_avg - base_avg) / base_avg * 100.0

        cpu_labels.append(f"CPU {cpu_id}")
        normal_overhead_pct.append(n_pct)
        policyA_overhead_pct.append(a_pct)
        policyB_overhead_pct.append(b_pct)
        policyC_overhead_pct.append(c_pct)

    if not cpu_labels:
        print("No CPUs to plot after filtering; check your inputs.")
        sys.exit(1)

    print("\nPercentage overhead per CPU (avg latency) vs system baseline:")
    print("CPU    Normal     Policy A    Policy B    Policy C")
    print("---------------------------------------------------")
    for label, n, a, b, c in zip(
        cpu_labels,
        normal_overhead_pct,
        policyA_overhead_pct,
        policyB_overhead_pct,
        policyC_overhead_pct,
    ):
        def fmt(p):
            sign = "+" if p >= 0 else ""
            return f"{sign}{p:7.2f}%"

        print(f"{label:5s} {fmt(n)}   {fmt(a)}   {fmt(b)}   {fmt(c)}")

    # --- Plot grouped bar chart: 4 bars per CPU ---
    x = np.arange(len(cpu_labels))  # positions for CPU cores
    width = 0.18                    # bar width

    plt.figure(figsize=(9, 4))
    plt.bar(x - 1.5 * width, normal_overhead_pct,  width, label="Normal PTP")
    plt.bar(x - 0.5 * width, policyA_overhead_pct, width, label="Watchdog Policy A")
    plt.bar(x + 0.5 * width, policyB_overhead_pct, width, label="Watchdog Policy B")
    plt.bar(x + 1.5 * width, policyC_overhead_pct, width, label="Watchdog Policy C")

    plt.axhline(0, linewidth=1)
    plt.xticks(x, cpu_labels)
    plt.xlabel("CPU Core")
    plt.ylabel("Overhead vs System Baseline (%)")
    plt.title("Random Disturbance Attack Run: Overhead per CPU Core\nNormal PTP vs Watchdog Policies A/B/C")
    plt.legend()
    plt.tight_layout()

    out_name = "random_disturbance_overhead_policies.png"
    plt.savefig(out_name, dpi=150)
    print(f"\nSaved plot → {out_name}")


if __name__ == "__main__":
    main()
