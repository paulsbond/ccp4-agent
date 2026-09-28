---
name: ccp4
description: Solve macromolecular crystal structures from X-ray diffraction data with CCP4, or carry out a single step on existing files. Use for data processing, molecular replacement, experimental phasing, automated model building, refinement, ligand fitting and validation.
metadata:
  source: ccp4-agent
---

# Solve a structure with CCP4

Automated programs can take diffraction images to a mostly built, refined model, but not to a final model ready for deposition. That needs interactive model building and validation by the user.

For a whole structure solution, work through the stages in order, as far as the automated programs reasonably can. For a single step, go straight to its topic page, ask the user for any inputs you cannot find, and stop when the step is done unless the user asks for more.

Topic pages say what to do and which program to use. Program pages say how to run it. Read every page in full before acting on it.

Record every step in `journal.md` in your working directory: the command you ran, the key numbers from its output, and what you decided.

## Stages

1. Data processing: [topics/data-processing.md](topics/data-processing.md).
2. Phasing: molecular replacement if a homologous structure or a predicted model is available, otherwise experimental phasing.
3. Automated model building.
4. Refinement.
5. Validation.
6. Ligands.

Only data processing has a topic page so far. If you are asked for a later stage, tell the user that this skill does not cover it yet.

## Programs

- [programs/xia2.md](programs/xia2.md): automated data processing with DIALS, or with XDS if it is installed.
- [programs/dials.md](programs/dials.md): data processing one step at a time, for choosing a lattice or processing several lattices.
