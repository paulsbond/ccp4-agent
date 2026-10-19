# Aimless

Aimless scales and merges integrated intensities from one sweep, such as unscaled data from MOSFLM or DIALS. Pointless runs first, to choose the space group and sort the data.

## Contents

- Running it
- Reading the result
- Leaving out images
- Resolution limit
- Merging data that are already scaled

## Running it

Make a new directory for each run and run both programs from inside it. _Why:_ Aimless writes files such as `ROGUES` and `SCALES` into the current directory, and a second run would overwrite them.

1. Choose the space group and sort the data with Pointless ([programs/pointless-symmetry.md](pointless-symmetry.md)), in the same directory. This gives `sorted.mtz`.
2. Write a keyword file `aimless.inp` containing:
   ```
   OUTPUT MERGED UNMERGED
   END
   ```
   Always give the keyword file. _Why:_ without one, Aimless waits for keywords to be typed and never finishes.
3. Scale and merge:
   ```
   aimless HKLIN sorted.mtz HKLOUT scaled.mtz < aimless.inp > aimless.log
   ```

## Reading the result

The run succeeded if `aimless.log` ends with `End of aimless job`. The output files are:

- `scaled.mtz`: merged intensities, `IMEAN` and `SIGIMEAN`, and anomalous intensities `I(+)` and `I(-)`. It has no amplitudes and no free-R flag: add flags with Freerflag ([programs/freerflag.md](freerflag.md)) before using it for anything else.
- `scaled_unmerged.mtz`: scaled, unmerged intensities.

Copy the table after `Summary data for` near the end of `aimless.log` into `journal.md`, down to the line `Space group:`. Its three columns are overall, lowest-resolution shell and highest-resolution shell:

```
                                           Overall  InnerShell  OuterShell
High resolution limit                       2.27      9.09      2.27
Rmerge  (within I+/I-)                     0.044     0.034     0.114
Mean((I)/sd(I))                             22.4      38.1      11.0
Mn(I) half-set correlation CC(1/2)         0.995     0.993     0.976
Completeness                                99.0      91.7      97.4
Multiplicity                                 4.7       4.3       4.5
Anomalous completeness                      96.4      99.0      91.2
DelAnom correlation between half-sets      0.758     0.790     0.475
```

- `DelAnom correlation between half-sets` measures the anomalous signal. When it is clear, the log says `There appears to be a significant anomalous signal so anomalous flag was switched ON`.
- The table `Analysis against all Batches` earlier in the log gives `Rmerge` for each image, called a batch. For images that stand out, run `ccp4-agent batches` ([programs/ccp4-agent-batches.md](ccp4-agent-batches.md)) on `scaled_unmerged.mtz`.

## Leaving out images

To leave out images, add a line before `END` in `aimless.inp` with their numbers, and run Aimless again in a new directory with the same `sorted.mtz`:

```
EXCLUDE BATCH 74 75
OUTPUT MERGED UNMERGED
END
```

To leave out a range, write `EXCLUDE BATCH 121 TO 140`. The log then says `Excluded batches:` with the numbers.

Leave out an image that `ccp4-agent batches` lists, and any image next to it that `Analysis against all Batches` shows clearly worse than the images around it. _Why:_ whatever spoiled the listed image can partly affect the next, and `ccp4-agent batches` lists only images that stand out strongly. Compare the summary tables of the two runs: leaving out a few bad images should raise I/sigma and lower completeness only slightly.

## Resolution limit

Read the limit from the line `from half-dataset correlation CC(1/2) >  0.30` under `Estimates of resolution limits: overall`:

```
Estimates of resolution limits: overall
   from half-dataset correlation CC(1/2) >  0.30: limit =  1.51A
```

If the line ends with `== maximum resolution`, CC½ stays above 0.3 to the edge of the data: keep all of it. Otherwise, add this line before `END` in `aimless.inp` and run Aimless again in a new directory with the same `sorted.mtz`:

```
RESOLUTION HIGH 1.51
```

_Why 0.3:_ it is the same choice xia2 and DIALS make. Weak outer shells still carry signal, and refinement weights each reflection by its error (Karplus and Diederichs, 2012, Science 336, 1030–1033).

## Merging data that are already scaled

To merge unmerged data that another program has already scaled, such as `DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.mtz` from xia2, skip Pointless and use this `aimless.inp`:

```
ONLYMERGE
END
```

```
aimless HKLIN <scaled_unmerged.mtz> HKLOUT merged.mtz < aimless.inp > aimless.log
```

The summary table is the same as above. _Why:_ scaling again would replace the other program's scales with Aimless's own.
