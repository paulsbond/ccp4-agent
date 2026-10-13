import argparse
from pathlib import Path

from . import batches, contents, install


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
    uniprot_parser = commands.add_parser(
        "uniprot", help="Show a UniProt sequence and what changes it in a crystal"
    )
    uniprot_parser.add_argument("accession", help="UniProt accession, e.g. P00698")
    uniprot_parser.add_argument(
        "--construct", type=Path, help="FASTA or PIR file to compare with UniProt"
    )
    similar_parser = commands.add_parser(
        "similar", help="Find PDB entries similar to each sequence in a file"
    )
    similar_parser.add_argument("sequences", type=Path, help="FASTA or PIR file")
    similar_parser.add_argument(
        "--rows", type=int, default=10, help="Entries to list for each sequence"
    )
    model_parser = commands.add_parser(
        "model", help="Show the cell and sequences (as FASTA) of a coordinate file"
    )
    model_parser.add_argument(
        "model", type=Path, help="PDB or mmCIF file, or a PDB ID to download"
    )
    model_parser.add_argument(
        "--construct", type=Path, help="FASTA or PIR file to compare with the model"
    )
    args = parser.parse_args()

    if args.command == "install":
        install.install()
    elif args.command == "uninstall":
        install.uninstall()
    elif args.command == "batches":
        batches.summarise(args.mtz, args.ranges)
    elif args.command == "uniprot":
        contents.uniprot(args.accession, args.construct)
    elif args.command == "similar":
        contents.similar(args.sequences, args.rows)
    elif args.command == "model":
        contents.model(args.model, args.construct)


if __name__ == "__main__":
    main()
