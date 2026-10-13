# gemmi mtz

`gemmi mtz` describes an MTZ file: where it came from and what it holds.

## Running it

```
gemmi mtz <file.mtz>
```

## Reading the result

For example, for merged data from xia2:

```
Title: From dials.merge.bat
Dataset    1   AUTOMATIC > DEFAULT > NATIVE:
        cell  112.831 53.0996 44.4068      90 103.05     90
  wavelength  0.9126
Number of Batches = 0
Resolution: 1.63 - 54.96 A
Space Group: C 1 2 1
 Column        Type  Dataset          Min        Max
 FreeR_flag      I       0              0         19
 IMEAN           J       1       -5.92707     1602.8
 F               F       1       0.207272    39.9845
History (5 lines):
 From XIA2 3.21.1, run on 12/10/2026 at 17:15:44
 From FREERFLAG 12/10/2026 18:15:44 with fraction 0.050
```

- `Title` and `History` name the programs that made the file, with versions and dates. Some programs write no history.
- Each dataset has its own cell and wavelength.
- Column types: `J` is an intensity, `F` an amplitude, `Q` a sigma, `I` an integer such as the free-R flag, `P` a phase.
- A free-R flag column whose `Min` and `Max` are equal has no free set.

## Merged or unmerged

- **Merged:** `Number of Batches = 0`, and one intensity or amplitude for each reflection, as in the example above.
- **Unmerged:** `Number of Batches` is the number of images, and the columns include `BATCH` (the image of each measurement) and `M/ISYM`, for example:

```
Number of Batches = 400
 M/ISYM          Y       1              1          4
 BATCH           B       1              1        400
 I               J       1       -26.5264    1654.19
 SIGI            Q       1       0.124751    45.7057
```

Unmerged data are for programs that scale or check measurements image by image. Phasing and refinement (usually) need merged data.
