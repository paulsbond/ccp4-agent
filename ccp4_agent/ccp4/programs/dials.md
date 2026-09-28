# DIALS

Run the DIALS programs one at a time when you need control that xia2 does not give: choosing a lattice, or processing several lattices.

## Contents

- One lattice
- Choosing a lattice
- Several lattices

## One lattice

Make a directory called `dials` in your working directory and run every command from inside it.

1. Import the images:
   ```
   dials.import <images>
   ```
   Check that `num images` in the output is the number you expect and that it reports `sweep: 1`.
2. Find spots:
   ```
   dials.find_spots imported.expt
   ```
3. Index:
   ```
   dials.index imported.expt strong.refl
   ```
   Read `% indexed` from the last table in the output.
4. If indexing fails or indexes fewer than 50% of spots, search for the beam centre and index again. _Why:_ a low fraction suggests a wrong beam centre, several crystals in the beam, or a wrong cell.
   ```
   dials.search_beam_position imported.expt strong.refl
   dials.index optimised.expt strong.refl
   ```
   If the search prints `Sorry: No solutions found`, or indexing still fails or indexes fewer than 50%, go to Several lattices.
5. Refine. To choose a lattice, go to Choosing a lattice instead.
   ```
   dials.refine indexed.expt indexed.refl
   ```
6. Integrate:
   ```
   dials.integrate refined.expt refined.refl
   ```
7. Find the symmetry:
   ```
   dials.symmetry integrated.expt integrated.refl
   ```
8. Scale:

   ```
   dials.scale symmetrized.expt symmetrized.refl
   ```

   Read the limit from the line starting `Resolution limit suggested` in the output. If there is no such line, CC½ stays above 0.3 to the edge of the data: skip step 9.

   To leave out images, add `exclude_images="0:<first>:<last>"` to this command and the next, for example `exclude_images="0:50:55"`.

9. Scale again, cutting the data at that limit:
   ```
   dials.scale symmetrized.expt symmetrized.refl d_min=<limit>
   ```
   _Why:_ the suggested limit is where CC½ falls to 0.3, which is DIALS's default choice of resolution limit.
10. Merge and export:
    ```
    dials.merge scaled.expt scaled.refl
    dials.export scaled.expt scaled.refl
    ```
    Copy the summary table at the end of the `dials.scale` output into `journal.md`. Use `merged.mtz` in the later stages. It holds merged intensities, amplitudes and a free-R flag. `scaled.mtz` holds unmerged intensities.

## Choosing a lattice

After indexing in One lattice, list the possible lattices:

```
dials.refine_bravais_settings indexed.expt indexed.refl
```

In the table, find the row whose `lattice` column is the lattice you need, and note its `Solution` number `<n>` and its `cb_op`. If `cb_op` is `a,b,c`, refine directly:

```
dials.refine bravais_setting_<n>.expt indexed.refl
```

Otherwise, reindex first and then refine:

```
dials.reindex indexed.refl change_of_basis_op=<cb_op>
dials.refine bravais_setting_<n>.expt reindexed.refl
```

Then continue from step 6 of One lattice.

## Several lattices

Several crystals in the beam give many spots that no single lattice explains, so indexing fails or indexes few of them.

Give the unit cell and a space group if you know them, for example from an earlier dataset of the same crystal form, and ask the user if you do not. _Why:_ without them, DIALS can report a wrong cell and invent lattices from a few stray spots. Give the space group without screw axes, for example `P222` for `P212121`.

1. Index several lattices, with the detector and beam fixed:
   ```
   dials.index imported.expt strong.refl max_lattices=<max> space_group=<space group> unit_cell=<a>,<b>,<c>,<alpha>,<beta>,<gamma> detector.fix=all beam.fix=all
   ```
   Set `<max>` to the most lattices you expect. DIALS stops when it finds no more. Read the number of reflections for each lattice from the `model <n> (<count> reflections)` lines after `Refined crystal models`. A lattice with far fewer reflections than the others is probably a few stray spots rather than a crystal: tell the user.
2. Refine with outlier rejection suited to several lattices:
   ```
   dials.refine indexed.expt indexed.refl outlier.algorithm=tukey
   ```
3. Continue from step 6 of One lattice.
