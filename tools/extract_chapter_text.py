"""Extract text from a page range of the source PDF.

Usage:
    python tools/extract_chapter_text.py --start 13 --end 18 --output tmp_ch01.txt

Page numbers are physical PDF pages, starting from 1.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pdfplumber


def extract(pdf_path: Path, start: int, end: int) -> str:
    chunks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        if start < 1 or end > total or start > end:
            raise ValueError(f"Invalid page range {start}-{end}; PDF has {total} pages.")
        for physical_page in range(start, end + 1):
            page = pdf.pages[physical_page - 1]
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            chunks.append(f"\n\n--- physical page {physical_page} ---\n{text}")
    return "".join(chunks).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default="A course in Time Series Analysis.pdf")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    text = extract(Path(args.pdf), args.start, args.end)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

