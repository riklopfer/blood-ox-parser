#! /usr/bin/env python3
import argparse
import csv
import dataclasses
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, TextIO, Dict

logger = logging.getLogger(os.path.basename(__file__))


@dataclass()
class Measurement:
    date: str
    bloodOxygen: float
    pressure: float


ATTR_PAT = re.compile(r'([a-zA-Z]+)="([^"]+)"')


def get_attr_values(xml_elem: str) -> Dict:
    return dict(match.groups() for match in ATTR_PAT.finditer(xml_elem))


def measurements(ifp: TextIO) -> Iterator[Measurement]:
    box, kpa, date = None, None, None

    for line in ifp:
        line = line.strip()
        if line.startswith('<Record type="HKQuantityTypeIdentifierOxygenSaturation"'):
            attr_values = get_attr_values(xml_elem=line)
            box = float(attr_values["value"])
            date = attr_values["creationDate"]

            # find pressure
            while True:
                line = next(ifp).strip()
                if line.startswith("<MetadataEntry"):
                    attr_values = get_attr_values(xml_elem=line)
                    if attr_values["key"] == "HKMetadataKeyBarometricPressure":
                        # 23.4323 kPa <- strip off the kPa_
                        kpa = float(attr_values["value"][:-4])
                    else:
                        logger.warning(
                            "Unknown key '%s' in %s", attr_values["key"], line
                        )
                else:
                    break

            if not kpa:
                logger.warning("No pressure for %s", line)

            yield Measurement(date=date, bloodOxygen=box, pressure=kpa)


def main(args: argparse.Namespace):
    with open(Path(args.export).expanduser(), "r", encoding="utf8") as ifp:
        with open(Path(args.output), "w", encoding="utf8") as ofp:
            writer = csv.writer(ofp)
            writer.writerow(("Time", "BloodOx", "AtmPressure"))
            for measurement in measurements(ifp):
                writer.writerow(dataclasses.astuple(measurement))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--export",
        help="path to health data export",
        type=str,
        default="~/Downloads/apple_health_export/export.xml",
    )
    parser.add_argument(
        "--output", help="Write CSV to this file", type=str, default="bloodox.csv"
    )

    main(parser.parse_args())
