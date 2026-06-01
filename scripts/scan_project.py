from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    "docs/project-insight",
}
IMPORTANT_FILE_NAMES = {
    "README",
    "README.md",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "package.json",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Cargo.toml",
    "pyproject.toml",
    "requirements.txt",
    "Makefile",
}
ENTRYPOINT_NAMES = {
    "main.py",
    "main.go",
    "main.rs",
    "main.ts",
    "main.js",
    "index.ts",
    "index.js",
    "server.ts",
    "server.js",
    "manage.py",
}
CONFIG_EXTENSIONS = {".yaml", ".yml", ".toml", ".ini", ".json", ".env"}
DOC_EXTENSIONS = {".md", ".mdx", ".rst"}
DEPLOY_MARKERS = {"deploy", "k8s", "helm", "docker", "compose"}
SOURCE_EXTENSIONS = {
    ".py",
    ".go",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".java",
    ".kt",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".swift",
}


def should_ignore(path: Path) -> bool:
    parts = path.parts
    for part in parts:
        if part in IGNORED_DIRECTORIES:
            return True
    return False


def is_deploy_file(relative_path: Path) -> bool:
    text = relative_path.as_posix().lower()
    return any(marker in text for marker in DEPLOY_MARKERS) or relative_path.name in {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
    }


def is_config_file(relative_path: Path) -> bool:
    return relative_path.suffix.lower() in CONFIG_EXTENSIONS or "config" in relative_path.as_posix().lower()


def is_doc_file(relative_path: Path) -> bool:
    return relative_path.suffix.lower() in DOC_EXTENSIONS


def is_entrypoint(relative_path: Path) -> bool:
    return relative_path.name.lower() in ENTRYPOINT_NAMES


def default_output_path(project_root: Path) -> Path:
    return project_root / "docs" / "project-insight" / "project_context.json"


def scan_project(project_root: str | Path, output_path: str | Path | None = None) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Project root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Project root is not a directory: {root}")

    extension_counter: Counter[str] = Counter()
    main_directories: set[str] = set()
    important_files: set[str] = set()
    entrypoints: set[str] = set()
    config_files: set[str] = set()
    deploy_files: set[str] = set()
    doc_files: set[str] = set()

    for path in root.rglob("*"):
        if should_ignore(path.relative_to(root)):
            continue

        relative_path = path.relative_to(root)
        if path.is_dir():
            if relative_path.parts:
                main_directories.add(relative_path.parts[0])
            continue

        suffix = path.suffix.lower()
        if suffix in SOURCE_EXTENSIONS:
            extension_counter[suffix] += 1

        if path.name in IMPORTANT_FILE_NAMES or relative_path.parts[0] in {"configs", "config", "deploy", "docs"}:
            important_files.add(relative_path.as_posix())

        if is_entrypoint(relative_path):
            entrypoints.add(relative_path.as_posix())
        if is_config_file(relative_path):
            config_files.add(relative_path.as_posix())
        if is_deploy_file(relative_path):
            deploy_files.add(relative_path.as_posix())
        if is_doc_file(relative_path):
            doc_files.add(relative_path.as_posix())

    context = {
        "project_root": str(root),
        "main_directories": sorted(main_directories),
        "important_files": sorted(important_files),
        "source_extensions": dict(sorted(extension_counter.items())),
        "candidate_entrypoints": sorted(entrypoints),
        "candidate_config_files": sorted(config_files),
        "candidate_deploy_files": sorted(deploy_files),
        "candidate_doc_files": sorted(doc_files),
    }

    resolved_output = Path(output_path) if output_path else default_output_path(root)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(json.dumps(context, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan a project and generate project insight context.")
    parser.add_argument("project_root", help="Path to the project root to scan.")
    parser.add_argument(
        "--output",
        dest="output_path",
        help="Optional output path for project_context.json. Defaults to docs/project-insight/project_context.json.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    context = scan_project(args.project_root, output_path=args.output_path)
    print(json.dumps(context, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

