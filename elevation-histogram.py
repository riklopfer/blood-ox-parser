#! /usr/bin/env python3
"""
Convert kPa to elevation above sea level in meters. Make a histogram of blood ox vs elevation. 
"""
import argparse
import csv
import logging
import os
from collections import defaultdict
from math import sqrt
from typing import Dict

logger = logging.getLogger(os.path.basename(__file__))


def to_elevation_meters(kpa: float) -> float:
    """
    https://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html
    p = 101325 (1 - 2.25577e-5*h)^ 5.25588
    p / 101325 = (1 - 2.25577e-5*h)^ 5.25588
    (p / 101325) ^ (1 / 5.25588) = 1 - 2.25577e-5 * h
    1 - (p / 101325) ^ (1 / 5.25588) = 2.25577e-5 * h
    (1 - (p / 101325) ^ (1 / 5.25588)) / 2.25577e-5 = h
    """
    p = kpa * 1000
    return (1 - pow(p / 101325, 1 / 5.25588)) / 2.25577e-5


def get_hist_bin(elevation: float) -> float:
    return (elevation // 10) * 10


def hist_to_str(histogram: Dict) -> str:
    s = ""
    for elevation in sorted(histogram.keys()):
        values = histogram[elevation]
        mean = sum(values, 0) / len(values)
        stdv = sqrt(sum(((value - mean) ** 2 for value in values)) / len(values))
        s += f"{elevation} :: n={len(values)} μ={mean:.5f} σ={stdv:.5f}\n"
    return s


def main(args: argparse.Namespace):
    histogram = defaultdict(list)
    with open(args.bloodox, "r") as ifp:
        reader = csv.reader(ifp)
        # skip header
        _ = next(reader)
        for tstmp, bloodox, kpa in reader:
            bloodox, kpa = map(float, (bloodox, kpa))
            elevation = to_elevation_meters(kpa)
            histogram[get_hist_bin(elevation)].append(bloodox)

    hist_str = hist_to_str(histogram)
    print(hist_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bloodox", help="Extracted blood oxygen CSV", type=str, default="bloodox.csv"
    )

    main(parser.parse_args())
