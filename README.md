# ccp4-agent

A knowledge base that lets an LLM agent solve macromolecular crystal structures from X-ray diffraction data with [CCP4](https://www.ccp4.ac.uk). It is written for models, not people. It targets small models running locally, and frontier models can use it too.

## Installing

To make it available to your agent, run:

```
ccp4-agent-install
```

This installs the `ccp4` [Agent Skill](https://agentskills.io) where your agents look for skills, and tells you what to do when CCP4 is updated.

You can then ask your agent to solve a structure from any directory. The skill costs one short description in each session and loads the rest only when you ask for crystallography, so it stays out of the way in your other work.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
