from __future__ import annotations

import argparse
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path


EDGE_PATTERN = re.compile(r"^\s*([A-Za-z0-9_]+)(?:\[[^\]]+\]|\([^)]+\))?\s*-->\s*([A-Za-z0-9_]+)(?:\[([^\]]+)\]|\(\(([^)]+)\)\)|\(([^)]+)\))?\s*$")
NODE_PATTERN = re.compile(r"^\s*([A-Za-z0-9_]+)(?:\[([^\]]+)\]|\(\(([^)]+)\)\)|\(([^)]+)\))?\s*$")


def _parse_mermaid(mermaid_text: str) -> tuple[list[tuple[str, str]], dict[str, str]]:
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str]] = []

    for raw_line in mermaid_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("graph "):
            continue

        edge_match = EDGE_PATTERN.match(line)
        if edge_match:
            source, target, bracket_label, double_circle_label, circle_label = edge_match.groups()
            target_label = bracket_label or double_circle_label or circle_label or target
            nodes.setdefault(source, source)
            nodes.setdefault(target, target_label)
            edges.append((source, target))
            continue

        node_match = NODE_PATTERN.match(line)
        if node_match:
            node_id, bracket_label, double_circle_label, circle_label = node_match.groups()
            nodes[node_id] = bracket_label or double_circle_label or circle_label or node_id

    return edges, nodes


def convert_mermaid_to_drawio(mermaid_text: str, output_path: str | Path | None = None) -> str:
    edges, nodes = _parse_mermaid(mermaid_text)

    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", id="project-insight", name="Architecture")
    model = ET.SubElement(diagram, "mxGraphModel", dx="1200", dy="800", grid="1", gridSize="10")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    node_ids: dict[str, str] = {}
    x = 40
    y = 40
    for index, (node_key, label) in enumerate(nodes.items(), start=2):
        node_ids[node_key] = str(index)
        cell = ET.SubElement(
            root,
            "mxCell",
            id=str(index),
            value=html.escape(label),
            style="rounded=1;whiteSpace=wrap;html=1;",
            vertex="1",
            parent="1",
        )
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width="140", height="60", **{"as": "geometry"})
        x += 180
        if x > 760:
            x = 40
            y += 120

    next_id = len(nodes) + 2
    for source, target in edges:
        edge = ET.SubElement(
            root,
            "mxCell",
            id=str(next_id),
            value="",
            edge="1",
            parent="1",
            source=node_ids[source],
            target=node_ids[target],
            style="endArrow=block;html=1;rounded=0;",
        )
        ET.SubElement(edge, "mxGeometry", relative="1", **{"as": "geometry"})
        next_id += 1

    xml_text = ET.tostring(mxfile, encoding="unicode")
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(xml_text, encoding="utf-8")
    return xml_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert a Mermaid graph into a basic Draw.io XML document.")
    parser.add_argument("input", help="Path to the Mermaid file.")
    parser.add_argument("output", help="Path to write the generated Draw.io XML.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    mermaid_text = Path(args.input).read_text(encoding="utf-8")
    xml_text = convert_mermaid_to_drawio(mermaid_text, output_path=args.output)
    print(xml_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
