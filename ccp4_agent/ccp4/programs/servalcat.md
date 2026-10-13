# Servalcat

Servalcat refines a model against X-ray data, with likelihood targets and restraints from CCP4's monomer library.

## Running it

```
servalcat refine_xtal_norefmac --hklin <data.mtz> --model <model.cif> -s xray -o refined
```

- `--hklin` is the merged data. Servalcat picks the columns itself, preferring amplitudes, and guesses which value of the free-R flag marks the free set. To refine against intensities instead, add `--prefer_intensity`; the table then has `CCIworkavg`, `R1work` and `R1free` in place of `CCFworkavg`, `Rwork` and `Rfree`.
- `--model` is a PDB or mmCIF file. Ligands must be in CCP4's monomer library, or given as restraint dictionaries with `--ligand <file.cif>`.
- `-s xray` says the data are X-ray data.
- `-o refined` sets the start of the output names.
- It runs 10 cycles. To change that, add `--ncycle <n>`.
- To take the free-R flags from another file, such as the earlier structure's data, add `--hklin_free <earlier.mtz>`. The two files must be indexed the same way.

## Reading the result

The log is `refined.log`. Near the end is a table of statistics against cycle:

```
 Ncyc  CCFworkavg  CCFfreeavg  Rwork  Rfree    FOM         -LL  rmsBOND  zBOND  rmsANGL  zANGL
    0      0.7176      0.7005 0.2953 0.2991 0.7566 354254.8080   0.0323 2.7069   3.7001 1.9960
    1      0.7825      0.7366 0.2654 0.2848 0.7810 347455.7832   0.0137 1.0468   1.9448 1.0435
   10      0.8226      0.7586 0.2424 0.2750 0.7946 342232.1323   0.0111 0.8566   2.0429 1.0827
```

- Cycle 0 is the model as given. The last cycle is the refined model.
- `Rwork` and `Rfree` are the R factors against the working and free reflections. A falling `Rfree` means the model is improving.
- `rmsBOND` and `rmsANGL` are the deviations from ideal geometry. Servalcat adjusts the weight to keep `zBOND` between 0.5 and 1.0.
- If the free-R flag column has only one value, the log says `FreeR_flag is not a test flag because all its values are identical`, and the table has no free columns. Data from xia2 always have a free set.
- If the model and the data have different space groups, the log says `Warning: space group mismatch between model and mtz` and uses the model's space group.

The output files are:

- `refined.mmcif` and `refined.pdb`: the refined model.
- `refined.mtz`: map coefficients. `FWT` and `PHWT` give the 2mFo-DFc map, and `DELFWT` and `PHDELWT` the mFo-DFc difference map.
