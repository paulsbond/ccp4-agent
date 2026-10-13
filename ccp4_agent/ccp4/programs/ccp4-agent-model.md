# ccp4-agent model

`ccp4-agent model` describes a coordinate file: its space group and cell, its ligands, and the sequence of each different chain. It can compare those sequences with the crystal's contents.

## Running it

```
ccp4-agent model <file> --construct contents.fasta
```

- `<file>` is a PDB or mmCIF file. It can instead be a PDB ID, such as `3k34`: the command then downloads the whole entry from the RCSB PDB into `<id>.cif` in the current folder, and describes that. Only the ID is sent.
- `--construct` is optional. It names a FASTA or PIR file, normally `contents.fasta`.

## Reading the result

For example, for a crystal structure:

```
Space group: P 1 21 1
Cell: 42.045 41.269 71.821 90 104.23 90
Ligands (residue name and number): GOL 3, HGB 1, SUA 1, ZN 1
>1 chains A (full sequence)
MSHHWGYGKHNGPEHWHKDFPIAKGERQSPVDIDTHTAKYDPSLKPLSVSYDQATSLRIL
...
```

- `Space group` and `Cell` mean the file has a crystal cell. `No crystal cell: a predicted model, or a model from another method.` means it has none, as for predicted models and models from NMR or cryo-EM. Such files often carry a dummy cell of 1 1 1 90 90 90 in P 1, which counts as no crystal cell.
- `Ligands` lists every residue that is not part of a polymer chain or water, with how many there are.
- Then comes one FASTA record for each different chain, with the chains that have it. A predicted model of a complex or oligomer has several chains.
- `(full sequence)` means the file records the whole sequence of the chain as it was in that experiment, including residues that were not modelled. For an entry from the PDB this is the construct of that crystal, which may differ from yours.
- `(modelled residues only, gaps not shown)` means the file records only the residues in the model. Disordered residues are missing, and the gaps are not marked.
- `No atoms in <file>: it is not a coordinate file.` For a `.cif` file, this usually means a restraint dictionary for a ligand, or structure factors.
- `Could not download PDB entry <id>` means the ID does not exist or the RCSB PDB cannot be reached.

## Comparing with the construct

With `--construct`, each record of the FASTA file is compared with the chain that matches it best:

```
histag (287 residues) against model chains A:
  Covers model 2-260, 259 of 259 aligned residues identical
  Extra at the N-terminus: MGSSHHHHHHSSGLVPRGSH
  Extra at the C-terminus: LEHHHHHH
```

- `Covers model` gives the residues of the model's sequence that align, and how many of them are identical. The numbers count along the model's sequence from 1, and are not residue numbers.
- `Extra at the N-terminus` or `C-terminus`: residues of your construct that the model lacks, such as a tag.
- `Missing model <n>-<m>`: residues of the model that your construct lacks. If the model has only its modelled residues, these include gaps in the model.
- `Inserted after model <n>`: residues of your construct that the model lacks, inside the chain.
- `Mutation C206S`: the model has C at position 206, and your construct has S.
- `Too different to list changes.` Fewer than 90% of the aligned residues are identical: a homologue, or the wrong file.
