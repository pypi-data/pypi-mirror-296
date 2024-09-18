"""
Simple entrypoint
"""

import argparse as ap
from pathlib import Path

from lmsi.core import core

parser = ap.ArgumentParser(description="Create a webpage from a set of plots.")

parser.add_argument(
    "--files",
    type=Path,
    nargs="+",
    help="Filenames of the plots to include in the webpage.",
)

parser.add_argument(
    "--config",
    type=Path,
    help="The configuration file to use.",
    default=None,
)

parser.add_argument(
    "--output",
    type=Path,
    help="The output HTML file.",
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Print debug information.",
    default=False,
)

args = parser.parse_args()


def main():
    if args.debug:
        print(args)

    core(args.files, args.config, args.output)
