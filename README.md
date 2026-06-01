# Project Insight Skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

Project Insight Skill is an agent-oriented skill for understanding unfamiliar software repositories and producing structured project documentation.

It is designed for coding agents such as Claude Code, Codex, Cursor, Cline, and Roo Code. The model is responsible for reasoning about business goals, module responsibilities, core flows, and technical decisions. Local scripts only provide lightweight support for scanning project context and writing outputs.

## Scope

V1 focuses on a simple, script-assisted skill workflow:

- scan the repository structure
- identify likely entrypoints, config files, deploy files, and docs
- help the agent read the right files
- write generated artifacts into `docs/project-insight/`
- optionally convert Mermaid architecture graphs into a basic Draw.io file

V1 does not attempt to be a standalone static analysis product.

## Repository Layout

```text
project-insight-skill/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── scripts/
│   ├── scan_project.py
│   ├── write_outputs.py
│   └── mermaid_to_drawio.py
├── templates/
│   ├── project_report_template.md
│   ├── architecture_template.mmd
│   └── business_flow_template.mmd
├── examples/
│   ├── backend_project_report.md
│   ├── frontend_project_report.md
│   └── architecture.mmd
└── tests/
```

## Workflow

1. The agent loads `SKILL.md`.
2. The agent runs `scripts/scan_project.py` against the target repository.
3. The agent reads `project_context.json` and inspects the most relevant files.
4. The agent generates:
   - `project_report.md`
   - `architecture.mmd`
   - `business_flow.mmd`
   - optional `analysis_notes.md`
   - optional `architecture.drawio`
5. The agent writes outputs into `<project_root>/docs/project-insight/` through `scripts/write_outputs.py`.

## Script Usage

### Scan Project Context

```bash
python3 scripts/scan_project.py /path/to/project
python3 scripts/scan_project.py /path/to/project --output /tmp/project_context.json
```

### Write Generated Outputs

Prepare a JSON payload like:

```json
{
  "project_report.md": "# Project Report\n",
  "architecture.mmd": "graph TD\n    A --> B\n",
  "business_flow.mmd": "graph TD\n    Start --> End\n"
}
```

Then run:

```bash
python3 scripts/write_outputs.py /path/to/project --payload /path/to/outputs.json
```

### Convert Mermaid to Draw.io

```bash
python3 scripts/mermaid_to_drawio.py architecture.mmd architecture.drawio
```

## Development

Run tests with:

```bash
python3 -m unittest discover -s tests -v
```

The implementation uses only the Python standard library so the repository stays lightweight in common agent environments.

