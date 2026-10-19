# Isomorphous refinement

Also called phasing by Fourier synthesis: the phases come from the earlier structure, refined against the new data.

## When to use

Data processing found the same crystal form as an earlier structure of the same molecule, as in "Known crystal forms" in [topics/data-processing.md](data-processing.md). This is common for point mutants and for crystals soaked or co-crystallised with ligands. Refine the earlier structure against the new data directly, and do not run molecular replacement. _Why:_ the model is already in place, and molecular replacement can put it at a different but equivalent origin, which makes comparison with the earlier structure harder.

## Inputs

- The merged data from data processing: `DataFiles/AUTOMATIC_DEFAULT_free.mtz` from xia2.
- The earlier structure, as a coordinate file, and its entry in the `Similar structures` section of `journal.md`.
- Optionally, the earlier structure's own data with its free-R flags.

## Steps

1. Remove waters and ligands from the earlier structure with `gemmi convert` ([programs/gemmi-convert.md](../programs/gemmi-convert.md)), writing `start.cif`. _Why:_ they belong to the earlier crystal. Waters and ligands are added back later where the new maps show them, so that the maps are not biased towards the earlier crystal.
2. Compare `start.cif` with `contents.fasta` using `ccp4-agent model` ([programs/ccp4-agent-model.md](../programs/ccp4-agent-model.md)), and record in `journal.md` each `Mutation` line. These residues differ between the model and your crystal, and need rebuilding after refinement.
3. Check the indexing of the data against the model with Pointless, as in "Indexing" below.
4. Refine with Servalcat ([programs/servalcat.md](../programs/servalcat.md)), with `reindexed.mtz` from step 3 and `start.cif`. If you have the earlier structure's data with its free-R flags, add them too.
5. Judge the result, as in "Did it work" below.
6. Tell the user the R values, and which residues need rebuilding and which ligands to look for, then continue to the next stage with the refined model and `refined.mtz`.

## Indexing

Check the indexing of `DataFiles/AUTOMATIC_DEFAULT_free.mtz` against `start.cif` as the reference model with Pointless ([programs/pointless-reference.md](../programs/pointless-reference.md)), writing `reindexed.mtz`. _Why:_ in some space groups, such as P 3, P 4 or P 6, the same data can be indexed in two or more ways that are equally valid on their own, so data processing picks one at random, and only the earlier structure shows which way matches it. `reindexed.mtz` is indexed to match the model and takes the model's space group, which also settles space groups that the data alone cannot tell apart, such as P 4<sub>1</sub> 2<sub>1</sub> 2 and P 4<sub>3</sub> 2<sub>1</sub> 2.

Read the CC of each line of the table at the end of the log:

- **CC of the first line clearly above the others, which are near 0.** The data and the model match. Continue with `reindexed.mtz`.
- **CC of the first line low, and close to the others.** The crystals are probably not isomorphous with the earlier structure. Refine anyway in step 4, as only refinement shows it clearly, and judge it there.

## Did it work

Read the `Rwork` and `Rfree` columns of Servalcat's table of statistics against cycle ([programs/servalcat.md](../programs/servalcat.md)).

- **R well below 0.59 at cycle 0, and falling.** The model fits: the crystals are isomorphous. Continue.
- **R near 0.59 at cycle 0, and hardly changing.** The model does not fit. _Why:_ an unrelated model gives R near 0.59 (Wilson, 1950, Acta Cryst. 3, 397–398). Check that you used `reindexed.mtz`. If you did, the crystals are not isomorphous: record that and go to molecular replacement with the earlier structure as the search model.

## R-free

If you refine the earlier structure against a new free set, R-free is lower than it should be. _Why:_ the earlier structure was refined against the reflections now in the new free set. If the earlier structure's data with its free-R flags are available, use them ([programs/servalcat.md](../programs/servalcat.md)). Otherwise, record in `journal.md` that R-free is biased, and tell the user.

## If it fails

- If Pointless stops with `different Laue symmetry to reference set`, the data and the model are not the same crystal form. Record it and go to molecular replacement with the earlier structure as the search model.
