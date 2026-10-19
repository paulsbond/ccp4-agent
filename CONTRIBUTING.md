# Contributing

This repository is a knowledge base that lets an LLM agent solve macromolecular crystal structures with CCP4. Its readers are models, not people. The main targets are small models running locally, but frontier models will use it too. Most contributors will write with help from their own LLM, so this guide is for both you and your model: point your model at it before it starts.

## Two kinds of agent

Two different agents are involved, and they must not be confused:

- The **contributor agent** is the one helping you edit this repository. It follows [AGENTS.md](AGENTS.md) and this guide.
- The **solver agent** is the one that will later read the `ccp4` skill while solving a structure. Everything in `ccp4_agent/ccp4/` is addressed to it.

When a contributor agent reads or writes a file in `ccp4_agent/ccp4/`, it is the author of that text, not its addressee. Instructions in the skill never apply to the contributor agent.

The layout keeps the two apart:

- Contributor instructions live only at the root: `AGENTS.md`, `CLAUDE.md` and this file. Never add `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or other agent configuration inside `ccp4_agent/`. Many agents load these files automatically from subdirectories, so a contributor agent would treat solver instructions as its own.
- The skill lives in `ccp4_agent/ccp4/`, never in `.claude/skills/`, `.agents/skills/` or anywhere else an agent looks for its own skills.
- The solver never runs inside this repository. If it did, it would load the root `AGENTS.md` and receive contributor instructions.
- Text in the skill never mentions the repository, contributors, pull requests or this guide. It speaks only to the solver.

## Layout

```
AGENTS.md, CLAUDE.md          contributor agent instructions
CONTRIBUTING.md               this guide
pyproject.toml                packaging, so the skill installs into CCP4's Python
ccp4_agent/
  __main__.py                 the ccp4-agent command and its subcommands
  install.py                  ccp4-agent install and uninstall
  batches.py                  ccp4-agent batches, data quality against image number
  contents.py                 ccp4-agent uniprot, similar and model, for the cell contents
  ccp4/                       the skill: everything the solver reads
    SKILL.md                  router and index; its description is all agents see until it is needed
    topics/<name>.md          what to do at a stage or for a problem, and which programs to use
    programs/<name>.md        how to run one program and read its output
