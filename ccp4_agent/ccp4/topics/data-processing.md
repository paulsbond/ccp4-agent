# Data processing

## When to use

You have diffraction images from a rotation sweep and need merged intensities in an MTZ file. A later stage may also send you back here: to use a different space group, lattice or resolution limit, or to leave out images.

## Inputs

- The images: the NeXus master file ending in `.nxs` for Eiger data, or the image files of the sweep.
- Optionally, a space group, lattice or image range from a later stage.

## Steps

1. Process the images with xia2 and the DIALS pipeline, as described in [programs/xia2.md](../programs/xia2.md). If a later stage gave you a space group, pass it to xia2.
2. Copy `xia2-summary.dat` into `journal.md`.
3. Check the data against image number, as in "Quality against image number" below.
4. Explain the completeness and resolution, as in "Completeness" and "Resolution limit" below.
5. Check for twinning, pseudotranslation and ice rings, as in "Twinning, pseudotranslation and ice rings" below.
6. Tell the user what you found in steps 3 to 5, and continue to the next stage with `DataFiles/AUTOMATIC_DEFAULT_free.mtz`. There is no fixed standard for good enough: the next stages show whether the data suffice.

## Quality against image number

Run:

```
ccp4-agent batches DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.mtz
```

It prints Rmerge and I/sigma for ranges of images, then lists single images that stand out from the rest.

- **Single images listed.** Something went wrong on those images, for example ice, a shutter fault, or the crystal leaving the beam. Process again without them. For images at the start or end of the sweep, give xia2 an image range. For images in the middle, use DIALS step by step and exclude them when scaling, as described in [programs/dials.md](../programs/dials.md).
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

## If it fails

- If xia2 with DIALS fails and the command `xds_par` exists, run xia2 with the XDS pipeline.
- If xia2 still fails, or you need a lattice that xia2 cannot give, process the data step by step as described in [programs/dials.md](../programs/dials.md).
- If a later stage fails, come back here and try, in turn: leaving out damaged images, a lower resolution limit, and another space group or lattice suggested by that stage.
