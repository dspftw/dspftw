#!/usr/bin/env python3
"""Benchmark memory usage of dspftw.signal_correlation."""

import argparse
import json
import os
import resource
import subprocess
import sys
import time

import numpy as np


def rss_bytes():
    """Return current resident memory in bytes."""
    import psutil
    return psutil.Process().memory_info().rss


def peak_rss_bytes():
    """Return peak resident memory in bytes."""
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return peak
    return peak * 1024


def worker(args):
    from dspftw.signal_correlation import signal_correlation

    rng = np.random.default_rng(20261105)

    signal = np.empty(args.size, dtype=np.complex64)
    chunk = 1_000_000

    for start in range(0, args.size, chunk):
        stop = min(start + chunk, args.size)
        signal.real[start:stop] = rng.standard_normal(
            stop - start, dtype=np.float32
        )
        signal.imag[start:stop] = rng.standard_normal(
            stop - start, dtype=np.float32
        )

    pattern = np.empty(args.pattern, dtype=np.complex64)
    pattern.real[:] = rng.standard_normal(
        args.pattern, dtype=np.float32
    )
    pattern.imag[:] = rng.standard_normal(
        args.pattern, dtype=np.float32
    )

    before = rss_bytes()
    started = time.perf_counter()

    result = signal_correlation(
        signal,
        pattern,
        norm=args.worker_norm,
        mode=args.mode,
        method=args.method,
        block=args.block,
    )

    elapsed = time.perf_counter() - started
    peak = peak_rss_bytes()

    checksum = float(
        np.abs(result[::max(1, len(result) // 1000)]).sum()
    )

    report = {
        "samples": args.size,
        "norm": args.worker_norm,
        "seconds": round(elapsed, 3),
        "input_mib": round(signal.nbytes / 2**20, 2),
        "output_mib": round(result.nbytes / 2**20, 2),
        "additional_peak_mib": round(
            max(0, peak - before) / 2**20, 2
        ),
        "additional_multiple": round(
            max(0, peak - before) / signal.nbytes, 2
        ),
        "checksum": round(checksum, 6),
    }

    print(json.dumps(report))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[1_000_000, 10_000_000],
    )
    parser.add_argument("--pattern", type=int, default=1024)
    parser.add_argument("--block", type=int, default=0)
    parser.add_argument(
        "--norm",
        choices=["both", "true", "false"],
        default="both",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "same", "valid"],
        default="full",
    )
    parser.add_argument(
        "--method",
        choices=["auto", "fft", "direct"],
        default="auto",
    )
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--worker-norm", default="false")
    args = parser.parse_args()

    if args.worker:
        args.size = args.sizes[0]
        args.worker_norm = args.worker_norm == "true"
        worker(args)
        return

    print(
        "Samples       Norm     Seconds    Extra MiB    Multiple"
    )
    print("-" * 60)

    for size in args.sizes:
        norms = (
            ["false", "true"]
            if args.norm == "both"
            else [args.norm]
        )

        for norm in norms:
            command = [
                sys.executable,
                os.path.abspath(__file__),
                "--worker",
                "--sizes",
                str(size),
                "--pattern",
                str(args.pattern),
                "--block",
                str(args.block),
                "--mode",
                args.mode,
                "--method",
                args.method,
                "--worker-norm",
                norm,
            ]

            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

            data = json.loads(completed.stdout.strip())

            print(
                f"{size:<13}"
                f"{norm:<9}"
                f"{data['seconds']:>8.3f}"
                f"{data['additional_peak_mib']:>13.2f}"
                f"{data['additional_multiple']:>12.2f}x"
            )


if __name__ == "__main__":
    main()
