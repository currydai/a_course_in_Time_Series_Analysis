from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
OUTPUT = ROOT / "main.tex"

CHAPTER_ORDER = [
    "ch01_introduction",
    "ch02_trends_in_a_time_series",
    "ch03_stationary_time_series",
    "ch04_linear_time_series",
    "ch05_a_review_of_some_results_from_multivariate_a",
    "ch06_the_autocovariance_and_partial_covariance_of",
    "ch07_prediction",
    "ch08_estimation_of_the_mean_and_covariance",
    "ch09_parameter_estimation",
    "ch10_spectral_representations",
    "ch11_spectral_analysis",
    "ch12_multivariate_time_series",
    "ch13_nonlinear_time_series_models",
    "ch14_consistency_and_asymptotic_normality_of_esti",
    "ch15_residual_bootstrap_for_estimation_in_autoreg",
    "appA_background",
    "appB_mixingales_and_physical_dependence",
]


def chapter_tex_file(chapter_dir: Path) -> Path:
    tex_files = sorted(
        path
        for path in chapter_dir.glob("*.tex")
        if not path.name.startswith("main") and not path.name.startswith("_")
    )
    if len(tex_files) != 1:
        raise RuntimeError(f"Expected one TeX file in {chapter_dir}, found {len(tex_files)}")
    return tex_files[0]


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"\\title\{(?P<title>.*?)\}\s*\\author", text, re.S)
    if not match:
        return fallback.replace("_", " ")
    title = re.sub(r"\s+", " ", match.group("title")).strip()
    if r"\quad" in title:
        title = title.split(r"\quad", 1)[1].strip()
    return title


def extract_body(text: str) -> str:
    begin = text.index(r"\begin{document}") + len(r"\begin{document}")
    end = text.rindex(r"\end{document}")
    body = text[begin:end].strip()
    body = re.sub(r"^\\maketitle\s*", "", body)
    return body.strip()


def rel_tex_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build() -> str:
    figures = []
    chapter_parts = []
    appendix_started = False

    for chapter_name in CHAPTER_ORDER:
        chapter_dir = CHAPTERS / chapter_name
        tex_path = chapter_tex_file(chapter_dir)
        text = tex_path.read_text(encoding="utf-8")
        title = extract_title(text, chapter_name)
        body = extract_body(text)

        figures_dir = chapter_dir / "figures"
        if figures_dir.exists():
            figures.append(f"{{{rel_tex_path(figures_dir)}/}}")

        if chapter_name.startswith("app") and not appendix_started:
            chapter_parts.append(r"\appendix")
            appendix_started = True

        source_comment = f"% Source: {rel_tex_path(tex_path)}"
        chapter_parts.append(f"{source_comment}\n\\chapter{{{title}}}\n{body}\n")

    graphicspath = "".join(figures)
    chapters = "\n\\clearpage\n".join(chapter_parts)

    return rf"""\documentclass[11pt,a4paper,openany]{{ctexbook}}

\usepackage[margin=2.6cm]{{geometry}}
\usepackage{{amsmath,amssymb,amsthm}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{listings}}
\usepackage{{caption}}

\graphicspath{{{graphicspath}}}
\hypersetup{{colorlinks=true, linkcolor=blue!50!black, urlcolor=blue!60!black}}
\lstset{{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  columns=fullflexible,
  backgroundcolor=\color{{gray!7}}
}}

\newtheorem{{definition}}{{定义}}[section]
\newtheorem{{theorem}}{{定理}}[section]
\newtheorem{{lemma}}{{引理}}[section]
\newtheorem{{proposition}}{{命题}}[section]
\newtheorem{{example}}{{例}}[section]

\title{{A Course in Time Series Analysis\\中文讲义与 Python 实践}}
\author{{基于原书内容整理的中文主导教学讲义}}
\date{{\today}}

\begin{{document}}
\maketitle
\frontmatter
\tableofcontents
\mainmatter

{chapters}

\end{{document}}
"""


def main() -> None:
    OUTPUT.write_text(build(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
