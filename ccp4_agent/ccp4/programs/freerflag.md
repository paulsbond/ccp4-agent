# Freerflag

Freerflag adds free-R flags to merged data: a column `FreeR_flag` that sets aside a random 5% of reflections, which refinement never fits, to give R-free. Every merged data file needs one before any refinement.

## When to use it

Add flags as soon as you have merged data without them. Merged data from Aimless have none. For any other merged file, check first with `ccp4-agent freer` ([programs/ccp4-agent-freer.md](ccp4-agent-freer.md)), which recognises flags written by other programs and converts them for CCP4. _Why:_ without a free set, nothing shows whether refinement improves the model or only fits noise.

Never replace flags that are already there. _Why:_ a model refined against those data has been fitted to every reflection outside the old free set, so R-free with new flags would be too low. If an earlier structure of the same crystal form has flags of its own, use those instead, as in [topics/isomorphous-refinement.md](../topics/isomorphous-refinement.md).

## Running it

Write a keyword file `freerflag.inp` containing only the line `END`, then:

```
freerflag HKLIN <merged.mtz> HKLOUT <merged_free.mtz> < freerflag.inp > freerflag.log
```

Always give the keyword file. _Why:_ without one, Freerflag waits for keywords to be typed and never finishes.

Use `<merged_free.mtz>` in all later steps.

## Reading the result

The run succeeded if `freerflag.log` says `FREERFLAG:  Normal termination` near the end. The new column has values 0 to 19, each on about 5% of the reflections, as the table after `Reflection flag =:` shows. Reflections with flag 0 are the free set, and Servalcat finds it itself.

## Completing existing flags

If some reflections have no flag, as `ccp4-agent freer` reports, give them flags and keep the others with this `freerflag.inp`:

```
COMPLETE FREE=FreeR_flag
END
```

The log says `The number of missing flags =` with their number.
