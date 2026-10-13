import json
import re
import textwrap
import urllib.error
import urllib.request
from collections import Counter
from itertools import groupby
from pathlib import Path

import gemmi
import pandas as pd
from gemmi import EntityType

UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/{}.json"
SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
GRAPHQL_URL = "https://data.rcsb.org/graphql"
ENTRY_URL = "https://files.rcsb.org/download/{}.cif"
MIN_LENGTH = 10
END_BLOCK = 4
MIN_IDENTITY = 0.9

PROCESSING = [
    "Initiator methionine",
    "Signal",
    "Transit peptide",
    "Propeptide",
    "Chain",
    "Peptide",
]
MODIFICATIONS = ["Disulfide bond", "Glycosylation", "Modified residue", "Lipidation"]

ENTRY_QUERY = """
query($ids: [String!]!) {
  polymer_entities(entity_ids: $ids) {
    rcsb_id
    rcsb_polymer_entity_container_identifiers { auth_asym_ids }
    entry {
      exptl { method }
      rcsb_entry_info { resolution_combined }
      symmetry { space_group_name_H_M }
      cell { length_a length_b length_c angle_alpha angle_beta angle_gamma }
      struct { title }
      nonpolymer_entities { nonpolymer_comp { chem_comp { id } } }
    }
  }
}
"""


def _fetch(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}
    with urllib.request.urlopen(urllib.request.Request(url, data, headers)) as r:
        return json.loads(r.read() or b"{}")


def _range(feature: dict) -> str:
    start = feature["location"]["start"].get("value", "?")
    end = feature["location"]["end"].get("value", "?")
    return str(start) if start == end else f"{start}-{end}"


def _kind(column: tuple[str, str, int]) -> str:
    construct, reference, _ = column
    if reference == "-":
        return "inserted"
    if construct == "-":
        return "missing"
    return "same" if construct == reference else "mutation"


def _core(kinds: list[str]) -> tuple[int, int] | None:
    blocks = []  # [first, last] column of each run of aligned residues
    for i, kind in enumerate(kinds):
        if kind in ("same", "mutation"):
            if blocks and blocks[-1][1] == i - 1:
                blocks[-1][1] = i
            else:
                blocks.append([i, i])
    # A few residues of a tag can align by chance beyond a gap, such as the
    # tag's Met with UniProt Met1, so leave short blocks at the ends out
    while len(blocks) > 1 and blocks[0][1] - blocks[0][0] + 1 < END_BLOCK:
        blocks.pop(0)
    while len(blocks) > 1 and blocks[-1][1] - blocks[-1][0] + 1 < END_BLOCK:
        blocks.pop()
    return (blocks[0][0], blocks[-1][1]) if blocks else None


def _differences(construct: str, reference: str, label: str) -> list[str]:
    result = gemmi.align_string_sequences(
        list(construct), list(reference), [], gemmi.AlignmentScoring()
    )
    query, _, target = result.formatted(construct, reference).splitlines()
    columns = []  # (construct residue, reference residue, reference number)
    number = 0
    for q, t in zip(query, target):
        number += t != "-"
        columns.append((q, t, number))
    core = _core([_kind(column) for column in columns])
    if core is None:
        return ["  No alignment: the sequences are unrelated."]
    first, last = core
    kinds = [_kind(column) for column in columns[first : last + 1]]
    aligned = kinds.count("same") + kinds.count("mutation")
    lines = [
        f"  Covers {label} {columns[first][2]}-{columns[last][2]}, "
        f"{kinds.count('same')} of {aligned} aligned residues identical"
    ]
    if kinds.count("same") < MIN_IDENTITY * aligned:
        lines.append("  Too different to list changes.")
        return lines
    if extra := "".join(q for q, _, _ in columns[:first] if q != "-"):
        lines.append(f"  Extra at the N-terminus: {extra}")
    for kind, group in groupby(columns[first : last + 1], key=_kind):
        run = list(group)
        if kind == "inserted":
            inserted = "".join(q for q, _, _ in run)
            lines.append(f"  Inserted after {label} {run[0][2]}: {inserted}")
        elif kind == "missing":
            missing = f"{run[0][2]}-{run[-1][2]}" if len(run) > 1 else run[0][2]
            lines.append(f"  Missing {label} {missing}")
        elif kind == "mutation":
            lines.extend(f"  Mutation {t}{n}{q}" for q, t, n in run)
    if extra := "".join(q for q, _, _ in columns[last + 1 :] if q != "-"):
        lines.append(f"  Extra at the C-terminus: {extra}")
    return lines


