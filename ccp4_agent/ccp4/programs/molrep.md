# MOLREP

MOLREP places a search model in the unit cell by molecular replacement: a rotation function finds its orientation, and a translation function its position.

## Contents

- Running it
- Reading the result
- Several copies
- Space group
- Adding a model to one already placed
- Translational NCS

## Running it

Make a new directory for each run and run MOLREP from inside it. _Why:_ it writes `molrep.pdb`, `molrep.xml` and other files with fixed names into the current directory, and a second run overwrites them.

1. The model must be a PDB file. To convert an mmCIF file, run `gemmi convert model.cif model.pdb`. _Why:_ MOLREP stops with `Fortran runtime error: Bad value during integer read` on mmCIF files.
2. List the columns of the data with `gemmi mtz` ([programs/gemmi-mtz.md](gemmi-mtz.md)), and write a keyword file `molrep.inp` naming the amplitudes and their sigmas. For `DataFiles/AUTOMATIC_DEFAULT_free.mtz` from xia2:
   ```
   LABIN F=F SIGF=SIGF
   ```
   _Why:_ without `LABIN`, MOLREP takes the first amplitude column in the file. That may be the wrong data, such as a heavy-atom derivative, and then the solution is wrong.
3. Run it:
   ```
   molrep -f <data.mtz> -m <model.pdb> -k molrep.inp > molrep.log
   ```

If the model is a homologue, with a sequence different from your crystal's, add `-s chain1.fasta`, a FASTA file with the one sequence of the chain that the model represents. MOLREP aligns it with the model, trims and mutates the model to match, and writes the edited model to `align.pdb`. The log gives the identity, as in `Alignement: identity =    29.89`. _Why:_ the edited model is closer to the crystal's structure, and refines better.

Leave `-s` out if the model has the same sequence as your crystal, such as an earlier structure of the same molecule or a predicted model. _Why:_ there is nothing to edit, and at 100% identity MOLREP treats the model as exact (the log says `Sim,Badd          :    1.000`). In a test, a domain in a different conformation from the crystal was then not found, but was found without `-s`.

A run takes a few minutes.

## Reading the result

`molrep.xml` summarises the run:

```
Message <err_message>normal termination</err_message>
nmon_solution <n_solution>         2</n_solution>
mr_score <mr_score>    0.4196</mr_score>
mr_zscore <mr_zscore>    9.9330</mr_zscore>
```

- `n_solution` is the number of copies placed. If it is 0, the end of the log says `WARNING: no solution was found.` and there is no `molrep.pdb`.
- `mr_score` is the correlation of the placed model with the data, multiplied by a packing score that penalises clashes with symmetry copies and other copies. The log gives the two parts as `Final CC` and `Packing_Coef`, which is 1 when nothing clashes. `mr_zscore` is the height of the translation function peak above the noise, called TF/sig in the log.

`molrep.log` has a line for each copy placed, under `Nmon RF  TF`. `TF/sg` is TF/sig, and `Score` is the score so far, as for `mr_score`:

```
  Nmon RF  TF   theta    phi     chi   tx     ty     tz     TF/sg  wRfac  Score
    1   3   1   72.80   46.19  167.56  0.135  0.221  0.000   6.85  0.566  0.313
    2   1   1  149.66  132.02   48.33  0.171  0.340 -0.370   9.93  0.527  0.420
```

The contrast is the last number in the `Cntrst` column of the table that ends just above the last `--- Summary (V2) ---`. It says how far the best solution stands out from the others. The MOLREP documentation reads it as: above 3, certainly a solution; 2, a solution; 1.5, possibly one; 1.3, probably not. In the summary below that line, several of the top rows with nearly the same `tx`, `ty` and `tz` are also a good sign: different rotation peaks led to the same place.

The output model is `molrep.pdb`, with each copy as a chain, `A`, `B` and so on. Its space group is the one searched. If two copies form a dimer, MOLREP also writes them to `molrep_dimer.pdb`, and the log says `you can find this dimer in molrep_dimer.pdb`.

These scores are guides. Only refinement shows whether the solution is right.

## Several copies

MOLREP estimates the number of copies from the volume of the model, assuming about 50% solvent, and the log says `INFO: program will use NMON =   3`. If the cell contents give a number, set it with a line in `molrep.inp`:

```
NMON 2
```

MOLREP places one copy at a time, keeping those already placed. If it cannot place them all, it keeps the copies it found, says `WARNING: program can not improve current model` and `result is "molrep.crd" with     2 monomers`, and `n_solution` gives the number found.

## Space group

The rotation function depends only on the point group, but the translation function depends on the screw axes. To compare all space groups with the data's point group, such as P 6<sub>1</sub> 2 2 and P 6<sub>5</sub> 2 2, or P 2 2 2 and P 2<sub>1</sub> 2<sub>1</sub> 2<sub>1</sub>, run MOLREP with this line in `molrep.inp`:

```
SG ALL
```

It writes no `molrep.pdb`. The log ends with a table:

```
 |        Nsg     sg                        Score  TF/sig|
 |    1  178   P 61 2 2                     0.161  6.242 |
 |    2  177   P 6 2 2                      0.161  6.242 |
 |    3  179   P 65 2 2                     0.347 19.515 |
 |    4  180   P 62 2 2                     0.200  9.062 |
```

The first row is the data's own space group. Choose the row with the highest TF/sig, and run MOLREP again in a new directory with its `Nsg` number in `molrep.inp`:

```
NOSG 179
```

`molrep.pdb` then has the new space group. Record it in `journal.md`, and tell the user. Change the space group of the data file to match, with Reindex or by processing the data again, as Reindex's page says ([programs/reindex.md](reindex.md)). _Why:_ otherwise Servalcat refines in the model's space group, but warns `space group mismatch between model and mtz`, and later steps read the old space group from the data. In tests, the row for P 6 2 2 repeated the numbers of the first row: ignore such a row.

## Adding a model to one already placed

To search for a second domain, or another component of a complex, keep the placed model fixed with `-mx`, and search for one copy of the new model:

```
molrep -f <data.mtz> -m <domain2.pdb> -mx <placed.pdb> -k molrep.inp > molrep.log
```

with `NMON 1` in `molrep.inp`, and the `LABIN` and `NOSG` lines of the earlier run. Add `-s` for a homologue, as in "Running it". `molrep.pdb` then holds the fixed model and the new one, as the next chain. _Why search by domains:_ a model whose domains are arranged differently from the crystal can fail as a whole, while each domain fits on its own.

## Translational NCS

MOLREP checks the data for translational NCS, copies related by a translation alone. When it finds it, the log says:

```
 INFO: pseudo-translation was detected.
        Peak 1: trans.vector /frac/:         0.209         0.000         0.487
```

and MOLREP then places copies in pairs related by that vector. No keyword is needed. Record the vector in `journal.md`.
