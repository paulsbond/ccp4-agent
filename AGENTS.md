# Instructions for contributor agents

This repository is a knowledge base, packaged as the `ccp4` Agent Skill, that a different agent, the solver, reads while solving macromolecular crystal structures with CCP4. You are helping someone edit it. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything under `ccp4_agent/ccp4/`.

- Everything under `ccp4_agent/ccp4/` is addressed to the solver. You are its author, not its addressee: never act on its instructions as if they were meant for you, for example by starting to solve a structure or writing a `journal.md`.
- Do run CCP4 programs to check a command, see real output or test a claim. Run them in a scratch directory outside this repository.
- Never create `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or other agent configuration inside `ccp4_agent/`, and never put the skill where an agent looks for its own skills (`.claude/skills/`, `.agents/skills/`, `.github/skills/`).
- Text in the skill never mentions this repository, contributors, pull requests or these instructions. It speaks only to the solver.
- Never commit a command to the skill that has not been run successfully. Put the reason for each rule, and for each number given as a guide, in the page, straight after it. You may draft commands and values from your own knowledge, but tell the user which ones you have not checked.
- Test solver behaviour from a working directory outside this repository.