def uniprot(accession: str, construct: Path | None = None) -> None:
    try:
        entry = _fetch(UNIPROT_URL.format(accession))
    except urllib.error.URLError as error:
        print(f"Could not fetch UniProt entry {accession}: {error}")
        return
    names = entry.get("proteinDescription", {})
    name = names.get("recommendedName", names.get("submissionNames", [{}]))
    if isinstance(name, list):
        name = name[0]
    sequence = entry["sequence"]["value"]
    print(
        f"{entry['primaryAccession']}: {name.get('fullName', {}).get('value', '')}, "
        f"{entry.get('organism', {}).get('scientificName', '')}, "
        f"{entry.get('entryType', '')}, {len(sequence)} residues"
    )
    print(f">{entry['primaryAccession']}")
    print("\n".join(textwrap.wrap(sequence, 60)))

    features = entry.get("features", [])
    print("\nProcessing (residue numbers in the sequence above):")
    lines = [
        f"  {f['type']} {_range(f)} {f.get('description', '')}".rstrip()
        for f in features
        if f["type"] in PROCESSING
    ]
    print("\n".join(lines) if lines else "  none annotated")

    print("\nModifications:")
    lines = []
    for kind in MODIFICATIONS:
        found = [
            f"{_range(f)} {f.get('description', '').split(' (')[0]}".rstrip()
            for f in features
            if f["type"] == kind
        ]
        if found:
            lines.append(f"  {kind}: {'; '.join(dict.fromkeys(found))}")
    print("\n".join(lines) if lines else "  none annotated")

    print("\nBinding sites:")
    ligands: dict[str, list[str]] = {}
    for f in features:
        if f["type"] == "Binding site":
            ligand = f.get("ligand", {}).get("name", "unnamed ligand")
            ligands.setdefault(ligand, []).append(_range(f))
    lines = [f"  {ligand}: {', '.join(sites)}" for ligand, sites in ligands.items()]
    print("\n".join(lines) if lines else "  none annotated")

    comments = entry.get("comments", [])
    cofactors = [
        c["name"]
        for comment in comments
        if comment["commentType"] == "COFACTOR"
        for c in comment.get("cofactors", [])
    ]
    print(f"\nCofactors: {', '.join(cofactors) if cofactors else 'none annotated'}")
    subunit = [
        text["value"]
        for comment in comments
        if comment["commentType"] == "SUBUNIT"
        for text in comment.get("texts", [])
    ]
    subunit = textwrap.shorten(" ".join(subunit), 400) if subunit else "none annotated"
    print(f"Subunit: {subunit}")

    for name, construct_sequence in _read_sequences(construct) if construct else []:
        length = len(construct_sequence)
        print(f"\n{name.split()[0]} ({length} residues) against UniProt:")
        print("\n".join(_differences(construct_sequence, sequence, "UniProt")))


def _sequence_type(sequence: str) -> str:
    if set(sequence) <= set("ACGTN"):
        return "dna"
    if set(sequence) <= set("ACGUN"):
        return "rna"
    return "protein"


def _search(sequence: str, rows: int) -> list[dict]:
    query = {
        "query": {
            "type": "terminal",
            "service": "sequence",
            "parameters": {
                "evalue_cutoff": 0.1,
                "identity_cutoff": 0.25,
                "sequence_type": _sequence_type(sequence),
                "value": sequence,
            },
        },
        "return_type": "polymer_entity",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "score", "direction": "desc"}],
            "scoring_strategy": "sequence",
            "results_verbosity": "verbose",
        },
    }
    hits = []
    for result in _fetch(SEARCH_URL, query).get("result_set", []):
        match = result["services"][0]["nodes"][0]["match_context"][0]
        aligned = match["query_end"] - match["query_beg"] + 1
        hits.append(
            {
                "entity": result["identifier"],
                "identity": match["sequence_identity"],
                "coverage": round(aligned / match["query_length"], 2),
            }
        )
    return hits


def _describe(hits: list[dict]) -> pd.DataFrame:
    ids = [hit["entity"] for hit in hits]
    data = _fetch(GRAPHQL_URL, {"query": ENTRY_QUERY, "variables": {"ids": ids}})
    details = {}
    for entity in data["data"]["polymer_entities"]:
        entry = entity["entry"]
        cell = entry.get("cell") or {}
        resolution = (entry.get("rcsb_entry_info") or {}).get("resolution_combined")
        ligands = {
            ligand["nonpolymer_comp"]["chem_comp"]["id"]
            for ligand in entry.get("nonpolymer_entities") or []
        }
        chains = entity["rcsb_polymer_entity_container_identifiers"]["auth_asym_ids"]
        details[entity["rcsb_id"]] = {
            "copies": len(chains or []),
            "method": entry["exptl"][0]["method"].split()[0],
            "resolution": resolution[0] if resolution else None,
            "space_group": (entry.get("symmetry") or {}).get("space_group_name_H_M"),
            "cell": " ".join(
                f"{cell[k]:g}" if cell.get(k) is not None else "?"
                for k in (
                    "length_a",
                    "length_b",
                    "length_c",
                    "angle_alpha",
                    "angle_beta",
                    "angle_gamma",
                )
            ),
            "ligands": " ".join(sorted(ligands)),
            "title": (entry.get("struct") or {}).get("title", "")[:50],
        }
    return pd.DataFrame([{**hit, **details.get(hit["entity"], {})} for hit in hits])


