# ccp4-agent batches

`ccp4-agent batches` shows how data quality changes with image number, to find damaged images and radiation damage.

## Running it

```
ccp4-agent batches <unmerged.mtz>
```

- `<unmerged.mtz>` is scaled, unmerged data, such as `DataFiles/AUTOMATIC_DEFAULT_scaled_unmerged.mtz` from xia2.
- It splits the sweep into 10 ranges of images. To change that, add `--ranges <n>`.

## Reading the result

```
By image range (medians):
 first_image  last_image  i_over_sigma  rmerge
           1          40         7.762   0.110
          41          80         7.083   0.095
 ...
         361         400         5.402   0.125

Images with Rmerge above 2 times the median (0.106) or I/sigma below 1/2 of the median (5.3):
       observations  i_over_sigma  rmerge
image
398             426         3.913   0.223
399             372         5.348   0.228
```

- The first table gives, for each range of images, the median I/sigma and Rmerge of its images. Rmerge for one image compares its reflections with other measurements of the same reflections.
- The second table lists single images that stand out from the rest, with the number of reflections on each. `none` means no image stands out. _Why the factor of 2:_ it is a reference point that picks out images clearly worse than the rest, not a test of good enough.
