---
name: project-insight
description: Analyze a software repository from a business and architecture perspective. Use this skill when asked to understand a codebase, summarize business functions, identify technology stack, extract key implementation flows, generate project documentation, or create Mermaid/Drawio architecture diagrams.
---

# Project Insight Skill

Use this skill when the user asks to understand, summarize, document, explain, or visualize a software project.

This skill is designed for coding agents such as Claude Code, Codex, Cursor Agent, Cline, and Roo Code.

The scripts in this skill are helpers only. They scan project structure, collect context, and write generated artifacts. They do not replace model-based reasoning.

## Workflow

1. Run `scripts/scan_project.py` on the target repository.
2. Read the generated `project_context.json`.
3. Inspect the most important files identified by the scanner.
4. Infer the project type, business goal, technology stack, module responsibilities, and core flows.
5. Generate:
   - `project_report.md`
   - `architecture.mmd`
   - `business_flow.mmd`
6. Save all outputs under:
   - `<project_root>/docs/project-insight/`
7. Optionally generate:
   - `architecture.drawio`
   - `analysis_notes.md`

## Analysis Rules

- Do not explain every file.
- Do not rewrite the README.
- Focus on business capabilities and key implementation flows.
- Extract only the most important 1-3 business flows.
- Explain technologies only in the context of this project.
- Always separate confirmed facts from inferred conclusions.
- Include related files for important claims.
- If confidence is low, explicitly state what evidence is missing.

## Output Rules

Default output directory:

`<project_root>/docs/project-insight/`

Never scatter generated files in the project root.

Required outputs:

- `project_report.md`
- `architecture.mmd`
- `business_flow.mmd`

Optional outputs:

- `architecture.drawio`
- `project_context.json`
- `analysis_notes.md`

## Helper Scripts

### `scripts/scan_project.py`

Responsibilities:

- scan the project file tree
- filter noisy directories
- identify important files
- count major source extensions
- generate `project_context.json`

Not responsible for:

- business understanding
- architecture explanation
- report writing

### `scripts/write_outputs.py`

Responsibilities:

- create `docs/project-insight/`
- write agent-generated Markdown, Mermaid, JSON, and Draw.io files
- keep outputs in a single bundle

### `scripts/mermaid_to_drawio.py`

Responsibilities:

- convert a Mermaid architecture graph into a basic editable Draw.io XML file
- keep the output simple and openable

