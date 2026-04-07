#!/usr/bin/env python3
"""Extract origin URL and a short README summary from local git repos."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


README_CANDIDATES = [
    "README.md",
    "README.MD",
    "readme.md",
    "README",
    "README.rst",
    "README.zh-CN.md",
    "README_ZH.md",
]


def git_origin(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "remote", "get-url", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def find_readme(path: Path) -> Path | None:
    for candidate in README_CANDIDATES:
        file_path = path / candidate
        if file_path.is_file():
            return file_path
    for file_path in sorted(path.iterdir()):
        if file_path.is_file() and file_path.name.lower().startswith("readme"):
            return file_path
    return None


def clean_line(line: str) -> str:
    text = line.strip()
    if not text:
        return ""
    if text.startswith("#") or text.startswith("```") or text.startswith("---"):
        return ""
    if text.startswith("![" ) or text.startswith("[!["):
        return ""
    if text.startswith("<img") or text.startswith("<div") or text.startswith("</div"):
        return ""
    if text.startswith("<p") or text.startswith("</p"):
        return ""

    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip(" -|")
    return text if len(text) >= 8 else ""


def readme_summary(path: Path) -> str:
    readme = find_readme(path)
    if readme is None:
        return ""
    try:
        lines = readme.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return ""
    for line in lines[:80]:
        cleaned = clean_line(line)
        if cleaned:
            return cleaned
    return ""


def extract(path_text: str) -> dict[str, str]:
    path = Path(path_text).resolve()
    return {
        "name": path.name,
        "path": str(path),
        "url": git_origin(path),
        "summary": readme_summary(path),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: extract_repo_meta.py <repo-path> [<repo-path> ...]", file=sys.stderr)
        return 1
    for arg in sys.argv[1:]:
        print(json.dumps(extract(arg), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
