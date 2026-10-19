# Reindex

Reindex changes the space group of merged data to another space group of the same point group. The indices and all columns, including the free-R flags, stay as they are. Use it when molecular replacement has chosen a space group that the data were not processed in, so that the data file matches the model.

## When to use it

Use Reindex only within the same point group, and only in these cases:

- **The other enantiomorph**, such as P 4<sub>1</sub> 2<sub>1</sub> 2 and P 4<sub>3</sub> 2<sub>1</sub> 2, P 3<sub>1</sub> 2 1 and P 3<sub>2</sub> 2 1, or P 6<sub>1</sub> 2 2 and P 6<sub>5</sub> 2 2, and I 2 3 and I 2<sub>1</sub> 3. _Why:_ the same reflections are present and absent, so merging in the new space group gives the same data.
- **More screw axes**, such as P 2 2 2 to P 2<sub>1</sub> 2<sub>1</sub> 2<sub>1</sub>, or P 2 to P 2<sub>1</sub>. _Why:_ the data then hold some reflections that the new space group says are absent. Servalcat removes them itself, and its log says `Removing <n> systematic absences`.

Otherwise, process the data again with the new space group, from the images with xia2 ([programs/xia2.md](xia2.md)) or from the unmerged data with Pointless ([programs/pointless-symmetry.md](pointless-symmetry.md)) and Aimless:

- **Fewer screw axes**, such as P 2<sub>1</sub> 2<sub>1</sub> 2<sub>1</sub> to P 2 2 2<sub>1</sub> or P 2 2 2. _Why:_ data processing may have removed the reflections on the axes that the old space group says are absent, and the new one needs them.
- **A different point group.** _Why:_ scaling and merging depend on the point group, and the free-R flags must be chosen again to suit it.

## Running it

Write a keyword file `reindex.inp` with the new space group, in quotes:

```
SYMM "I 21 3"
END
```

_Why the quotes:_ without them, Reindex stops with `**SYMMETRY OPERATOR ERROR**`.

```
reindex HKLIN <data.mtz> HKLOUT <data_new.mtz> < reindex.inp > reindex.log
```

Always give the keyword file. _Why:_ without one, Reindex waits for keywords to be typed and never finishes.

## Reading the result

The run succeeded if `reindex.log` says `REINDEX:   ** Normal termination` near the end, and `Number of reflections written to output file:` gives the same number as `gemmi mtz` ([programs/gemmi-mtz.md](gemmi-mtz.md)) gives for the input.

Check that the two `Point group:` lines in `reindex.log`, under `Input symmetry:` and `Output symmetry:`, are the same:

```
Space group: "I 2 3" Point group: "PG23" Laue group: "m3bar"
Space group: "I 21 3" Point group: "PG23" Laue group: "m3bar"
```

If they differ, delete the output file: the space group you gave is wrong for these data. _Why:_ Reindex does not check. Given I 4 3 2 for data in I 2 3, it wrote a file in I 4 3 2 and still ended normally.

The log always says `WARNING: ** Symmetry change of merged data **`. This is expected.

Servalcat refines against the new file in the new space group, without the warning `space group mismatch between model and mtz`.
