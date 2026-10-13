# ccp4-agent uniprot

`ccp4-agent uniprot` shows a UniProt entry and what it says about the protein as it exists in the cell, and compares constructs with it.

## Running it

```
ccp4-agent uniprot <accession> --construct contents.fasta
```

- `<accession>` is a UniProt accession, such as `P00918`. Only the accession is sent to UniProt.
- `--construct` is optional. It names a FASTA or PIR file, normally `contents.fasta`. The comparison runs on this computer.

## Reading the result

```
P00918: Carbonic anhydrase 2, Homo sapiens, UniProtKB reviewed (Swiss-Prot), 260 residues
>P00918
MSHHWGYGKHNGPEHWHKDFPIAKGERQSPVDIDTHTAKYDPSLKPLSVSYDQATSLRIL
...

Processing (residue numbers in the sequence above):
  Initiator methionine 1 Removed
  Chain 2-260 Carbonic anhydrase 2

Modifications:
  Modified residue: 2 N-acetylserine; 2 Phosphoserine; 165 Phosphoserine; 172 Phosphoserine

Binding sites:
  Zn(2+): 94, 96, 119
  substrate: 198-199

Cofactors: Zn(2+), Co(2+)
Subunit: Interacts with SLC4A4 ...
```

- `Processing` lists the parts removed in the cell: initiator methionine, signal peptide, transit peptide and propeptides. `Chain` is the mature protein.
- `Modifications` lists disulfide bonds, glycosylation, modified residues and lipidation.
- `Binding sites` lists the residues that bind each ligand.
- `Cofactors` and `Subunit` come from UniProt's comments. `Subunit` describes the oligomeric state and partners.
- `Could not fetch UniProt entry <accession>` means the accession does not exist or UniProt cannot be reached.

## Comparing with the construct

With `--construct`, each record of the FASTA file is compared with the UniProt sequence, in UniProt numbering:

```
edited (240 residues) against UniProt:
  Covers UniProt 1-240, 233 of 234 aligned residues identical
  Extra at the N-terminus: GA
  Missing UniProt 39-44
  Inserted after UniProt 98: GGSG
  Mutation V206S
```

The lines mean the same as for [programs/ccp4-agent-model.md](ccp4-agent-model.md), with UniProt in place of the model. `Mutation V206S` means UniProt has V at residue 206, and your construct has S. `Too different to list changes.` or `No alignment` means the accession or the sequence is wrong.