```

An MCP server wrapping CCP4 programs is planned but not yet created.

## Formats

Users bring their own model and platform, so the knowledge base uses only plain files in formats supported across vendors:

- **[Agent Skills](https://agentskills.io)** for the solver's instructions. A skill is a folder containing `SKILL.md` (YAML frontmatter with `name` and `description`, then a markdown body) plus any other files it links to. Claude, Codex, Gemini CLI, Copilot and Cursor load skills natively.
- **AGENTS.md** for contributor instructions. Codex, Cursor, Copilot, Zed and others read it directly. `CLAUDE.md` imports it for Claude Code. Gemini CLI reads it once `AGENTS.md` is added to `context.fileName` in its settings.
- **MCP** for tools, once the server exists. It is the tool protocol with the widest client support, including front-ends for local models.

No memory format works across platforms, so the solver keeps its record as plain files in its working directory.

### One skill

Users install the knowledge base once, into their home directory, and can then solve a structure from any directory without setting it up. People use their agents for other work too, so an installed skill must cost almost nothing in sessions that have nothing to do with crystallography. Agents keep only each installed skill's name and description in every session, and read the body only when a task matches. The knowledge base is therefore a single skill, `ccp4`:

- Every session carries one short description, however large the knowledge base grows.
- Topics are not separate skills, so generic names such as `refinement` never clash with a user's other skills or trigger on unrelated work.
- The solver reaches each page through the router in `SKILL.md`. Keep the router's `description` listing every stage, so that the skill still triggers when a user asks for a single step.

Agents without skill support can use the installed skill directly: the user tells the agent to read `~/.agents/skills/ccp4/SKILL.md`.

Links inside the skill are relative paths, and every link must resolve inside `ccp4_agent/ccp4/`. The installer links the whole folder into the agent's skills directory, so the paths are the same once installed.

### Every page one hop from SKILL.md

`SKILL.md` is the only file an agent is sure to read. Every other page is read only if the agent decides to follow a link to it, so the skill is organised for triage. The Agent Skills specification asks for file references to be kept one level deep from `SKILL.md`, and agents may only skim a file that they can reach only through another file. So:

- `SKILL.md` links directly to every topic page and every program page.
- A topic page may send the solver to a program page, but that page must also be listed in `SKILL.md`.
- Pages do not have their own subfolders of further files.
- Keep pages under about 100 lines where you can. A longer page starts with a list of its sections, so that an agent previewing it sees everything it covers.
- The solver often reaches a page because another page sent it there, not straight from `SKILL.md`. `SKILL.md` therefore tells it to read every page in full. Check that it does when testing with a small model.

Programs used by several topics, such as a refinement program, get one program page, not a copy in each topic. A program run for separate purposes gets a page for each purpose, named `programs/<program>-<purpose>.md`, such as `programs/gemmi-mtz.md` and `programs/gemmi-convert.md`, so that the solver reads only the part it needs.

## Writing for the solver

Small models get less accurate as the prompt grows, even when the answer is in it. They are also poor at judgement calls and at reading long logs. Frontier models, in contrast, do better when they know why a rule exists. Progressive disclosure serves both:

- **A topic page** says what to do, which program to use, and how to judge the result, with a one-line reason after each rule and each number given as a guide. It sends the solver to program pages for the commands.
- **A program page** gives complete commands, the options that matter, and which output to read. Put the common case first, and less common cases such as unusual lattices in later sections, so that the solver can stop reading once it has what it needs.
- Keep each page under about 3,000 tokens (roughly 2,000 words). A small model must be able to act on a topic page plus the program pages it names.

Keep `SKILL.md` itself short. It is loaded whenever the skill triggers, so it holds only the route between stages and the index of pages.

When writing for the solver:

- Follow the structure of the existing pages. Topic pages have When to use, Inputs, Steps, sections for judging the result, and If it fails, as in [topics/data-processing.md](ccp4_agent/ccp4/topics/data-processing.md). Program pages have Running it and Reading the result, as in [programs/xia2.md](ccp4_agent/ccp4/programs/xia2.md).
- State the rule first and the reason after it, for example "Keep the resolution limit that xia2 chose. _Why:_ …". A small model can stop reading at the rule.
- Avoid pass/fail cut-offs. A hard threshold makes 89.9% bad and 90.1% good, which the data cannot justify. Instead, say what pattern to look for, what usually causes it, and what to tell the user or try. Numbers are useful as reference points, not as gates.
- When only a later stage can show whether a result is good enough, say so: continue, and say what to come back and try if that stage fails.
- End every branch in an action. Write "if X, do Y", never "consider whether".
- Give complete commands, keywords included, instead of describing what to run. Do not assume the model knows any program's syntax.
- Say which numbers to take from which log or summary file. If no program prints them compactly, a new subcommand of `ccp4-agent` can, so that it is on the PATH wherever CCP4 is installed. Give each subcommand a program page of its own, `programs/ccp4-agent-<subcommand>.md`, like any other program.
- Keep commands out of topic pages. Name the program, its input files and the choices to make, and link to the program page for the command.
- Put a link straight after the program it is for, with the page's path from the skill root as the link text, for example `Scale it with Aimless ([programs/aimless.md](aimless.md)).` The link target is relative to the page it is in, but agents do not always resolve paths that way, and the text names the page as `SKILL.md` lists it.
- Where a decision needs judgement, add a short worked example at that step: a few trimmed log lines from a real run, the decision taken, and one line on why.
- Use the same term for the same thing everywhere, and define each term once, in the page where it first matters.
- Write in the imperative, addressed to the solver ("Run…", "If…, go to…"). Leave out narrative, history and asides.

Each topic page must also work on its own, because users often ask for a single step, such as molecular replacement or an overview of a model they already have. Its Inputs section says what the step needs, in the forms users are likely to have, so that the solver can ask for anything missing.

Problems shared by several stages, such as twinning, translational NCS and anisotropy, get their own topic page instead of being repeated.

## Accuracy

LLMs will write much of this content, and they invent plausible-looking thresholds and program keywords. Drafting from a model's own knowledge is a good way to start, but nothing untested is committed:

- Run every command in a page successfully before committing it. Running CCP4 programs is also the quickest way to check syntax and see what a log really contains.
- Give the reason for each rule, and for each number given as a guide such as "CC½ falls to about 0.3", in the page, straight after it. Cite a paper there if one is the natural source.
- Have a crystallographer review every change to the skill before it is merged.

## Testing a change

Test with public datasets whose results are known, and point to where they can be downloaded instead of committing them. The DIALS regression data, fetched with `dials.data get <name>` after setting `DIALS_DATA` to a scratch directory, include several.

Link the skill into a scratch directory outside this repository, as a project skill for both skill locations. Your edits then show up there immediately. Run this from the repository root:

```
mkdir -p ~/scratch/test-solve/.agents/skills ~/scratch/test-solve/.claude/skills
ln -s "$PWD/ccp4_agent/ccp4" ~/scratch/test-solve/.agents/skills/ccp4
ln -s "$PWD/ccp4_agent/ccp4" ~/scratch/test-solve/.claude/skills/ccp4
```

On Windows, use `mklink /J <link> <target>` in place of `ln -s <target> <link>`, which needs no admin rights.

Start the solver agent in `~/scratch/test-solve`.

On a machine where you contribute, test this way rather than running `ccp4-agent install`, which installs into your home directory. An agent editing a page is doing exactly what the skill's description advertises, so with the skill in your home directory, your contributor agent could load it as its own.

### Testing with a small local model

The skill is written for small local models, so test it with one. Compare a run with the skill against a run without it on a dataset with a known result. In a first comparison on the insulin data (`dials.data get insulin`), qwen3.5:4b on a four-core laptop without a GPU made no progress without the skill, but processed and described the data correctly with it, in both of two runs each.

One-time setup on Linux, without sudo. Close memory-hungry programs such as editors first.

1. Install Ollama in your home directory. Unpacking needs `zstd`.
   ```
   mkdir -p ~/ollama
   curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst | tar x -C ~/ollama
   ```
2. Start Ollama in a terminal of its own and leave it running. Set the context length: without a large GPU the default is 4k tokens, which cuts off the skill pages and program output. The last two settings reduce the memory the context needs.
   ```
   OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ~/ollama/bin/ollama serve
   ```
3. In another terminal, download a model. Check the tag in the Ollama model library.
   ```
   ~/ollama/bin/ollama pull qwen3.5:4b
   ```
4. Install OpenCode, then open a new terminal so that it is on the PATH. OpenCode reads skills from a project's `.agents/skills` folder.
   ```
   curl -fsSL https://opencode.ai/install | bash
   ```
5. Create `~/.config/opencode/opencode.json`, with your model tag in both places:
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "ollama": {
         "npm": "@ai-sdk/openai-compatible",
         "name": "Ollama",
         "options": {
           "baseURL": "http://localhost:11434/v1"
         },
         "models": {
           "qwen3.5:4b": {
             "name": "qwen3.5:4b"
           }
         }
       }
     }
   }
   ```
