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
Clone this repo and point Claude Code at it — e.g. symlink into a workspace's `skills/` directory:

```bash
git clone git@github.com:kaywiegand/wgnd-skills.git
ln -s "$(pwd)/wgnd-skills" /path/to/workspace/skills
```

Each skill resolves a `WORKSPACE_ROOT` (the workspace it's invoked from) and, where relevant, a
`SCAFFOLDING_ROOT` (the `wgnd-scaffolding` checkout) at runtime from context — no hardcoded paths.

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
