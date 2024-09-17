"""
Utilities for working with packages in the CLI.
"""

import re


def load_package(file):
    loader = load_source
    if file.suffix == ".md":
        loader = load_from_markdown

    with open(file, "r", encoding="utf-8") as fd:
        source = loader(fd)
        info = {"name": None, "file": file, "kind": "package"}
        for line in source:
            match = re.fullmatch(r"\s*package\s+(\S+)\s*([;#].*)?", line)
            if match:
                if info["name"] is not None:
                    raise ValueError(f"Multiple packages found in {file}")
                info["name"] = match.group(1)

        info["content"] = "".join(source)

    return info


def load_source(fd):
    return list(fd)


def load_from_markdown(fd):
    source = list(fd)
    if re.match(r"^---\s*\n", source[0]):
        split_at = len(source)
        for i in range(1, len(source) - 1):
            if re.match(r"^---\s*\n", source[i]):
                split_at = i
                break
        source = source[split_at + 1 :]

    buffer = []
    in_fenced_area = False
    for line in source:
        if not in_fenced_area and re.match(r"^```(htn)?\n$", line):
            in_fenced_area = True
        elif in_fenced_area and re.match(r"^```\n$", line):
            in_fenced_area = False
        elif in_fenced_area:
            buffer.append(line)
    return buffer
