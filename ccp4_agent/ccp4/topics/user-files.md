# The user's files and experiments

## When to use

First, before any other step, whether you are solving a whole structure or doing a single step. Skip it only if `journal.md` already has a `Files and experiments` section. _Why:_ what was collected and what the user already has decide how to process the data and which later stages are needed. An unpublished structure of the same molecule, for example, can make phasing easy, and only the user knows about it.

## Inputs

- Your working directory, and any folders the user names.

## Steps

Asking needs no CCP4. Run the commands below the way [topics/ccp4-setup.md](ccp4-setup.md) describes for CCP4 commands.

1. List the files in your working directory and its subfolders with your file tools. _Why:_ you can then ask about them by name.
2. Ask the user the questions in "What to ask" below, in one message. If they do not know an answer or want to skip it, record that and continue with what you have.
3. Work out what each file is, as in "Kinds of file" below.
4. Add a `Files and experiments` section to `journal.md`: each crystal and sweep, with its wavelength and purpose, and the path of each file and what it is.
5. Tell the user what you recorded, and ask them to correct anything wrong. Then continue.

## What to ask

- The diffraction experiments: how many crystals, and for each crystal, how many sweeps, at which wavelengths and why. For example, one native sweep; sweeps at the peak and inflection of an absorption edge for MAD; or a long-wavelength sweep for sulfur SAD. _Why:_ sweeps at different wavelengths carry different anomalous signal for experimental phasing, so each wavelength is kept as a dataset of its own.
- Which crystals were soaked or derivatised, for example with heavy atoms or ligands, and which images come from which crystal.
- Which images were only tests, for example screening shots. _Why:_ they are rarely worth processing with the main sweeps.
- Any earlier processing of these data, and what it found.
- Coordinate files: their own earlier structures of this molecule (published or not), and structures of homologues.
- A predicted model, for example from AlphaFold 3, Boltz, Chai or OpenFold 3. _Why:_ unless an earlier structure of the same molecule exists, a predicted model is usually the best search model for molecular replacement, much better than a PDB entry of similar sequence. The best is a prediction of everything in the crystal together: the whole complex, or the oligomer if the molecule forms one. _Why:_ a prediction of the assembly gets the interfaces between chains right more often, and even a predicted homodimer can be a better search model than a monomer. If they have none, ask whether they can make one, or agree to one being made, and record the answer.
- Sequence files, and restraint dictionaries for ligands.

Name the files you found in step 1, and ask what each one is if its name does not say.

## Kinds of file

- **Diffraction images.** Numbered series such as `name_00001.cbf`, or `.img` or `.mccd` files; or, for Eiger detectors, a master file ending in `_master.h5` or `.nxs` beside data files. Each numbered series, or each master file, is usually one sweep. Record its folder, name pattern, first and last image, and which crystal and wavelength it belongs to.
- **Processed data.** `.mtz`, `.sca`, `XDS_ASCII.HKL`, or `.cif` files of structure factors. Describe each MTZ file with `gemmi mtz`, as described in [programs/gemmi-mtz.md](../programs/gemmi-mtz.md). Record the programs that made it, whether it is merged or unmerged, and its space group, cell, resolution and wavelength.
- **Coordinates.** `.pdb`, `.ent`, `.cif` or `.mmcif`. Describe each with [programs/ccp4-agent-model.md](../programs/ccp4-agent-model.md), and record its space group and cell, or that it has no crystal cell. A model with no crystal cell is a predicted model, or one from NMR or cryo-EM: ask the user which, if the name does not say. [topics/similar-structures.md](similar-structures.md) compares these models with the crystal's contents.
- **A `.cif` file that `ccp4-agent model` says is not a coordinate file.** It is a restraint dictionary for a ligand or a file of structure factors. Ask the user which, and record it.
- **Sequences.** `.fasta`, `.fa`, `.seq` or `.pir`. [topics/cell-contents.md](cell-contents.md) uses them.
- **Logs and results of earlier runs.** Record what they are. Do not repeat their work without telling the user.

## If it fails

- If there are no files in your working directory, ask the user where their files are. If they have none yet, record that and continue.
