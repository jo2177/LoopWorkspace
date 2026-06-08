#!/usr/bin/env python3

"""Remove <file> sections from XLIFF files by their 'original' attribute.

Usage:
    remove_xliff_sections.py <xliff_dir> <original_path> [<original_path> ...]

For each .xliff file in <xliff_dir>, removes any <file original="..."> section
whose 'original' attribute matches one of the given paths.
"""

import sys
import os
import xml.etree.ElementTree as ET


XLIFF_NS = "urn:oasis:names:tc:xliff:document:1.2"
NS = {"xliff": XLIFF_NS}


def remove_sections(xliff_path, paths_to_remove):
    tree = ET.parse(xliff_path)
    root = tree.getroot()

    removed = []
    for path in paths_to_remove:
        for file_elem in root.findall(f'xliff:file[@original="{path}"]', NS):
            root.remove(file_elem)
            removed.append(path)

    if removed:
        ET.register_namespace("", XLIFF_NS)
        tree.write(xliff_path, xml_declaration=True, encoding="UTF-8")
        for path in removed:
            print(f"  Removed: {path}")

    return len(removed)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <xliff_dir> <original_path> [<original_path> ...]",
              file=sys.stderr)
        sys.exit(1)

    xliff_dir = sys.argv[1]
    paths_to_remove = sys.argv[2:]

    for filename in sorted(os.listdir(xliff_dir)):
        if not filename.endswith(".xliff"):
            continue
        xliff_path = os.path.join(xliff_dir, filename)
        print(f"Processing {filename}:")
        count = remove_sections(xliff_path, paths_to_remove)
        if count == 0:
            print("  No matching sections found")


if __name__ == "__main__":
    main()