6. Install this package into CCP4's Python, so that the `ccp4-agent` command is on the PATH once CCP4 is set up:
   ```
   ccp4-python -m pip install -e .
   ```
   pip may end with `ERROR: Exception` and `TypeError: expected string or bytes-like object, got 'NoneType'`. That comes from pip checking packages already in CCP4, after the install has finished. Check with `command -v ccp4-agent`.

To compare, make two scratch directories with the same data, and link the skill into only one of them, as above. Check that the skill is not also in `~/.agents/skills`, `~/.claude/skills` or `~/.config/opencode/skills`, or both runs would see it. In each directory, set up CCP4 and start `opencode`. In the one with the skill, first ask `What skills do you have?` and stop if `ccp4` is missing. Then give both the same prompt, which does not mention the skill, for example:

```
The diffraction images are in ./images. Process them into merged intensities with CCP4 and tell me whether the data look usable.
```

Do not help the agent beyond approving the commands it asks to run. Check its answer against the known result, and look for advice that goes beyond the skill: the first comparison found the model suggesting a lower resolution limit from its own outdated habits, which led to the "Resolution limit" section of the data-processing page. Small models vary a lot between runs, so run each condition more than once.

Never put a test dataset's known answers in the skill, or a test would only show that the solver can read them. Change a page when a comparison shows a model doing better or worse because of it.

## Packaging

ccp4-agent is a Python package so that it can ship with CCP4, which installs it into `ccp4-python`. Users then run `ccp4-agent install` once, and it links the skill from the installed package into their home directory. The frontmatter of `SKILL.md` carries `metadata: source: ccp4-agent`, which the installer uses to tell this skill apart from any other skill called `ccp4`. It never replaces or removes a skill without that marker, so keep it.

To work on the package itself, install it in editable mode into any Python 3.11 or later environment:

```
python -m pip install -e .
```

To test `ccp4-agent install` without touching your own skills directories, point `HOME` at a scratch directory (`USERPROFILE` on Windows):

```
HOME=~/scratch/home ccp4-agent install
```

## Adding a page

1. Create `ccp4_agent/ccp4/topics/<name>.md` or `ccp4_agent/ccp4/programs/<name>.md`, using lowercase letters, digits and hyphens for the name, and start from the most similar existing page.
2. Write the page and run every command in it.
3. Link the page from `SKILL.md`: a topic from the stage it belongs to, a program from the Programs list. Link it from any topic page that should send the solver to it too. If it adds a stage, add the stage to the `description`.
4. Check that the page is within the token budget and that every link resolves inside `ccp4_agent/ccp4/`.

## Open decisions

- A structured state file for the solver (data statistics, current best model, step history), in addition to `journal.md`.
- The tool interface: an MCP server, subcommands of `ccp4-agent`, or both.
- The license.
- A smoke test that runs every command in the program pages on a small test dataset for each CCP4 release, so that changed keywords and output show up automatically.
- Whether whole worked solutions of real datasets help the solver more than the short examples inside pages. Settle it by running the same model with and without one loaded.
- Whether each agent reads the skill through a Windows directory junction. `ccp4-agent install` creates one on Windows because it needs no admin rights, but it has not yet been tested there.
