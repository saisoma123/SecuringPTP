#!/usr/bin/env python3
import sys
import re
import matplotlib.pyplot as plt

MAX_OFFSETS = 300  # number of offset samples to use per run

OFFSET_REGEX = re.compile(r"master offset\s+(-?\d+)")


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


def main():
    num_logs = len(sys.argv) - 1
    if num_logs <= 0 or num_logs % 3 != 0:
        print(
            f"Usage: {sys.argv[0]} "
            "r1_log1 r1_log2 r1_log3 "
            "[r2_log1 r2_log2 r2_log3 ...]"
        )
        print("  (Number of log files must be a positive multiple of 3.)")
        sys.exit(1)

    num_runs = num_logs // 3
    paths = sys.argv[1:]  

    runs = []

    labels = ["Most Recently Used policy", "Random policy"]

    for i in range(num_runs):
        run_paths = paths[i * 3 : (i + 1) * 3]
        runs.append((labels[i], run_paths))

    all_avg_offsets = []
    lengths = []

    for label, run_paths in runs:
        avg_offsets = average_run_offsets(run_paths, MAX_OFFSETS)
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
        ms_offsets = [v / 1_000_000.0 for v in offsets[:common_len]]
        plt.plot(x, ms_offsets, label=label)

    plt.xlabel("Time (s)")
    plt.ylabel("Servo Offset (ms)")
    plt.title("PTP Servo Offset under Incremental Skew Attack")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out_name = "ptp_rand_passive_servo.png"
    plt.savefig(out_name, dpi=150)
    print(f"Saved plot → {out_name}")


if __name__ == "__main__":
    main()
