# Sheetbend

Sheetbend refines a model by shift-field refinement: it moves whole regions of the model at once, starting at low resolution, to correct large errors such as those in a model placed by molecular replacement. It uses no geometry restraints, so always follow it with refinement in Servalcat.

## Running it

The program is called `csheetbend`. Give it a PDB file:

```
csheetbend -mtzin <data.mtz> -colin-fo "/*/*/[F,SIGF]" -colin-free "/*/*/[FreeR_flag]" -pdbin <model.pdb> -pdbout sheetbend.pdb -coord -cycles 12 -resolution-by-cycle 6,3 -pseudo-regularize -refine-regularize-cycles 3 > sheetbend.log
```

- `-colin-fo` names the amplitudes and their sigmas, and `-colin-free` the free-R flag, in the form `/*/*/[<column>]`. List the columns with `gemmi mtz` ([programs/gemmi-mtz.md](gemmi-mtz.md)). The example is for `DataFiles/AUTOMATIC_DEFAULT_free.mtz` from xia2. Keep the quotes. If the file has no free-R flag, add one first with Freerflag ([programs/freerflag.md](freerflag.md)).
- `-coord` refines the coordinates.
- `-cycles 12 -resolution-by-cycle 6,3` runs 12 cycles, from 6 Å to 3 Å. _Why:_ large shifts are found at low resolution first.
- `-pseudo-regularize -refine-regularize-cycles 3` repeats the 12 cycles three times, each followed by a regularisation of the geometry.

It takes seconds.

## Version

The first lines of `sheetbend.log` give the version, as in `csheetbend         version 0.5.0`. Version 0.5.0 and older do not scale the observed amplitudes to the model's before calculating the shifts. This matters only if the amplitudes are not on an absolute scale. Amplitudes from xia2, DIALS and Ctruncate are, but amplitudes converted from intensities by `servalcat fw` are not: do not use those with Sheetbend 0.5.0. Version 0.5.1 and later scale them.

## Reading the result

The run succeeded if `sheetbend.log` says `csheetbend: Normal termination` near the end. The refined model is `sheetbend.pdb`.

The log gives `R-factor` and `Free R-factor` for each cycle, at that cycle's resolution only. Do not use them to judge the model. _Why:_ they are not comparable between cycles. The free R-factor at low resolution rests on few reflections, and jumps from one cycle to the next.

Refine `sheetbend.pdb` for 10 cycles with Servalcat, without jelly-body restraints ([programs/servalcat.md](servalcat.md)), and judge the model from its table, as for jelly-body refinement there. Cycle 0 shows the model as Sheetbend left it.
