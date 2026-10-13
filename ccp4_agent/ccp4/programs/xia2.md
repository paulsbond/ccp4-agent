# xia2

xia2 runs a complete data-processing pipeline and makes its own choices of lattice, space group and resolution limit.

## Running it

Make a new directory for each run and run xia2 from inside it:

```
xia2 pipeline=dials image=<images>
```

- `<images>` is the NeXus master file ending in `.nxs`, or the first image file of a sweep. xia2 finds the other images itself.
- On Windows, add `read_all_image_headers=False` when giving an image file. _Why:_ without it, xia2 can stop at once with `Error: no sweeps found`, because reading the image headers in parallel fails there.
- To force a space group, add `space_group=<space group>`, written without spaces, for example `space_group=P43212`, or `space_group=P1211` for `P 1 21 1`.
- To process only some images, add the first and last image number to the image file: `image=<first image file>:<first>:<last>`, for example `image=insulin_1_001.img:1:40`.
- To use XDS instead of DIALS, replace `pipeline=dials` with `pipeline=3dii`. This needs XDS installed, which you can check by looking for the command `xds_par`. XDS cannot read `.nxs` data unless an HDF5 plugin is installed.

## Reading the result

- The run succeeded if the output ends with `Status: normal termination`.
- If the XDS pipeline stops with `Error: HDF5 input with no converter for XDS` or `Error: installed XDS expired`, XDS cannot process these data. Tell the user which error it was, and use `pipeline=dials`.
- `xia2-summary.dat` gives the space group, the unit cell, and the resolution, completeness, multiplicity, I/sigma and CC half. Its three columns are overall, lowest-resolution shell and highest-resolution shell.
- `DataFiles/AUTOMATIC_DEFAULT_free.mtz` holds merged intensities, amplitudes and a free-R flag.
- `DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.mtz` holds unmerged intensities.
- `LogFiles/AUTOMATIC_DEFAULT_NATIVE_merging-statistics.txt` gives the statistics for each resolution shell, including completeness in the `%comp` column.
- `LogFiles/Xtriage.log` is the Xtriage analysis of the merged data, including twinning, pseudotranslation and ice rings.
