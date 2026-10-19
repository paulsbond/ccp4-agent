# Cell contents

Sections: When to use, Inputs, Steps, What to ask, The sequence as crystallised, Copies and oligomeric state, Checking against UniProt, If it fails.

## When to use

After [topics/user-files.md](user-files.md), before any other step, whether you are solving a whole structure or doing a single step. Skip it only if `journal.md` already has a `Cell contents` section. _Why:_ what is in the crystal decides what the later stages search for and build.

## Inputs

What the user may have, in any combination:

- Sequence files. FASTA has a line starting with `>`, then the sequence. PIR has a line such as `>P1;name`, a description line, then the sequence ending in `*`.
- UniProt accessions, such as `P00918`. These give the full-length natural protein, which is rarely exactly what was crystallised.
- Coordinate files of this molecule, listed in the `Files and experiments` section of `journal.md`.
- A description: which residues, tags, mutations, partners, ligands.

## Steps

Asking needs no CCP4. Run the `ccp4-agent` commands below the way [topics/ccp4-setup.md](ccp4-setup.md) describes for CCP4 commands.

1. Ask the user the questions in "What to ask" below, in one message. If they do not know an answer or want to skip it, record that and continue with what you have.
2. Turn what they give you into the sequence of each chain as crystallised, as in "The sequence as crystallised" below.
3. Write `contents.fasta` in your working directory with your file-writing tool: one record for each different polymer chain, as crystallised, with a short name on the `>` line. It holds the raw sequences only. _Why:_ later programs read sequences from it, and FASTA has no place for anything else. Some programs need the contents in another form, such as a sequence repeated for each copy or a file that gives the number of copies; their program pages say how to write it from `contents.fasta` and `journal.md`.
4. If you have a UniProt accession, check the construct against it, as in "Checking against UniProt" below.
5. Add a `Cell contents` section to `journal.md` with everything that is not a raw sequence: each chain and where its sequence came from, the tags and mutations, the ratio of chains and the oligomeric state as hypotheses (see "Copies and oligomeric state" below), the expected ligands, metals, cofactors and glycosylation, and the crystallisation conditions.
6. Show the user the sequences in `contents.fasta` and the other expected contents, and ask them to confirm. Correct anything they point out, then continue.

## What to ask

Ask for the contents of the crystal, not of the gene:

- The sequence of every macromolecule in the crystal, as the construct that was expressed or synthesised: a sequence file, a UniProt accession with the residue range, or typed out.
- Any tag, and whether it was cleaved off before crystallisation. If it was, which residues the cleavage left on the protein.
- Any mutations, for example `C206S`.
- Partners in a complex, protein or nucleic acid.
- What they know about the oligomeric state or, for a complex, the ratio of the chains, for example "a trimer in solution" or "1:1".
- Ligands, inhibitors, cofactors and metal ions added or expected, and whether the protein was expressed in eukaryotic cells, which can add glycosylation.
- Selenomethionine or other heavy atoms, which matter for experimental phasing.
- The crystallisation and cryoprotection conditions, if known. _Why:_ components such as sulfate, glycerol and ethylene glycol often bind and show up in the density.

## The sequence as crystallised

- Leave out a tag that was cleaved off, but keep any residues the cleavage left behind, for example GS after thrombin or G after TEV protease. _Why:_ they are no longer in the crystal, apart from those residues.
- Keep a tag that was not cleaved, even though it will probably not be seen in the density. _Why:_ it is in the crystal and adds to the mass used to work out how many copies fit in the asymmetric unit, and is sometimes ordered.
- Apply each mutation to the sequence.
- Keep selenomethionine as `M` in the sequence, and note it in `journal.md`.
- If the user has only a coordinate file of this molecule, get its sequences with [programs/ccp4-agent-model.md](../programs/ccp4-agent-model.md), and ask the user whether their construct is the same. _Why:_ a model from another crystal may come from a different construct, so even its full sequence may not be yours.
- Never take the sequence from a file whose sequence is marked `(modelled residues only, gaps not shown)`. Ask the user for the full sequence instead. _Why:_ disordered residues and tags are missing from such a sequence, and the gaps are not marked, so it is not the construct.

## Copies and oligomeric state

Record what the user knows about the oligomeric state and the ratio of the chains as hypotheses, not facts. _Why:_ the number of copies in the asymmetric unit depends on the cell and space group, so it is estimated only after data processing, and a molecule can pack differently in the crystal from how it behaves in solution. Only the solved structure settles it.

If the user does not know, record that. Do not guess a number of copies at this stage.

## Checking against UniProt

Compare `contents.fasta` with the UniProt entry using `ccp4-agent uniprot` ([programs/ccp4-agent-uniprot.md](../programs/ccp4-agent-uniprot.md)). It lists how each record differs from UniProt.

- **Extra residues at either end.** Usually a tag or leftover residues from a cleaved one. Check them against what the user said about tags.
- **A mutation, an insertion or missing residues that the user did not mention.** Ask the user about each one. _Why:_ it may be an unmentioned mutation, a different isoform or species, or a typing error.
- **`Too different to list changes` or `No alignment`.** The accession or the sequence is wrong. Ask the user.
- **Only an accession, no construct.** Show the user the `Processing` lines and ask which residues were expressed. If they do not know, use the residues of the `Chain` line, and say so in `journal.md`.

Add the cofactors and binding-site ligands to the expected contents, and ask the user whether they were present.

## If it fails

- If `ccp4-agent uniprot` cannot reach UniProt, ask whether they can give the sequence another way, record the contents from what they gave you, and continue.
- If the user cannot give any sequence, record that and continue. Tell the user that molecular replacement and model building will need one.
