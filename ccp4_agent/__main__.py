import argparse
from pathlib import Path

from . import batches, install


def main() -> None:
    parser = argparse.ArgumentParser(prog="ccp4-agent", description="CCP4 AI Agent")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("install", help="Add the ccp4 skill")
    commands.add_parser("uninstall", help="Remove the ccp4 skill")
    batches_parser = commands.add_parser(
        "batches", help="Analyse per-image data quality"
    )
    batches_parser.add_argument("mtz", type=Path, help="Unmerged, scaled MTZ file")
    batches_parser.add_argument(
        "--ranges", type=int, default=10, help="Number of image ranges"
    )
    args = parser.parse_args()

    if args.command == "install":
        install.install()
    elif args.command == "uninstall":
        install.uninstall()
    elif args.command == "batches":
        batches.summarise(args.mtz, args.ranges)


if __name__ == "__main__":
    main()
