# ccp4-agent similar

`ccp4-agent similar` searches the current PDB for entries similar to each sequence in a file, and lists their crystal forms and ligands. It sends the sequences to the RCSB PDB, so run it only when the user asks for it.

## Running it

```
ccp4-agent similar contents.fasta
```

- The file is FASTA or PIR. Each record is searched in turn. Records shorter than 10 residues cannot be searched.
- To list more than 10 entries for each record, add `--rows <n>`.

## Reading the result

```
edited (240 residues):
entity  identity  coverage  copies method  resolution space_group                              cell      ligands
30TA_1     0.951       1.0       1  X-RAY        1.05    P 1 21 1  42.239 41.479 71.98 90 104.15 90 A1J8Z MBO ZN
```

- `entity` is the PDB ID and the number of the matching chain type in that entry.
- `identity` is the fraction of identical residues where the sequences align, and `coverage` the fraction of your sequence that aligns.
- `copies` is the number of chains of that type in the entry.
- `ligands` lists the non-polymer residue names in the entry.
- Entries are sorted by identity, then coverage, then resolution.
- `No similar entries found by sequence search.` or `Search failed: <error>` mean no list for that record.