def _read_sequences(path: Path) -> list[tuple[str, str]]:
    records = []
    lines = iter(path.read_text().splitlines())
    for line in lines:
        if line.startswith(">"):
            pir = line[3:4] == ";"
            records.append((line[4:] if pir else line[1:], []))
            if pir:
                next(lines, None)  # PIR has a description line after the header
        elif records:
            records[-1][1].append(line)
    return [
        (name.strip() or "unnamed", "".join("".join(seq).split()).upper().rstrip("*"))
        for name, seq in records
    ]


def similar(path: Path, rows: int) -> None:
    for name, sequence in _read_sequences(path):
        print(f"\n{name.split()[0]} ({len(sequence)} residues):")
        if len(sequence) < MIN_LENGTH:
            print(f"  Too short to search: the PDB needs {MIN_LENGTH} or more.")
            continue
        try:
            # Fetch extra hits, so that the best resolution among equals comes first
            hits = _search(sequence, rows * 10)
            table = _describe(hits) if hits else None
        except (urllib.error.URLError, KeyError, IndexError) as error:
            print(f"  Search failed: {error}")
            continue
        if table is None:
            print("  No similar entries found by sequence search.")
            continue
        table = table.sort_values(
            ["identity", "coverage", "resolution"], ascending=[False, False, True]
        )
        print(table.head(rows).to_string(index=False))


def _download(code: str) -> Path | None:
    path = Path(f"{code.lower()}.cif")
    try:
        with urllib.request.urlopen(ENTRY_URL.format(code.upper())) as response:
            path.write_bytes(response.read())
    except urllib.error.URLError as error:
        print(f"Could not download PDB entry {code}: {error}")
        return None
    print(f"Downloaded PDB entry {code} to {path}")
    return path


def model(path: Path, construct: Path | None = None) -> None:
    if not path.exists() and re.fullmatch(r"[0-9][A-Za-z0-9]{3}", str(path)):
        path = _download(str(path))
        if path is None:
            return
    structure = gemmi.read_structure(str(path))
    if len(structure) == 0 or structure[0].count_atom_sites() == 0:
        print(f"No atoms in {path}: it is not a coordinate file.")
        return
    if structure.cell.is_crystal():
        cell = structure.cell.parameters
        print(f"Space group: {structure.spacegroup_hm or 'not given'}")
        print(f"Cell: {' '.join(f'{x:g}' for x in cell)}")
    else:
        print("No crystal cell: a predicted model, or a model from another method.")
    structure.setup_entities()
    ligands = Counter(
        residue.name
        for chain in structure[0]
        for residue in chain
        if residue.entity_type in (EntityType.NonPolymer, EntityType.Branched)
    )
    counts = ", ".join(f"{name} {n}" for name, n in sorted(ligands.items()))
    print(f"Ligands (residue name and number): {counts or 'none'}")
    sequences = {}
    for entity in structure.entities:
        # Without SEQRES, older gemmi leaves the polymer's type unknown
        if entity.entity_type not in (EntityType.Polymer, EntityType.Unknown):
            continue
        subchains = [
            (chain.name, chain.get_subchain(sub))
            for chain in structure[0]
            for sub in entity.subchains
            if chain.get_subchain(sub)
        ]
        if entity.full_sequence:
            source = "full sequence"
            names = [gemmi.Entity.first_mon(name) for name in entity.full_sequence]
        else:
            source = "modelled residues only, gaps not shown"
            names = [residue.name for residue in subchains[0][1]]
        chains = ",".join(dict.fromkeys(name for name, _ in subchains))
        sequences[chains] = gemmi.one_letter_code(names)
        print(f">{entity.name} chains {chains} ({source})")
        print("\n".join(textwrap.wrap(sequences[chains], 60)))

    for name, construct_sequence in _read_sequences(construct) if construct else []:
        if not sequences:
            break
        # Compare with the model's chains that match best
        scoring = gemmi.AlignmentScoring()
        chains = max(
            sequences,
            key=lambda c: (
                gemmi.align_string_sequences(
                    list(construct_sequence), list(sequences[c]), [], scoring
                ).score
            ),
        )
        label = f"model chains {chains}"
        length = len(construct_sequence)
        print(f"\n{name.split()[0]} ({length} residues) against {label}:")
        print("\n".join(_differences(construct_sequence, sequences[chains], "model")))
