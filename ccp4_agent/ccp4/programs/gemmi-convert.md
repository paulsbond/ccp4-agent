# gemmi convert

`gemmi convert` writes a copy of a coordinate file, optionally with parts removed.

## Running it

To remove waters and ligands from a model:

```
gemmi convert --remove-lig-wat <model> <new model>
```

- It removes waters, and everything that is not part of a polymer chain, such as ligands and metal ions.
- The input and output can each be PDB or mmCIF, chosen by the file extension.

## Reading the result

It prints nothing when it succeeds. To check the new model, describe it with [programs/ccp4-agent-model.md](ccp4-agent-model.md): its `Ligands` line should say `none`.
