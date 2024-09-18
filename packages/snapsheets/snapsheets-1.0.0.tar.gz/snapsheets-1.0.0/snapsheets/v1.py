"""Snapsheets (v1)

Wget Google spreadsheet

usage: snapsheets-next [-h] [--config config | --url url] [-o filename] [-d description] [-t format] [-v] [--skip]

snapsheets

Optional arguments:
    -h, --help       show this help message and exit
    --config config  set config file or directory.
    --url url        set URL of Google spreadsheet.
    -o filename      set output filename.
    -d description   set description of a spreadsheet.
    -t format        set datetime prefix for backup filename.
    -v, --version    show program's version number and exit
"""

import argparse
import sys

from loguru import logger

from snapsheets import __version__
from snapsheets.book import Book
from snapsheets.sheet import Sheet


def setup_parser() -> argparse.ArgumentParser:
    """Setup argument parser"""

    parser = argparse.ArgumentParser(description="snapsheets")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--config",
        metavar="config",
        default="config.toml",
        help="set config file or directory",
    )
    group.add_argument(
        "--url",
        metavar="url",
        help="set URL of Google spreadsheet",
    )

    parser.add_argument(
        "-o",
        metavar="filename",
        default="snapshot.csv",
        help="set output filename",
    )
    parser.add_argument(
        "-d",
        metavar="description",
        default="Add description here.",
        help="set description of a spreadsheet",
    )
    parser.add_argument(
        "-t",
        metavar="format",
        default="",
        help="set datetime prefix for backup filename",
    )
    parser.add_argument("--skip", action="store_true", help="skip file")
    parser.add_argument("--debug", action="store_true", help="show more messages")
    parser.add_argument("--version", action="version", version=f"{__version__}")

    return parser


def configure_logger(debug: bool) -> None:
    """Configure loguru logger"""

    logger.remove()

    if debug:
        fmt = (" | ").join(
            [
                "{time:YYYY-MM-DDTHH:mm:ss}",
                "<level>{level:8}</level>",
                "<cyan>{name}.{function}:{line}</cyan>",
                "<level>{message}</level>",
            ]
        )
        logger.add(sys.stderr, format=fmt, level="DEBUG")
    else:
        fmt = (" | ").join(
            [
                "{time:YYYY-MM-DDTHH:mm:ss}",
                "<level>{level:8}</level>",
                "<level>{message}</level>",
            ]
        )
        logger.add(sys.stderr, format=fmt, level="SUCCESS")


def process_url(args: argparse.Namespace) -> None:
    """Get snapshot using the provided URL."""
    sheet = Sheet(
        url=args.url,
        filename=args.o,
        description=args.d,
        datefmt=args.t,
        skip=args.skip,
    )
    sheet.snapshot()


def process_config(args: argparse.Namespace) -> None:
    """Get snapshot using configuration file"""
    book = Book(args.config)
    book.snapshots()


def cli() -> None:
    """
    Command Line Interface for snapsheets.
    """

    parser = setup_parser()
    args = parser.parse_args()

    configure_logger(args.debug)

    logger.info("Running V1 version")

    if args.url:
        process_url(args)
    else:
        process_config(args)


if __name__ == "__main__":
    cli()
