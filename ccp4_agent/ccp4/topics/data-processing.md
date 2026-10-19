# Data processing

## When to use

You have diffraction images from a rotation sweep and need merged intensities in an MTZ file. A later stage may also send you back here: to use a different space group, lattice or resolution limit, or to leave out images.

## Inputs

- The images: the NeXus master file ending in `.nxs` for Eiger data, or the image files of the sweep.
- Optionally, a space group, lattice or image range from a later stage.
- Optionally, the space groups and cells of earlier structures of the same molecule, from the `Similar structures` section of `journal.md`, found as in [topics/similar-structures.md](similar-structures.md).

## Steps

1. Process the images with xia2 and the DIALS pipeline ([programs/xia2.md](../programs/xia2.md)). If a later stage gave you a space group, pass it to xia2.
2. Copy `xia2-summary.dat` into `journal.md`.
3. Check the data against image number, as in "Quality against image number" below.
4. Explain the completeness and resolution, as in "Completeness" and "Resolution limit" below.
5. Check for twinning, pseudotranslation and ice rings, as in "Twinning, pseudotranslation and ice rings" below.
6. Check how clearly the data support the symmetry, as in "Symmetry" below.
7. Compare the space group and cell with earlier structures of the same molecule, as in "Known crystal forms" below.
8. Tell the user what you found in steps 3 to 7, and continue to the next stage with `DataFiles/AUTOMATIC_DEFAULT_free.mtz`. There is no fixed standard for good enough: the next stages show whether the data suffice.

## Quality against image number

Run `ccp4-agent batches` ([programs/ccp4-agent-batches.md](../programs/ccp4-agent-batches.md)) on `DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.mtz`. It shows Rmerge and I/sigma for ranges of images, then lists single images that stand out from the rest.

- **Single images listed.** Something went wrong on those images, for example ice, a shutter fault, or the crystal leaving the beam. Process again without them. For images at the start or end of the sweep, give xia2 an image range. For images in the middle, use DIALS step by step ([programs/dials.md](../programs/dials.md)) and exclude them when scaling.
- **Rmerge rising and I/sigma falling steadily towards the end of the sweep.** This is radiation damage. Process again without the worst images at the end, and keep both results. _Why:_ leaving out images improves agreement but loses completeness and multiplicity, which matter most for experimental phasing, and only the next stages show which result is better. Record both in `journal.md`, with the completeness and, for anomalous data, the anomalous completeness and multiplicity of each.
- **No trend and no images listed.** Nothing to leave out.

## Completeness

Read the completeness in each resolution shell from the `%comp` column of `LogFiles/AUTOMATIC_DEFAULT_NATIVE_merging-statistics.txt`.

- **High to near the resolution limit, then falling in the last few shells.** The crystal diffracts beyond the edge of the detector, so the corners record only part of the outer shells. Tell the user the resolution to which the data are nearly complete. This is normal.
- **Low in every shell.** The sweep covers too little rotation for this crystal's symmetry. Tell the user that collecting more rotation would help.
- **Low only in the lowest-resolution shell.** Reflections near the beam are missing, for example behind the beamstop or because they overloaded the detector. Tell the user.

## Resolution limit

Keep the resolution limit that xia2 chose, and do not suggest cutting the data further because I/sigma is low in the outer shells. _Why:_ xia2 stops where CC½ falls to about 0.3. Weak outer shells still carry signal, and refinement weights each reflection by its error, so including them usually improves the model (Karplus and Diederichs, 2012, Science 336, 1030–1033).

Leave the anomalous signal to the later stages. _Why:_ whether weak anomalous signal is useful depends on the phasing method, and is judged there.

## Twinning, pseudotranslation and ice rings

xia2 runs Xtriage on the merged data. Read the `Final verdict` under `Twinning and intensity statistics summary` near the end of `LogFiles/Xtriage.log`, and the line about ice rings earlier in the same file. Clean data give:

```
No significant pseudotranslation is detected.
No twinning is suspected.
No ice ring related problems detected.
```

Copy these lines into `journal.md`. If Xtriage reports twinning or pseudotranslation (translational NCS), tell the user and continue. _Why:_ both change how the later stages should run, and those stages need to know.

## Symmetry

xia2 chooses the symmetry from how well reflections agree under each symmetry operator. The scores are in `LogFiles/AUTOMATIC_DEFAULT_SYMMETRY.log`. Read the table under `Scoring individual symmetry elements`, and the lines after `Best solution`:

```
|   likelihood |   Z-CC |   CC |     N |    | Operator     |
|        0.898 |   9.27 | 0.93 | 50382 | ** | 1 |(0, 0, 0) |
|        0.854 |   8.78 | 0.88 | 49722 | ** | 2 |(0, 1, 0) |

Best solution: C 1 2/m 1
Laue group probability: 0.854
Laue group confidence: 0.777
```

Each line is one operator: the identity (`1`), then rotations such as a 2-fold (`2`) about the axis in brackets. `likelihood` near 1 and stars mean the data have that symmetry. Here the one 2-fold scores well, so C 1 2/m 1 is supported.

- **Every operator near 1 or near 0.** The choice is clear. Continue.
- **An operator in between, roughly 0.3 to 0.7, or with a small `N`.** The choice is uncertain: the true symmetry may be higher or lower. Record which operator, and continue. If an earlier structure of the same molecule exists, "Known crystal forms" below decides. Otherwise, molecular replacement can test the alternatives.

## Known crystal forms

If the `Similar structures` section of `journal.md` lists earlier structures of the same molecule, the user's own or from the PDB, compare the space group and cell in `xia2-summary.dat` with theirs. Compare the cell lengths in any order, since the axes may be labelled differently.

- **Same space group, and every cell length and angle within about 2% of an earlier structure's.** The same crystal form: the crystals are probably isomorphous. Record that structure in `journal.md`, and go next to [topics/isomorphous-refinement.md](isomorphous-refinement.md) instead of molecular replacement. _Why:_ the cell of one crystal form varies by a little between crystals, and the earlier model is already in place.
- **Same cell, and a space group that differs only in its screw axes, such as P 4<sub>1</sub> 2<sub>1</sub> 2 and P 4<sub>3</sub> 2<sub>1</sub> 2.** Also the same crystal form. _Why:_ the diffraction data alone cannot tell such space groups apart, so xia2 may pick either. Go to [topics/isomorphous-refinement.md](isomorphous-refinement.md), which takes the earlier structure's space group.
- **A similar cell, but xia2 chose a space group of lower symmetry than the earlier structure's.** Run xia2 again in a new directory, forcing that structure's space group ([programs/xia2.md](../programs/xia2.md)), and keep both results. _Why:_ xia2 judges the symmetry from these data alone, and only molecular replacement and refinement show which space group is right.
- **A similar cell, but xia2 chose a space group of higher symmetry.** Keep xia2's result, and record the difference.
- **No similar cell.** A new crystal form. Record it and continue.

## If it fails

- If xia2 with DIALS fails and the command `xds_par` exists, run xia2 with the XDS pipeline.
- If xia2 still fails, or you need a lattice that xia2 cannot give, process the data step by step ([programs/dials.md](../programs/dials.md)).
- If a later stage fails, come back here and try, in turn: leaving out damaged images, a lower resolution limit, and another space group or lattice suggested by that stage.
