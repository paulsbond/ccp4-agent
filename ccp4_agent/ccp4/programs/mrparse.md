# MrParse

MrParse searches for structures and predicted models similar to a sequence, and prepares them as search models for molecular replacement.

## Running it

```
mrparse --seqin chain1.fasta
```

- `--seqin` is a FASTA file. MrParse searches only its first sequence, so give each chain a file of its own.
- It searches both the PDB and the AlphaFold database, on this computer, against copies of their sequences that come with CCP4, and sends the sequence nowhere. It then downloads the entries it finds by their IDs, from the RCSB PDB and the EBI.
- The copies are as old as the CCP4 installation, so the newest entries are missing. The copy of the AlphaFold database holds about a million of its predictions, not all of them.
- It ends by printing `Big Fantastic Virus Database search could not find any hits!` and `ESMfold Atlas database search could not find any hits!`. Ignore those two lines: CCP4 does not include copies of those databases.
- In the PDB, it keeps by default one entry for each group of sequences more than 95% identical, which shows the homologues. To list the closest entries instead, which are usually several of the same molecule, add `--phmmer_dblvl 100`.
- To search only one database, add `--database pdb` or `--database afdb`.
- Do not add `--do_classify` unless the user agrees to send their sequence online. _Why:_ it predicts transmembrane regions with DeepTMHMM through BioLib, which runs on BioLib's servers.
- For the AlphaFold database, it removes residues with pLDDT below 70 from the prepared models. To change that, add `--plddt_cutoff 50` or `--plddt_cutoff 90`. Do not use `--plddt_cutoff None`, which the help offers: it stops with `ValueError` and prepares no models.

Each run makes a new folder, `mrparse_0`, `mrparse_1` and so on.

## Reading the result

In the run's folder, for the PDB:

- `homologs.json` lists the entries found, best first. Each has `name` (PDB ID and chain), `seq_ident` (fraction of identical residues), `range` (the residues of your sequence it covers) and `resolution`.
- `pdb_files` holds the downloaded entries. MrParse removes ligands and waters from them.
- `homologs` holds each match trimmed to the region that aligns with your sequence, ready for molecular replacement.

For the AlphaFold database:

- `af_models.json` lists the predictions found, best first. Each has `name` (such as `AF-P00918-F1`, where `P00918` is the UniProt accession), `seq_ident`, `range`, `avg_plddt` (the model's mean confidence, from 0 to 100) and `pdb_file`.
- `AF2_files` holds the downloaded predictions.
- `models` holds each prediction prepared for molecular replacement: trimmed by pLDDT and to the region that aligns with your sequence, with pLDDT converted to B-factors.

For example, a search with human carbonic anhydrase II listed in `homologs.json` first `3k34_A` with `seq_ident` 1.0 and `range` 3-260 (the same protein), then `4cnx_A` with `seq_ident` 0.79 (a homologue). In `af_models.json` it listed first `AF-P00918-F1` with `seq_ident` 1.0 and `avg_plddt` 97.6.

The AlphaFold database holds predictions of single chains. A prediction of everything in the crystal together, made by the user, can be a better search model.

If a PDB entry cannot be downloaded, MrParse prints `Error downloading PDB file for: <id>` and continues, and the entry is still listed in `homologs.json`. If a prediction cannot be downloaded, MrParse prints `SearchModelFinder failed:` with the address `alphafold.ebi.ac.uk`, and `af_models.json` is empty. The predictions it found are still listed, by ID, in the first column of `phmmerTblout_af2.log`, best first. A prediction that cannot be prepared gives `Error selecting residues for: <id>`, and is left out.
