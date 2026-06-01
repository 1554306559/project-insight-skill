# Project Insight Skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

Project Insight Skill 是一个面向编码 Agent 的项目理解 Skill，用来帮助 Agent 更稳定地阅读陌生代码仓库，并生成结构化的项目分析文档。

它主要面向 Claude Code、Codex、Cursor、Cline、Roo Code 这类编码 Agent。大模型负责理解业务目标、模块职责、核心链路和关键技术实现；本地脚本只负责做轻量辅助，比如扫描项目上下文、整理输出目录、写入结果文件。

## 定位与范围

V1 版本聚焦于一个简单、稳定、适合 Agent 调用的工作流：

- 扫描仓库目录结构
- 识别可能的重要入口文件、配置文件、部署文件和文档
- 帮助 Agent 更快定位关键代码
- 将生成结果统一写入 `docs/project-insight/`
- 可选把 Mermaid 架构图转换为基础 Draw.io 文件

V1 不是一个独立的本地静态分析产品，也不尝试替代大模型的项目理解能力。

## 仓库结构

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

## 工作流程

1. Agent 读取 `SKILL.md`。
2. Agent 对目标仓库运行 `scripts/scan_project.py`。
3. Agent 读取生成的 `project_context.json`，并进一步检查关键文件。
4. Agent 生成以下结果：
   - `project_report.md`
   - `architecture.mmd`
   - `business_flow.mmd`
   - 可选 `analysis_notes.md`
   - 可选 `architecture.drawio`
5. Agent 通过 `scripts/write_outputs.py` 将产物统一写入 `<project_root>/docs/project-insight/`。

## 脚本使用方式

### 扫描项目上下文

```bash
python3 scripts/scan_project.py /path/to/project
python3 scripts/scan_project.py /path/to/project --output /tmp/project_context.json
```

### 写入生成结果

准备一个类似下面的 JSON 文件：

```json
{
  "project_report.md": "# 项目分析报告\n",
  "architecture.mmd": "graph TD\n    A --> B\n",
  "business_flow.mmd": "graph TD\n    Start --> End\n"
}
```

然后执行：

```bash
python3 scripts/write_outputs.py /path/to/project --payload /path/to/outputs.json
```

### Mermaid 转 Draw.io

```bash
python3 scripts/mermaid_to_drawio.py architecture.mmd architecture.drawio
```

## 开发与测试

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

当前实现仅依赖 Python 标准库，目的是让这个仓库在常见 Agent 运行环境里尽量保持轻量、开箱即用。
