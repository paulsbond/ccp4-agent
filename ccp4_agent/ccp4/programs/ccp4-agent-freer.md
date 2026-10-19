# ccp4-agent freer

`ccp4-agent freer` checks the free-R flags of merged data, and converts them to the convention that CCP4 programs expect: 0 for the free set.

Programs write free-R flags in different ways. CCP4 uses values 0 to 19, with 0 free. Phenix uses 0 and 1, with 1 free. Others use 0 and 1, with 0 free. Some CCP4 programs, such as Sheetbend, take 0 as free unless told otherwise, and some cannot be told. _Why convert:_ with Phenix flags, such a program would take 95% of the reflections as the free set.

## Running it

```
ccp4-agent freer <merged.mtz>
```

- It looks for an integer column whose name contains `free` or `test`. If it finds several, it lists them: run it again with `--label <column>`.
- To name the converted file, add `--output <file.mtz>`. Otherwise it is `<name>_freer.mtz`.

## Reading the result

```
Column: R-free-flags
Convention: Phenix (1 is free, 0 is working)
Free reflections: 538 of 11215 (4.8%)
Observed reflections without a flag: 0
Wrote merged_freer.mtz, with R-free-flags replaced by FreeR_flag (0 is free, 1 working).
```

- The free value is the lowest value that fewer than half of the reflections have.
- `Already in the CCP4 convention: use this file as it is.` No file is written.
- `Wrote ...` The new file has the same free set, as `FreeR_flag`, in place of the old column. Use it in all later steps.
- `No free-R flag column` or `All flags are the same: there is no free set`: add flags with Freerflag ([programs/freerflag.md](freerflag.md)).
- `Observed reflections without a flag` above 0: give them flags with Freerflag's `COMPLETE` keyword ([programs/freerflag.md](freerflag.md)), using the converted file if one was written. _Why:_ Servalcat stops with `Error: Missing FREE reflection(s).`
- Tell the user the number and percentage of free reflections. About 5% is usual.
