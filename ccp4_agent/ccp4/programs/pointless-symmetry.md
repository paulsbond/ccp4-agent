# Pointless: symmetry of integrated data

Pointless chooses the space group of integrated, unscaled data, such as data from MOSFLM or DIALS, and sorts them ready for scaling with Aimless.

## Running it

Make a new directory for the run, and in it write a keyword file `pointless.inp` containing only the line `END`. _Why:_ without a keyword file, Pointless waits for keywords to be typed and never finishes.

```
pointless HKLIN <integrated.mtz> HKLOUT sorted.mtz < pointless.inp > pointless.log
```

## Reading the result

Read the result from the lines after `Best Solution:` near the end of `pointless.log`:

```
Best Solution:    space group H 3 2
   Reindex operator:                   [h,k,l]
   Laue group probability:             0.999
```

- The space group may differ from the one in the input file, here `H 3` before. `sorted.mtz` has Pointless's space group. Scale it with Aimless, as described in [programs/aimless.md](aimless.md).
- If it says `point group` instead of `space group`, followed by `WARNING: You will have to determine the true space group later`, the data cannot tell apart space groups that differ only in their screw axes, such as I 2 3 and I 2<sub>1</sub> 3. Record both in `journal.md` and continue. _Why:_ molecular replacement, or an earlier structure of the same crystal form, decides between them.
