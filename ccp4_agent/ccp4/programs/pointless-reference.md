# Pointless: indexing against a reference

Pointless checks the indexing of diffraction data against reference data or a reference model, and reindexes the data to match.

## Running it

Write a keyword file `pointless.inp` containing only the line `END`. _Why:_ without a keyword file, Pointless waits for keywords to be typed and never finishes.

To check the indexing of merged or unmerged data against a model:

```
pointless HKLIN <data.mtz> XYZIN ./<model.cif> HKLOUT reindexed.mtz < pointless.inp > pointless.log
```

- `XYZIN` is a PDB or mmCIF file with the space group and cell. Pointless calculates reference data from it.
- To compare with reference data instead of a model, replace `XYZIN ./<model.cif>` with `HKLREF <reference.mtz>`.
- Keep `./` in front of a `.cif` file in the current folder. _Why:_ without a folder, CCP4 first looks for the file in its own library and prints `Cannot find input file (Error)` at the top of the log, although it then reads yours.
## Reading the result

The summary at the end of the log has one of these tables. Where the data can be indexed in more than one way:

```
Alternative indexing scores relative to reference
       Alternative reindexing        Lklhd      CC     R(E^2)    Number Cell_deviation
 1              [k,h,-l]             0.903    0.703    0.272     39165      0.54
 2              [h,k,l]              0.097    0.071    0.493     39165      0.54
```

Where there is only one way:

```
Comparison score relative to reference
       Alternative reindexing        Lklhd      CC     R(E^2)    Number Cell_deviation
 1              [h,k,l]              1.000    0.735    0.258     35557      0.18
```

- The first line is the best match. `[h,k,l]` means the data were already indexed like the reference. Any other operator means `reindexed.mtz` was reindexed with it.
- `CC` is the correlation between your data and the reference. `Lklhd` is the probability of each way relative to the others.
- `reindexed.mtz` keeps all columns, including the free-R flags, and takes the space group of the reference.
- If the log has `**** ERROR ****` and `Merged test dataset (HKLIN) has different Laue symmetry to reference set`, the data and the reference are not the same crystal form, and no `reindexed.mtz` is written.
