"""YAML helpers with graceful fallback for the glossary project.

The project prefers :func:`yaml.safe_load` from PyYAML so values such as
``"Silence alerts: skip postmortems"`` remain plain strings instead of being
parsed as nested dictionaries.  For environments where PyYAML is unavailable
we retain a tiny parser that understands the limited subset of YAML found in
``data/terms``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

try:  # pragma: no cover - exercised implicitly through public helpers
    import yaml
except ModuleNotFoundError:  # pragma: no cover - fallback path
    yaml = None


@dataclass
class SimpleYAMLParser:
    lines: List[str]
    base_indent: int = 0
    index: int = 0

    @classmethod
    def from_text(cls, text: str, base_indent: int = 0) -> "SimpleYAMLParser":
        lines = [line.rstrip("\n") for line in text.splitlines()]
        return cls(lines=lines, base_indent=base_indent, index=0)

    def parse(self) -> Any:
        return self.parse_block(0)

    def parse_block(self, indent: int) -> Any:
        while self.index < len(self.lines):
            line = self.lines[self.index]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                self.index += 1
                continue
            current_indent = self.get_indent(line)
            if current_indent < indent:
                break
            if stripped.startswith("- "):
                return self.parse_sequence(indent)
            return self.parse_mapping(indent)
        return {}

    def parse_mapping(self, indent: int) -> dict:
        result: dict = {}
        while self.index < len(self.lines):
            line = self.lines[self.index]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                self.index += 1
                continue
            current_indent = self.get_indent(line)
            if current_indent < indent or stripped.startswith("- "):
                break
            if ":" not in stripped:
                raise ValueError(f"Unsupported YAML mapping line: {line}")
            key, rest = stripped.split(":", 1)
            key = key.strip()
            rest = rest.strip()
            self.index += 1

            if rest in {">", ">-"}:
                value = self.parse_folded_block(indent)
            elif rest == "":
                value = self.parse_block(indent + 2)
            else:
                value = parse_scalar(rest)
            result[key] = value
        return result

    def parse_sequence(self, indent: int) -> list:
        result: list = []
        while self.index < len(self.lines):
            line = self.lines[self.index]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                self.index += 1
                continue
            current_indent = self.get_indent(line)
            if current_indent < indent or not stripped.startswith("- "):
                break
            item_content = stripped[2:]
            self.index += 1

            if item_content == "":
                value = self.parse_block(indent + 2)
            elif ":" in item_content and not item_content.strip().startswith(('"', "'")):
                key_fragment = item_content.split(":", 1)[0]
                if " " not in key_fragment.strip():
                    value = self.parse_nested_item(indent, item_content)
                else:
                    value = parse_scalar(item_content)
            else:
                value = parse_scalar(item_content)
            result.append(value)
        return result

    def parse_nested_item(self, indent: int, first_line: str) -> Any:
        item_lines: List[str] = [" " * (self.base_indent + indent + 2) + first_line]
        while self.index < len(self.lines):
            next_line = self.lines[self.index]
            stripped = next_line.strip()
            if not stripped:
                item_lines.append(next_line)
                self.index += 1
                continue
            next_indent = self.get_indent(next_line)
            if next_indent <= indent:
                break
            item_lines.append(next_line)
            self.index += 1
        sub_parser = SimpleYAMLParser(item_lines, base_indent=self.base_indent + indent + 2)
        return sub_parser.parse_block(0)

    def parse_folded_block(self, indent: int) -> str:
        lines: List[str] = []
        while self.index < len(self.lines):
            line = self.lines[self.index]
            stripped = line.strip("\n")
            if not stripped:
                lines.append("")
                self.index += 1
                continue
            if self.get_indent(line) < indent + 2:
                break
            trimmed = line[self.base_indent + indent + 2 :]
            lines.append(trimmed.rstrip())
            self.index += 1
        paragraphs: List[str] = []
        current: List[str] = []
        for segment in lines:
            if segment.strip() == "":
                if current:
                    paragraphs.append(" ".join(part.strip() for part in current).strip())
                    current = []
            else:
                current.append(segment)
        if current:
            paragraphs.append(" ".join(part.strip() for part in current).strip())
        return "\n\n".join(paragraphs)

    def get_indent(self, line: str) -> int:
        return max(0, self.absolute_indent(line) - self.base_indent)

    @staticmethod
    def absolute_indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))


def parse_scalar(text: str) -> Any:
    text = text.strip()
    if not text:
        return ""
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('\\"', '"')
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    if text.isdigit():
        return int(text)
    try:
        return float(text)
    except ValueError:
        return text


def safe_load(text: str) -> Any:
    if yaml is not None:
        return yaml.safe_load(text)  # type: ignore[no-any-return]
    parser = SimpleYAMLParser.from_text(text)
    return parser.parse()


def safe_load_path(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return safe_load(handle.read())
