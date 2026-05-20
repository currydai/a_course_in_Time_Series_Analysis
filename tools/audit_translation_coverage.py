"""Audit whether translated chapter notes are pedagogically close to sources.

This script does not try to prove sentence-level equivalence. It scores whether
the Chinese LaTeX notes are close enough for teaching: standard chapter
structure is present, source-like section coverage is reasonable, key
definition/theorem/example/exercise markers are covered, and the body is not
just a tiny outline.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
REPORT = ROOT / "translation_pedagogical_audit.md"


SOURCE_RE = re.compile(r"source_.*\.txt$")
COMMAND_RE = re.compile(r"\\[a-zA-Z*]+(?:\[[^\]]*\])?(?:\{[^{}]*\})?")
ENV_RE = re.compile(r"\\(?:begin|end)\{[^{}]+\}")
PAGE_RE = re.compile(r"--- physical page \d+ ---")


@dataclass
class AuditRow:
    chapter_dir: Path
    source_file: Path
    tex_file: Path
    source_chars: int
    tex_chars: int
    char_ratio: float
    source_sections: int
    tex_sections: int
    source_key_items: int
    tex_key_items: int
    structure_score: float
    section_score: float
    key_score: float
    density_score: float
    pdf_score: float
    total_score: float
    status: str


def visible_source_text(text: str) -> str:
    text = PAGE_RE.sub(" ", text)
    text = re.sub(r"\(cid:\d+\)", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def visible_tex_text(text: str) -> str:
    body = text
    if "\\begin{document}" in body:
        body = body.split("\\begin{document}", 1)[1]
    if "\\end{document}" in body:
        body = body.split("\\end{document}", 1)[0]
    body = ENV_RE.sub(" ", body)
    body = COMMAND_RE.sub(" ", body)
    body = re.sub(r"[%].*", " ", body)
    body = re.sub(r"\s+", " ", body)
    return body.strip()


def source_section_count(text: str) -> int:
    # Require a heading-like word after the section number; this avoids counting
    # graph tick labels such as "0.0 0.2 0.4".
    return len(re.findall(r"(?m)^(?:\d+\.\d+(?:\.\d+)?|A\.\d+|B\.\d+)\s+[A-Za-z]", text))


def tex_section_count(text: str) -> int:
    return len(re.findall(r"\\(?:section|subsection)\*?\{", text))


def source_key_item_count(text: str) -> int:
    return len(re.findall(r"(?m)^(?:Definition|Theorem|Lemma|Proposition|Example|Exercise)\b", text))


def tex_key_item_count(text: str) -> int:
    markers = [
        r"\\begin\{definition\}",
        r"\\begin\{theorem\}",
        r"\\begin\{lemma\}",
        r"\\begin\{proposition\}",
        r"\\begin\{example\}",
        r"\\section\{练习提要\}",
        r"Exercise\s+\d",
        r"原文\s+(?:Definition|Theorem|Lemma|Proposition|Example|Exercise)",
    ]
    return sum(len(re.findall(p, text)) for p in markers)


def has_standard_structure(text: str) -> int:
    required = [
        r"\section*{本章学习目标}",
        r"\section{Python 工程实践}",
        r"\section{练习提要}",
        r"\section*{本章小结}",
    ]
    return sum(1 for marker in required if marker in text)


def find_tex_file(chapter_dir: Path) -> Path:
    tex_files = sorted(chapter_dir.glob("*.tex"))
    if len(tex_files) != 1:
        raise ValueError(f"Expected one tex file in {chapter_dir}, found {len(tex_files)}")
    return tex_files[0]


def audit_chapter(source_file: Path) -> AuditRow:
    chapter_dir = source_file.parent
    tex_file = find_tex_file(chapter_dir)
    source_raw = source_file.read_text(encoding="utf-8")
    tex_raw = tex_file.read_text(encoding="utf-8")
    source_visible = visible_source_text(source_raw)
    tex_visible = visible_tex_text(tex_raw)

    source_chars = len(source_visible)
    tex_chars = len(tex_visible)
    ratio = tex_chars / source_chars if source_chars else 0.0
    source_sections = source_section_count(source_raw)
    tex_sections = tex_section_count(tex_raw)
    source_key_items = source_key_item_count(source_raw)
    tex_key_items = tex_key_item_count(tex_raw)
    pdf_file = tex_file.with_suffix(".pdf")

    structure_score = 20.0 * has_standard_structure(tex_raw) / 4.0
    section_score = 25.0 if source_sections == 0 else 25.0 * min(tex_sections / source_sections, 1.0)
    key_score = 25.0 if source_key_items == 0 else 25.0 * min(tex_key_items / source_key_items, 1.0)
    # Teaching notes can be shorter than the source, but below roughly one third
    # of the extracted source they are usually too skeletal.
    density_score = 20.0 * min(ratio / 0.35, 1.0)
    pdf_score = 10.0 if pdf_file.exists() else 0.0
    total_score = structure_score + section_score + key_score + density_score + pdf_score

    if total_score >= 75.0:
        status = "PASS"
    elif total_score >= 60.0:
        status = "REVIEW: 教学覆盖基本接近，但建议继续补强"
    else:
        status = "FAIL: 教学覆盖不足，需要补充"

    return AuditRow(
        chapter_dir=chapter_dir,
        source_file=source_file,
        tex_file=tex_file,
        source_chars=source_chars,
        tex_chars=tex_chars,
        char_ratio=ratio,
        source_sections=source_sections,
        tex_sections=tex_sections,
        source_key_items=source_key_items,
        tex_key_items=tex_key_items,
        structure_score=structure_score,
        section_score=section_score,
        key_score=key_score,
        density_score=density_score,
        pdf_score=pdf_score,
        total_score=total_score,
        status=status,
    )


def write_report(rows: list[AuditRow]) -> None:
    lines = [
        "# Translation Pedagogical Coverage Audit",
        "",
        "Criterion: translated Chinese notes should be pedagogically close to the extracted English source. This is not a sentence-length audit. It scores chapter structure, source-like sections, key theorem/example/exercise markers, body density, and successful PDF generation.",
        "",
        "Score weights: standard structure 20, section coverage 25, key item coverage 25, body density up to one third of source 20, PDF presence 10. PASS >= 75, REVIEW >= 60.",
        "",
        "| Chapter | Ratio | Sections | Key items | Structure | Density | Total | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        chapter = row.chapter_dir.name
        lines.append(
            f"| `{chapter}` | {row.char_ratio:.2f} | {row.tex_sections}/{row.source_sections} | "
            f"{row.tex_key_items}/{row.source_key_items} | {row.structure_score:.0f}/20 | "
            f"{row.density_score:.0f}/20 | {row.total_score:.1f} | {row.status} |"
        )
    failed = [row for row in rows if row.status.startswith("FAIL")]
    review = [row for row in rows if row.status.startswith("REVIEW")]
    if failed:
        next_action = "Next required action: prioritize FAIL chapters with low density and weak section/key-item coverage."
    elif review:
        next_action = "Next suggested action: enrich REVIEW chapters, especially where density or section coverage is weakest."
    else:
        next_action = "Next suggested action: all chapters pass the pedagogical coverage audit; future work can focus on style unification and optional example expansion."
    lines.extend(
        [
            "",
            f"Result: {len(rows) - len(failed) - len(review)} PASS, {len(review)} REVIEW, {len(failed)} FAIL.",
            "",
            "Interpretation: a FAIL means the current LaTeX note is still too skeletal for teaching-effect equivalence. REVIEW means usable but worth enriching.",
            next_action,
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    sources = sorted(path for path in CHAPTERS.rglob("source_*.txt") if SOURCE_RE.match(path.name))
    rows = [audit_chapter(path) for path in sources]
    write_report(rows)
    for row in rows:
        print(
            f"{row.chapter_dir.name}: ratio={row.char_ratio:.2f}, "
            f"sections {row.tex_sections}/{row.source_sections}, "
            f"key {row.tex_key_items}/{row.source_key_items}, "
            f"score={row.total_score:.1f}, {row.status}"
        )
    return 1 if any(row.status.startswith("FAIL") for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
