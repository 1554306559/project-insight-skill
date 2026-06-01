from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping


OUTPUT_DIRECTORY = Path("docs") / "project-insight"


def _resolve_output_path(project_root: Path, relative_name: str) -> Path:
    output_root = (project_root / OUTPUT_DIRECTORY).resolve()
    target_path = (output_root / relative_name).resolve()
    if output_root not in target_path.parents and target_path != output_root:
        raise ValueError(f"Refusing to write outside output bundle: {relative_name}")
    return target_path


def write_outputs(project_root: str | Path, outputs: Mapping[str, str]) -> list[str]:
    root = Path(project_root).resolve()
    output_root = root / OUTPUT_DIRECTORY
    output_root.mkdir(parents=True, exist_ok=True)

    written_files: list[str] = []
    for relative_name, content in outputs.items():
        target_path = _resolve_output_path(root, relative_name)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        written_files.append(str(target_path))

    return written_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write project insight outputs into docs/project-insight.")
    parser.add_argument("project_root", help="Path to the project root.")
    parser.add_argument(
        "--payload",
        required=True,
        help="Path to a JSON file mapping output filenames to file content.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload_path = Path(args.payload).resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    written = write_outputs(args.project_root, payload)
    print(json.dumps({"written_files": written}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

