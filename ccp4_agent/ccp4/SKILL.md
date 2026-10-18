---
name: ccp4
description: Solve macromolecular crystal structures from X-ray diffraction data with CCP4, or carry out a single step on existing files. Use for taking stock of the user's files and experiments, the crystal's contents and similar structures, data processing, molecular replacement, experimental phasing, automated model building, refinement, ligand fitting and validation.
metadata:
  source: ccp4-agent
---

# Solve a structure with CCP4

Automated programs can take diffraction images to a mostly built, refined model, but not to a final model ready for deposition. That needs interactive model building and validation by the user.

For a whole structure solution, work through the stages in order, as far as the automated programs reasonably can. For a single step, do stages 1 to 3 and then go straight to the step's topic page, ask the user for any inputs you cannot find, and stop when the step is done unless the user asks for more.

Topic pages say what to do and which program to use. Program pages say how to run it. Read every page in full before acting on it.

Record every step in `journal.md` in your working directory: the command you ran, the key numbers from its output, and what you decided.

Never send the user's sequences or files to an online service unless the user asks you to. You may download public entries, such as PDB entries by ID and UniProt entries by accession. If a download fails, tell the user that this computer may have no internet access or the service may be down.

Before the first CCP4 command, find CCP4 and learn how to run its programs: [topics/ccp4-setup.md](topics/ccp4-setup.md).

## Stages

1. The user's files and experiments, always first: [topics/user-files.md](topics/user-files.md).
2. Cell contents: [topics/cell-contents.md](topics/cell-contents.md).
3. Similar structures: [topics/similar-structures.md](topics/similar-structures.md).
4. Data processing: [topics/data-processing.md](topics/data-processing.md).
5. Phasing. If data processing found the same crystal form as an earlier structure of the same molecule, refine that structure directly: [topics/isomorphous-refinement.md](topics/isomorphous-refinement.md). Otherwise, molecular replacement with the starting model chosen in stage 3: an earlier structure of the same molecule if there is one, or else preferably a predicted model rather than a homologue. Use experimental phasing if there is no model.
6. Automated model building.
7. Refinement.
8. Validation.
9. Ligands.

Only stages 1 to 4 and isomorphous refinement have topic pages so far. If you are asked for another stage, tell the user that this skill does not cover it yet.

## Programs

- [programs/aimless.md](programs/aimless.md): scaling and merging integrated data, such as unscaled data from MOSFLM.
- [programs/ccp4-agent-batches.md](programs/ccp4-agent-batches.md): data quality against image number.
- [programs/ccp4-agent-model.md](programs/ccp4-agent-model.md): the space group, cell, ligands and sequences of a coordinate file or PDB entry, compared with the crystal's contents.
- [programs/ccp4-agent-similar.md](programs/ccp4-agent-similar.md): searching the current PDB online, only when the user asks.
- [programs/ccp4-agent-uniprot.md](programs/ccp4-agent-uniprot.md): a UniProt entry, compared with the construct.
- [programs/dials.md](programs/dials.md): data processing one step at a time, for choosing a lattice or processing several lattices.
- [programs/gemmi-convert.md](programs/gemmi-convert.md): removing waters and ligands from a model.
- [programs/gemmi-mtz.md](programs/gemmi-mtz.md): describing an MTZ file.
- [programs/mrparse.md](programs/mrparse.md): searching for similar structures from the PDB (on this computer) and the AlphaFold database (online).
- [programs/pointless-reference.md](programs/pointless-reference.md): checking the indexing of data against a model or reference data.
- [programs/pointless-symmetry.md](programs/pointless-symmetry.md): choosing the space group of integrated data before scaling with Aimless.
- [programs/servalcat.md](programs/servalcat.md): refinement of a model against X-ray data.
- [programs/xia2.md](programs/xia2.md): automated data processing with DIALS, or with XDS if it is installed.
