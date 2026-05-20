"""Generate figures for ch03."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.chapter_practice_figures import generate_chapter_figures


if __name__ == "__main__":
    generate_chapter_figures("ch03", Path(__file__).resolve())
