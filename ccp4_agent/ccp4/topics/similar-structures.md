# Similar structures

## When to use

After [topics/cell-contents.md](cell-contents.md), before any other step, whether you are solving a whole structure or doing a single step. Skip it only if `journal.md` already has a `Similar structures` section. _Why:_ structures of the same molecule, whether the user's own or in the PDB, can show the cell, space group and ligands before you process the data, and decide, with any predicted model, which model to start phasing from.

## Inputs

- `contents.fasta`, from [topics/cell-contents.md](cell-contents.md).
- The user's coordinate files, including predicted models, from the `Files and experiments` section of `journal.md`.

## Steps

Run the commands below the way [topics/ccp4-setup.md](ccp4-setup.md) describes for CCP4 commands.

1. Compare each of the user's coordinate files with `contents.fasta` using `ccp4-agent model` ([programs/ccp4-agent-model.md](../programs/ccp4-agent-model.md)), and judge it as in "The user's structures" below.
2. Search the PDB and the AlphaFold database, as in "Searching the PDB and the AlphaFold database" below.
3. Choose the starting model for phasing, as in "Choosing the starting model" below.
4. Add a `Similar structures` section to `journal.md`. For each structure, record where it came from (the user's own, the PDB, or predicted), the file or PDB ID, the identity and the residues it covers, the space group and cell, and any ligands that matter, as in "Ligands" below. Record the starting model you chose, and why.
5. Tell the user what you found and which starting model you chose, and continue.

## The user's structures

- **A crystal cell, and nearly all aligned residues identical.** An earlier crystal structure of the same molecule. If the user solved it, it may be unpublished, so no search will find it.
- **A crystal cell, and `Too different to list changes`.** A homologue. Record the identity from the `Covers` line.
- **`No crystal cell`.** A predicted model, or one from NMR or cryo-EM. Record which chains it has and which residues of your construct each covers. A predicted model of a complex or oligomer has a chain for each copy.

## Choosing the starting model

Choose the first that applies:

1. **A crystal structure of the same molecule, the same or with only small mutations.** If data processing finds the same crystal form, refine it directly; if not, use it as the search model for molecular replacement. _Why:_ it is an experimental model of this molecule, so nothing fits the data better.
2. **A predicted model.** Use it as the search model for molecular replacement. If the user has none, ask them to make one, for example with AlphaFold 3, Boltz, Chai or OpenFold, of everything in the crystal together, or whether they agree to one being made. Meanwhile, use the best prediction of each chain from the AlphaFold database, found as in "Searching the PDB and the AlphaFold database" below. _Why:_ current predictions are usually much better search models than PDB entries of similar sequence.
3. **A homologue from the PDB or the user's files.** Use it only if no predicted model can be had. Record the best few by identity and coverage.
4. **Nothing.** Phasing will need to be experimental.

## Searching the PDB and the AlphaFold database

For each record of `contents.fasta`, write it to a file of its own, such as `chain1.fasta`, and search with MrParse ([programs/mrparse.md](../programs/mrparse.md)), listing the closest PDB entries. It searches the PDB and the AlphaFold database on this computer, and sends the sequence nowhere. _Why the closest entries:_ they are usually several of the same molecule, which show its crystal forms and ligands. If none is the same molecule, run it again with its default grouping of near-identical sequences, to find homologues.

Record the best prediction of each chain from `af_models.json`, with its `seq_ident`, `range` and `avg_plddt`.

For the best entries, compare the PDB entry with `contents.fasta` using `ccp4-agent model` ([programs/ccp4-agent-model.md](../programs/ccp4-agent-model.md)) with the PDB ID. _Why:_ MrParse removes ligands from the files it downloads, and this downloads the whole entry, for its space group, cell and ligands.

- **Identity near 1, covering most of your sequence.** The same molecule. Your sequence may have a tag or extra residues that the structure lacks. Record the space group and cell: your crystals may have the same form, and data processing compares against it. The copies in such a structure are a hint for your crystal only if it has the same crystal form.
- **Lower identity.** Homologues. Record them, and choose as in "Choosing the starting model" above.
- **Nothing similar.** Record that.

If the user asks for a search of the whole current PDB, run [programs/ccp4-agent-similar.md](../programs/ccp4-agent-similar.md), which sends the sequences to the RCSB PDB. Run it only when the user asks.

## Ligands

Read the `Ligands` line from `ccp4-agent model` for the entries of the same molecule. A metal or cofactor in those entries is probably in your crystal too, even if the user did not mention it, especially if UniProt lists it as a cofactor: add it to the expected contents in the `Cell contents` section of `journal.md`, and tell the user. Ignore common additives such as `GOL`, `EDO`, `SO4` and `CL` unless they are in your crystallisation conditions.

For example, for human carbonic anhydrase II, the first MrParse run listed `3k34_A` with `seq_ident` 1.0, and `ccp4-agent model 3k34` printed:

```
Space group: P 1 21 1
Cell: 42.045 41.269 71.821 90 104.23 90
Ligands (residue name and number): GOL 3, HGB 1, SUA 1, ZN 1
```

UniProt lists zinc as the cofactor, and there is one `ZN` for the one chain, so add one zinc ion per chain to the expected contents. `GOL` is glycerol, an additive. `HGB` and `SUA` are compounds from that study: check them against the user's ligands.

## If it fails

- If MrParse prints `Error downloading PDB file`, or `ccp4-agent model` prints `Could not download PDB entry`, this computer may have no internet access or the RCSB PDB may be down. Tell the user, record the PDB IDs, identities and ranges from `homologs.json`, which MrParse still writes, and continue.
- If the AlphaFold database search stops with `SearchModelFinder failed:`, the same applies to the EBI. Record the IDs of the predictions it found from `phmmerTblout_af2.log` ([programs/mrparse.md](../programs/mrparse.md)), and continue.
