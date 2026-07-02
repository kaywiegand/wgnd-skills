# wgnd-skills

Claude Code skills for bootstrapping, auditing, and packaging data science / analytics projects.

Part of the `wgnd-*` toolchain — pairs with [wgnd-scaffolding](https://github.com/kaywiegand/wgnd-scaffolding)
(deterministic project generator) and [wgnd-toolkit](https://github.com/kaywiegand/wgnd-toolkit)
(EDA/visualization library). Each piece works standalone or together:

```
/project-init → (data project?) → wgnd-scaffolding → wgnd-toolkit (used in notebooks)
      ↓
/project-review  (audit loop)
      ↓
/project-case  (data projects only)
```

## Skills

| Skill | Purpose |
| :--- | :--- |
| `project-init/` | Bootstrap a new project. Asks for name/type, then either writes generic docs (`web`/`tool`/`general`) or delegates to `wgnd-scaffolding` (`data` → DAN/DSC). |
| `project-review/` | Read-only audit of an existing project — structure, README quality, MD-file coherence, git hygiene. |
| `project-case/` | Builds a portfolio case study for a **data** project — story extraction, slide deck (`slides.yaml` → HTML), landing page hub. |

## Setup

These are [Claude Code](https://docs.claude.com/claude-code) skills, plain markdown instruction files.
Clone this repo and register each skill as a slash command — point `~/.claude/commands/*.md`
directly at the skill files, no symlink needed:

```bash
git clone git@github.com:kaywiegand/wgnd-skills.git
ln -s "$(pwd)/wgnd-skills/project-init/project-init.md" ~/.claude/commands/project-init.md
ln -s "$(pwd)/wgnd-skills/project-review/project-review.md" ~/.claude/commands/project-review.md
ln -s "$(pwd)/wgnd-skills/project-case/project-case.md" ~/.claude/commands/project-case.md
```

Each skill resolves a `SKILL_ROOT` (the folder containing the skill file itself, for its own
`scripts/`/`templates/`) and, where genuinely external, a `WORKSPACE_ROOT` (the workspace it's
invoked from) and `SCAFFOLDING_ROOT` (the `wgnd-scaffolding` checkout) at runtime from context —
no hardcoded paths.

## Structure

```
project-init/
  project-init.md
project-review/
  project-review.md
  portfolio-readme-template.md
project-case/
  project-case.md              ← entry point, modes: check|story|slides|report|full|audit-communication
  build-pipeline.md            ← technical reference: slides.yaml → JSON → HTML build chain
  case-standards.md            ← quality bar / machine-checkable criteria
  communication-concept.md     ← audience segmentation, artifact-per-audience matrix
  portfolio-check-template.md  ← copied into a project as PORTFOLIO_CHECK.md
  portfolio-summary-template.md
  preparation-workflow.md      ← human playbook: audit → triage → prep → QA → publish
  scripts/                     ← build scripts (slides.yaml → JSON/HTML/MD, mechanical)
  templates/                   ← shared slide/hub design (HTML/CSS)
```
