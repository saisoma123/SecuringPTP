#!/usr/bin/env python3
import sys
import re
import matplotlib.pyplot as plt

MAX_OFFSETS = 300  

OFFSET_REGEX = re.compile(r"master offset\s+(-?\d+)")

# Extracts the offsets from the PTP4L logs in nanoseconds
def extract_offsets(path, max_count=MAX_OFFSETS):
    offsets = []
    with open(path, "r") as f:
        for line in f:
            m = OFFSET_REGEX.search(line)
            if m:
                val = int(m.group(1))
                offsets.append(val)
                if len(offsets) >= max_count:
                    break
    return offsets

# Averages the extracted offsets from 3 runs
def average_run_offsets(log_paths, max_count=MAX_OFFSETS):

    if len(log_paths) != 3:
        raise ValueError("Each run must have exactly 3 log files.")

    all_series = [extract_offsets(p, max_count) for p in log_paths]

    min_len = min(len(s) for s in all_series)
    if min_len == 0:
        return []

    n = min(max_count, min_len)

    avg_offsets = []
    for i in range(n):
        s = all_series[0][i] + all_series[1][i] + all_series[2][i]
        avg_offsets.append(s / 3.0)
    return avg_offsets

# Plots our averaged out runs per policy/baseline
def main():

    if len(sys.argv) != 1 + 12:
        print(
            f"Usage: {sys.argv[0]} "
            "run1_log1 run1_log2 run1_log3 "
            "run2_log1 run2_log2 run2_log3 "
            "run3_log1 run3_log2 run3_log3 "
            "run4_log1 run4_log2 run4_log3"
        )
        sys.exit(1)

    run1_paths = sys.argv[1:4]
    run2_paths = sys.argv[4:7]
    run3_paths = sys.argv[7:10]
    run4_paths = sys.argv[10:13]

    runs = [
        ("Normal PTP", run1_paths),
        ("Watchdog", run2_paths),
        ("Most Recently Used policy", run3_paths),
        ("Random Policy", run4_paths),
    ]

    all_avg_offsets = []
    lengths = []

    for label, paths in runs:
        avg_offsets = average_run_offsets(paths, MAX_OFFSETS)
        all_avg_offsets.append((label, avg_offsets))
        lengths.append(len(avg_offsets))
        print(f"{label}: using {len(avg_offsets)} averaged offsets")

    if any(len(o) == 0 for _, o in all_avg_offsets):
        print("Error: at least one run has zero extracted offsets. Check the logs / regex.")
        sys.exit(1)

    common_len = min(lengths)
    print(f"Plotting first {common_len} averaged offsets per run")

    x = list(range(common_len))  

    plt.figure(figsize=(10, 5))

    for label, offsets in all_avg_offsets:
        plt.plot(x, offsets[:common_len], label=label)

    plt.xlabel("Time (s)")
    plt.ylabel("Servo Offset (ns)")
    plt.title("PTP Baseline Servo Offset over 5 minutes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out_name = "ptp_servo_baseline.png"
    plt.savefig(out_name, dpi=150)
    print(f"Saved plot → {out_name}")


if __name__ == "__main__":
    main()
