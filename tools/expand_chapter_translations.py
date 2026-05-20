"""Expand first-pass chapter notes into structured Chinese LaTeX notes.

The generated files follow the chapter-2 refinement standard:
learning objectives, source-like section structure, main formulas,
definitions/theorems/examples, Python practice, exercise guide, and summary.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PREAMBLE = r"""\documentclass[11pt,a4paper]{ctexart}

\usepackage[margin=2.6cm]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{caption}

\graphicspath{{figures/}}
\hypersetup{colorlinks=true, linkcolor=blue!50!black, urlcolor=blue!60!black}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  columns=fullflexible,
  backgroundcolor=\color{gray!7}
}

\newtheorem{definition}{定义}[section]
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}{引理}[section]
\newtheorem{proposition}{命题}[section]
\newtheorem{example}{例}[section]

"""


def fig_blocks(zh: str, figs: list[str], captions: list[str]) -> str:
    blocks: list[str] = []
    for fig, caption in zip(figs, captions):
        blocks.append(
            rf"""\begin{{figure}}[htbp]
  \centering
  \includegraphics[width=0.86\textwidth]{{{fig}}}
  \caption{{{caption}}}
\end{{figure}}"""
        )
    return "\n\n".join(blocks)


def tex_document(spec: dict[str, object]) -> str:
    objectives = "\n".join(f"  \\item {item}" for item in spec["objectives"])  # type: ignore[index]
    sections = "\n\n".join(spec["sections"])  # type: ignore[index]
    figures = fig_blocks(spec["zh"], spec["figs"], spec["captions"])  # type: ignore[index]
    exercises = "\n".join(f"  \\item {item}" for item in spec["exercises"])  # type: ignore[index]
    return rf"""{PREAMBLE}\title{{{spec["title"]}}}
\author{{基于 \textit{{A Course in Time Series Analysis}} 的中文讲义与 Python 实践}}
\date{{}}

\begin{{document}}
\maketitle

\section*{{本章学习目标}}

本章按照原文 \textit{{{spec["en"]}}} 的小节顺序整理，保留主要定义、定理、模型公式和练习方向，并将原文中的 R 实践思路改写为 Python 工程实践。

完成本章后，应能够：
\begin{{itemize}}
{objectives}
\end{{itemize}}

{sections}

\section{{Python 工程实践}}

在本章目录下运行：
\begin{{lstlisting}}[language=bash]
python scripts/{spec["code"]}_generate_figures.py
\end{{lstlisting}}

脚本会把图像写入本章 \texttt{{figures/}} 目录。当前图像用于配合本章核心概念的仿真说明；若后续补齐原始数据文件，可把模拟数据替换为原文真实数据案例。

{figures}

\section{{练习提要}}

原文练习主要围绕下列方向展开：
\begin{{itemize}}
{exercises}
\end{{itemize}}

\section*{{本章小结}}

{spec["summary"]}

\end{{document}}
"""


SPECS: list[dict[str, object]] = [
    {
        "code": "ch03",
        "dir": "chapters/ch03_stationary_time_series",
        "file": "第03章_Stationary_Time_Series_平稳时间序列.tex",
        "en": "Stationary Time Series",
        "zh": "平稳时间序列",
        "title": r"第 3 章 \quad Stationary Time Series / 平稳时间序列",
        "objectives": [
            r"复习期望、协方差、渐近阶 \(O(\cdot)\) 与 \(o(\cdot)\) 等预备知识；",
            r"形式化定义时间序列并理解有限维分布；",
            r"推导相关序列下样本均值的方差和标准误；",
            r"区分严格平稳、二阶平稳和遍历性；",
            r"判断一个序列或函数能否作为合法协方差。"
        ],
        "sections": [
r"""\section{预备知识}

原文先复习本课程反复使用的概率记号。若 \(X\) 是随机变量，期望写作 \(E(X)\)；若 \(X,Y\) 二阶矩存在，协方差为
\[
  \mathrm{cov}(X,Y)=E\{(X-E X)(Y-E Y)\}.
\]
若 \(a_n/b_n\) 有界，则 \(a_n=O(b_n)\)；若 \(a_n/b_n\to0\)，则 \(a_n=o(b_n)\)。这些记号用于描述估计误差、协方差衰减和渐近方差的阶。

\subsection{时间序列的形式化定义}

时间序列是定义在同一概率空间上的一族随机变量
\[
  \{X_t:t\in\mathbb Z\}.
\]
实际观测通常只是有限片段 \(X_1,\ldots,X_n\)，但理论上把过程延拓到整数时间轴可使平移、滞后和协方差函数的定义更自然。""",
r"""\section{样本均值及其标准误}

样本均值为
\[
  \bar X_n=\frac1n\sum_{t=1}^n X_t.
\]
在独立同分布情形，
\[
  \mathrm{var}(\bar X_n)=\frac{\sigma^2}{n}.
\]
但若序列相关，方差变为
\[
  \mathrm{var}(\bar X_n)
  =\frac1{n^2}\sum_{s=1}^n\sum_{t=1}^n\mathrm{cov}(X_s,X_t).
\]
若过程二阶平稳，记 \(c(r)=\mathrm{cov}(X_t,X_{t+r})\)，则
\[
  \mathrm{var}(\bar X_n)
  =\frac1n c(0)+\frac2{n^2}\sum_{r=1}^{n-1}(n-r)c(r).
\]
这正是时间序列推断区别于 iid 推断的第一条主线：相关性改变标准误。

\subsection{线性回归估计量的方差}

在回归模型中，若误差相关，普通最小二乘估计量的方差不再只是 \(\sigma^2(X'X)^{-1}\)。原文用该例说明：在时间序列回归中，即使估计量形式仍是最小二乘，标准误也必须反映误差的协方差矩阵。""",
r"""\section{平稳过程}

\subsection{平稳性的类型}

\begin{definition}[严格平稳，原文 Definition 3.3.1]
若对任意 \(k\)、任意时间点 \(t_1,\ldots,t_k\) 和任意整数平移 \(h\)，随机向量
\[
  (X_{t_1},\ldots,X_{t_k})
\]
与
\[
  (X_{t_1+h},\ldots,X_{t_k+h})
\]
具有相同联合分布，则称 \(\{X_t\}\) 严格平稳。
\end{definition}

\begin{definition}[二阶平稳或弱平稳，原文 Definition 3.3.2]
若 \(E(X_t)=\mu\) 不随 \(t\) 变化，且
\[
  \mathrm{cov}(X_t,X_s)=c(t-s)
\]
只依赖滞后 \(t-s\)，则称 \(\{X_t\}\) 二阶平稳。
\end{definition}

严格平稳关注所有有限维分布；二阶平稳只关注一阶矩和二阶矩。若严格平稳且二阶矩有限，则自动二阶平稳。

\begin{example}[二阶平稳下样本均值方差]
若 \(\sum_{r=-\infty}^{\infty}|c(r)|<\infty\)，则
\[
  n\,\mathrm{var}(\bar X_n)
  \to \sum_{r=-\infty}^{\infty}c(r).
\]
右端称为长期方差，是后续 HAC/Newey-West 标准误的理论来源。
\end{example}

\begin{definition}[遍历性，原文 Definition 3.3.3]
粗略地说，遍历性保证时间平均可代表总体平均。若
\[
  \frac1n\sum_{t=1}^n X_t \xrightarrow{a.s.} E(X_0),
\]
则样本路径上的长期平均具有统计意义。
\end{definition}""",
r"""\section{什么样的函数可以作为协方差}

\begin{definition}[非负定序列，原文 Definition 3.4.1]
序列 \(\{c(k):k\in\mathbb Z\}\) 非负定，是指对任意 \(n\) 和任意实数 \(a_1,\ldots,a_n\)，
\[
  \sum_{i=1}^n\sum_{j=1}^n a_i a_j c(i-j)\ge0.
\]
\end{definition}

\begin{theorem}[协方差的必要性质，原文 Theorem 3.4.1]
若 \(\{X_t\}\) 是离散时间二阶平稳过程，则其协方差函数 \(c(k)\) 必为非负定序列；连续时间情形中，协方差函数也必须满足对应的非负定条件。
\end{theorem}

\begin{theorem}[Fourier 判别，原文 Theorem 3.4.2]
若 \(\sum_k |c(k)|<\infty\)，则 \(c(k)\) 是合法协方差序列的一个充分条件是其 Fourier 变换
\[
  f(\omega)=\frac1{2\pi}\sum_{k=-\infty}^{\infty}c(k)e^{-ik\omega}
\]
非负。该函数就是谱密度。
\end{theorem}

\section{空间协方差}

原文最后把一维时间协方差推广到空间协方差 \(c:\mathbb R^d\to\mathbb R\)。若协方差只依赖距离 \(\|u\|\)，称为各向同性协方差。空间部分为后续理解非时间索引随机场提供背景。""",
        ],
        "figs": ["ch03_fig01_stationary_vs_random_walk.png", "ch03_fig02_rolling_mean.png"],
        "captions": [
            "平稳 AR(1) 与随机游走对比：平稳序列围绕固定均值波动，随机游走的水平随时间漂移。",
            "滚动均值稳定性：平稳序列的滚动均值较稳定，随机游走的滚动均值呈持续漂移。"
        ],
        "exercises": [
            r"计算由白噪声构造的线性组合的协方差，练习协方差展开；",
            r"判断给定过程是否二阶平稳，并解释均值和协方差是否随时间改变；",
            r"为 SOI、太阳黑子和温度数据绘制 ACF，理解样本自相关的含义；",
            r"判断给定序列或函数是否可作为协方差。"
        ],
        "summary": r"第 3 章建立了全书的概率基础：时间序列推断依赖平稳性、遍历性和协方差结构。样本均值的标准误不再只由 \(c(0)\) 决定，而由所有滞后协方差共同决定；合法协方差必须满足非负定性，并可通过谱密度刻画。"
    },
    {
        "code": "ch04",
        "dir": "chapters/ch04_linear_time_series",
        "file": "第04章_Linear_time_series_线性时间序列.tex",
        "en": "Linear time series",
        "zh": "线性时间序列",
        "title": r"第 4 章 \quad Linear time series / 线性时间序列",
        "objectives": [
            r"理解线性过程和 \(MA(\infty)\) 表示；",
            r"掌握后移算子、AR(p) 差分方程和因果解；",
            r"说明 AR(2) 的伪周期现象和季节 AR 模型；",
            r"区分 AR、MA、ARMA 的因果性与可逆性；",
            r"理解单位根、非可逆过程以及 ACF/PACF 诊断。"
        ],
        "sections": [
r"""\section{动机}

线性时间序列把当前观测表示为过去冲击的线性组合。它是全书的工作马模型：既能产生丰富的相关结构，又有清晰的协方差、预测和频域公式。

\section{线性过程与移动平均模型}

\begin{definition}[线性过程与 \(MA(\infty)\)，原文 Definition 4.2.1]
若 \(\{\varepsilon_t\}\) 是均值为 0、方差为 \(\sigma^2\) 的不相关创新，且
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j},
  \qquad \sum_{j=0}^{\infty}|\psi_j|<\infty,
\]
则称 \(\{X_t\}\) 是线性过程，也称具有 \(MA(\infty)\) 表示。
\end{definition}

\begin{lemma}[无限和的存在性，原文 Lemma 4.2.1]
若系数满足适当可和条件且创新二阶矩有限，则上述无限和在均方意义下存在，并定义一个二阶平稳过程。
\end{lemma}

其均值为 0，自协方差为
\[
  c(k)=\sigma^2\sum_{j=0}^{\infty}\psi_j\psi_{j+|k|}.
\]""",
r"""\section{AR(p) 模型}

\subsection{差分方程与后移算子}

后移算子定义为 \(BX_t=X_{t-1}\)。AR(p) 模型写作
\[
  X_t=\phi_1X_{t-1}+\cdots+\phi_pX_{t-p}+\varepsilon_t,
\]
或
\[
  \phi(B)X_t=\varepsilon_t,\qquad
  \phi(z)=1-\phi_1z-\cdots-\phi_pz^p.
\]

\subsection{AR(1) 的两个解}

对
\[
  X_t=\phi X_{t-1}+\varepsilon_t,
\]
若 \(|\phi|<1\)，因果平稳解为
\[
  X_t=\sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j}.
\]
若 \(|\phi|>1\)，也可构造非因果平稳解
\[
  X_t=-\sum_{j=1}^{\infty}\phi^{-j}\varepsilon_{t+j},
\]
但该解依赖未来创新，不适合作为预测模型。

\begin{lemma}[AR(p) 因果解，原文 Lemma 4.3.1]
若 \(\phi(z)\) 的所有根都在单位圆外，则 AR(p) 有唯一因果平稳解，且可写成
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j},
\]
其中 \(\psi(z)=1/\phi(z)\) 在单位圆附近解析。
\end{lemma}""",
r"""\section{AR(2)、伪周期与季节自回归}

AR(2) 的特征根若为复数，会产生阻尼振荡。若根可表示为 \(re^{\pm i\omega}\)，则样本路径和自协方差常表现出近似周期
\[
  P=\frac{2\pi}{\omega}.
\]
这就是原文称为 pseudo periodicity 的现象：模型没有确定性周期项，但相关结构会产生类似周期的波动。

季节自回归模型把滞后设为季节长度，例如月度数据中常见
\[
  X_t=\Phi X_{t-12}+\varepsilon_t.
\]
它用于刻画每年同月之间的相关性。""",
r"""\section{ARMA 模型}

\begin{definition}[AR、ARMA 与 MA，原文 Definition 4.5.1]
ARMA(p,q) 模型定义为
\[
  \phi(B)X_t=\theta(B)\varepsilon_t,
\]
其中
\[
  \phi(z)=1-\phi_1z-\cdots-\phi_pz^p,\qquad
  \theta(z)=1+\theta_1z+\cdots+\theta_qz^q.
\]
当 \(q=0\) 时为 AR(p)，当 \(p=0\) 时为 MA(q)。
\end{definition}

\begin{definition}[因果与可逆，原文 Definition 4.5.2]
若 \(\phi(z)\) 的根都在单位圆外，则模型因果；若 \(\theta(z)\) 的根都在单位圆外，则模型可逆。可逆性保证创新可由当前和过去观测恢复：
\[
  \varepsilon_t=\sum_{j=0}^{\infty}\pi_j X_{t-j}.
\]
\end{definition}

\section{ARFIMA、单位根与诊断}

ARFIMA 模型通过分数差分 \((1-B)^d\) 描述长记忆。单位根模型含有 \(\phi(1)=0\)，最典型例子是随机游走
\[
  X_t=X_{t-1}+\varepsilon_t.
\]
诊断上，MA(q) 的 ACF 通常 q 阶截尾，AR(p) 的 PACF 通常 p 阶截尾；单位根过程的 ACF 衰减很慢，差分后更接近平稳。""",
        ],
        "figs": ["ch04_fig01_arma_series.png", "ch04_fig02_acf_pacf.png"],
        "captions": ["模拟 ARMA(2,1) 序列：线性模型可产生持续相关但均值稳定的波动。", "ACF/PACF 诊断图：用于区分 AR 与 MA 结构并辅助阶数选择。"],
        "exercises": [r"求 AR(1)、AR(2) 的平稳因果解；", r"根据特征根判断 AR(p) 的因果性；", r"构造具有指定伪周期的 AR(2) 模型；", r"模拟 ARMA、单位根和非可逆模型并比较 ACF/PACF。"],
        "summary": "第 4 章给出了线性时间序列的模型语言。后移算子把差分方程写成多项式，根的位置决定因果性、可逆性和单位根；ACF 与 PACF 则把这些理论结构变成可观察诊断。"
    },
    {
        "code": "ch05",
        "dir": "chapters/ch05_a_review_of_some_results_from_multivariate_a",
        "file": "第05章_Multivariate_analysis_review_多元分析结果回顾.tex",
        "en": "A review of some results from multivariate analysis",
        "zh": "多元分析结果回顾",
        "title": r"第 5 章 \quad A review of some results from multivariate analysis / 多元分析结果回顾",
        "objectives": [r"复习内积、范数、正交和投影；", r"把线性预测理解为 Hilbert 空间投影；", r"推导多阶段投影和偏相关；", r"理解精度矩阵中的零元素与条件不相关的关系；", r"为后续 Durbin-Levinson 和部分自相关建立几何语言。"],
        "sections": [
r"""\section{欧氏空间与投影}

\subsection{内积、范数与正交}

在 \(\mathbb R^n\) 中，内积为
\[
  \langle x,y\rangle=\sum_{i=1}^n x_i y_i,
\]
范数为 \(\|x\|=\sqrt{\langle x,x\rangle}\)。若 \(\langle x,y\rangle=0\)，称 \(x\) 与 \(y\) 正交。

\subsection{投影}

把向量 \(Y\) 投影到由 \(X\) 张成的空间，得到
\[
  \hat Y=\alpha X,\qquad
  \alpha=\frac{\langle Y,X\rangle}{\langle X,X\rangle}.
\]
残差 \(Y-\hat Y\) 与 \(X\) 正交。多元情形中，若 \(X\) 为设计矩阵，则
\[
  \hat Y=X(X'X)^{-1}X'Y.
\]
投影矩阵 \(P=X(X'X)^{-1}X'\) 满足 \(P^2=P\) 和 \(P'=P\)。

\subsection{多阶段投影}

若先投影到一个子空间，再对残差投影到另一个正交补空间，可以把复杂预测分解为几个正交部分。这一思想在后续部分自相关和 Durbin-Levinson 递推中反复出现。""",
r"""\section{随机变量空间}

二阶随机变量构成一个带内积的空间：
\[
  \langle X,Y\rangle=E(XY).
\]
若使用中心化随机变量，则内积对应协方差：
\[
  \langle X-E X,Y-EY\rangle=\mathrm{cov}(X,Y).
\]
因此，最佳线性预测就是在随机变量空间中的正交投影。

\section{线性预测}

设要用 \(X_1,\ldots,X_p\) 线性预测 \(Y\)，预测量为
\[
  \hat Y=\sum_{j=1}^p a_jX_j.
\]
最优系数由正交方程给出：
\[
  E\left[(Y-\hat Y)X_k\right]=0,\qquad k=1,\ldots,p.
\]
写成矩阵形式：
\[
  \Gamma a=\gamma,
\]
其中 \(\Gamma_{ij}=E(X_iX_j)\)，\(\gamma_i=E(YX_i)\)。""",
r"""\section{偏相关}

偏相关衡量在控制其他变量后两个变量之间剩余的线性关系。设 \(X\) 与 \(Y\) 都先对 \(Z\) 做线性投影，残差分别为
\[
  X^\perp=X-\mathrm{Proj}(X\mid Z),\qquad
  Y^\perp=Y-\mathrm{Proj}(Y\mid Z).
\]
则偏相关为
\[
  \rho_{XY\cdot Z}
  =\frac{\mathrm{cov}(X^\perp,Y^\perp)}
  {\sqrt{\mathrm{var}(X^\perp)\mathrm{var}(Y^\perp)}}.
\]
在时间序列中，部分自相关就是 \(X_t\) 与 \(X_{t+h}\) 在控制中间 \(X_{t+1},\ldots,X_{t+h-1}\) 后的相关。""",
r"""\section{精度矩阵性质}

协方差矩阵 \(\Sigma\) 的逆矩阵
\[
  \Omega=\Sigma^{-1}
\]
称为精度矩阵。若随机向量为高斯分布，则 \(\Omega_{ij}=0\) 等价于第 \(i\) 与第 \(j\) 个分量在给定其他分量后条件独立。即使非高斯，精度矩阵的零元素也对应线性条件不相关结构。

\section{附录：Hilbert 空间投影}

原文附录把投影定理放在 Hilbert 空间中陈述：若 \(\mathcal M\) 是闭线性子空间，则任意 \(Y\) 可唯一分解为
\[
  Y=\mathrm{Proj}_{\mathcal M}Y+e,
  \qquad e\perp \mathcal M.
\]
该定理是预测理论的几何基础。""",
        ],
        "figs": ["ch05_fig01_projection_prediction.png", "ch05_fig02_correlation_matrix.png"],
        "captions": ["线性预测的投影视角：预测值是观测向解释变量空间的正交投影。", "相关矩阵示例：多元关系可由协方差矩阵和精度矩阵进一步分析。"],
        "exercises": [r"计算向量投影和投影残差，验证正交性；", r"推导最优线性预测的正规方程；", r"用残差相关解释偏相关；", r"从协方差矩阵求精度矩阵并解释零元素。"],
        "summary": "第 5 章把多元线性代数翻译成时间序列预测语言。投影给出最小均方误差预测，偏相关解释 PACF，精度矩阵则连接到条件依赖结构。"
    },
    {
        "code": "ch06",
        "dir": "chapters/ch06_the_autocovariance_and_partial_covariance_of",
        "file": "第06章_Autocovariance_partial_covariance_自协方差与偏协方差.tex",
        "en": "The autocovariance and partial covariance of a stationary time series",
        "zh": "平稳时间序列的自协方差与偏协方差",
        "title": r"第 6 章 \quad Autocovariance and partial covariance / 自协方差与偏协方差",
        "objectives": [r"推导线性过程、AR、MA、ARMA 的自协方差；", r"理解 ARMA 自协方差衰减速度；", r"估计样本 ACF 并识别模型；", r"定义时间序列偏协方差与 PACF；", r"理解方差矩阵、精度矩阵和非因果模型的 ACF。"],
        "sections": [
r"""\section{自协方差函数}

平稳过程的自协方差定义为
\[
  c(k)=\mathrm{cov}(X_t,X_{t+k}).
\]
对线性过程
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j},
\]
若 \(\mathrm{var}(\varepsilon_t)=\sigma^2\)，则
\[
  c(k)=\sigma^2\sum_{j=0}^{\infty}\psi_j\psi_{j+|k|}.
\]

\begin{lemma}[线性表示的协方差，原文 Lemma 6.1.1]
若平稳序列具有绝对可和的线性表示，则其自协方差由系数卷积给出，并且 \(\sum_k|c(k)|<\infty\) 在相应条件下成立。
\end{lemma}

\subsection{ARMA 协方差的衰减}

因果可逆 ARMA 的系数通常几何衰减，因此自协方差也几何衰减。AR 根越接近单位圆，ACF 衰减越慢。""",
r"""\section{AR、MA 和 ARMA 的自协方差}

AR(p) 模型
\[
  X_t=\phi_1X_{t-1}+\cdots+\phi_pX_{t-p}+\varepsilon_t
\]
两边同乘 \(X_{t-k}\) 并取期望，可得 Yule-Walker 方程：
\[
  c(k)=\phi_1c(k-1)+\cdots+\phi_pc(k-p),\qquad k\ge1.
\]
对 AR(1)，
\[
  c(k)=\frac{\sigma^2}{1-\phi^2}\phi^{|k|}.
\]

MA(q) 模型
\[
  X_t=\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q}
\]
的自协方差在 \(q\) 阶后截尾：
\[
  c(k)=0,\qquad |k|>q.
\]
ARMA 模型的 ACF 通常在前若干阶受 MA 部分影响，随后按 AR 部分的差分方程递推衰减。""",
r"""\section{从数据估计 ACF}

若均值未知，样本自协方差通常写为
\[
  \hat c(k)=\frac1n\sum_{t=1}^{n-k}(X_t-\bar X)(X_{t+k}-\bar X),
\]
样本自相关为
\[
  \hat\rho(k)=\frac{\hat c(k)}{\hat c(0)}.
\]
ACF 图是识别线性模型的基础：MA(q) 的 ACF 倾向截尾，AR(p) 的 ACF 倾向拖尾。

\section{偏相关}

\begin{definition}[偏协方差/偏相关，原文 Definition 6.2.1]
\(X_t\) 与 \(X_{t+h}\) 在控制中间变量 \(X_{t+1},\ldots,X_{t+h-1}\) 后的残差协方差称为偏协方差；标准化后称为偏相关。
\end{definition}

对平稳序列，h 阶偏自相关可记为 \(\phi_{h,h}\)。它等于用 \(X_{t-1},\ldots,X_{t-h}\) 预测 \(X_t\) 的最佳 AR(h) 模型中第 h 个系数。AR(p) 的 PACF 在 p 阶后截尾。""",
r"""\section{方差矩阵、精度矩阵与非因果模型}

对向量 \(X_1,\ldots,X_n\)，协方差矩阵为 Toeplitz 形式：
\[
  \Gamma_n=(c(i-j))_{i,j=1}^n.
\]
其逆矩阵反映条件线性依赖结构。AR(p) 过程的精度矩阵具有带状结构，这对应“给定最近 p 个邻居后更远变量无直接线性影响”。

原文最后讨论非因果时间序列和 minimum phase。谱密度定义为
\[
  f(\omega)=\frac1{2\pi}\sum_{k=-\infty}^{\infty}c(k)e^{-ik\omega},
\]
不同因果/非因果表示可能具有相同的二阶结构，因此仅凭 ACF 不能总是区分时间方向。""",
        ],
        "figs": ["ch06_fig01_acf_shapes.png", "ch06_fig02_pacf_shapes.png"],
        "captions": ["AR 与 MA 的 ACF 形态：AR 通常拖尾，MA 通常截尾。", "AR 与 MA 的 PACF 形态：AR 通常截尾，MA 通常拖尾。"],
        "exercises": [r"推导 AR(2) 的自协方差和伪周期 ACF；", r"比较 AR、MA、ARMA 的 ACF/PACF 图；", r"计算 MA(1) 的偏相关；", r"证明 AR(p) 方差矩阵逆的带状结构。"],
        "summary": "第 6 章把线性模型与可观察的相关图联系起来。Yule-Walker 方程给出 AR 的协方差递推，MA 的协方差截尾，PACF 则将投影几何转化为模型识别工具。"
    },
    {
        "code": "ch07",
        "dir": "chapters/ch07_prediction",
        "file": "第07章_Prediction_预测.tex",
        "en": "Prediction",
        "zh": "预测",
        "title": r"第 7 章 \quad Prediction / 预测",
        "objectives": [r"理解预测在估计和模型诊断中的作用；", r"推导 AR 与 ARMA 的一步和多步预测；", r"掌握有限过去预测与 Durbin-Levinson 递推；", r"理解 Kalman 滤波的状态空间预测形式；", r"了解非线性模型、Wold 分解和 Kolmogorov 公式。"],
        "sections": [
r"""\section{预测在估计中的作用}

预测的目标是在给定信息集 \(\mathcal F_t\) 下预测未来 \(X_{t+h}\)。均方误差意义下的最优预测是条件期望：
\[
  \hat X_{t+h|t}=E(X_{t+h}\mid\mathcal F_t).
\]
若只允许线性预测，则最优预测是向由过去观测张成的线性空间做正交投影。

\section{自回归过程预测}

AR(1)
\[
  X_t=\phi X_{t-1}+\varepsilon_t
\]
的一步预测为
\[
  \hat X_{t+1|t}=\phi X_t,
\]
h 步预测为
\[
  \hat X_{t+h|t}=\phi^hX_t.
\]
预测误差方差为
\[
  \mathrm{var}(X_{t+h}-\hat X_{t+h|t})
  =\sigma^2\sum_{j=0}^{h-1}\phi^{2j}.
\]""",
r"""\section{AR(p) 与一般时间序列预测}

对 AR(p)，一步预测为
\[
  \hat X_{t+1|t}=\phi_1X_t+\cdots+\phi_pX_{t+1-p}.
\]
多步预测可递归计算：未来尚未观测的 \(X\) 用其预测值代替。

\begin{lemma}[因果 AR(p) 预测，原文 Lemma 7.3.1]
若 \(X_t\) 有因果 AR(p) 表示，则基于无限过去的一步预测由 AR 递推直接给出，预测误差为创新 \(\varepsilon_{t+1}\)。
\end{lemma}

对一般线性过程
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j},
\]
若创新可由过去观测恢复，则 h 步预测保留已知创新项、舍去未来创新项：
\[
  \hat X_{t+h|t}=\sum_{j=h}^{\infty}\psi_j\varepsilon_{t+h-j}.
\]""",
r"""\section{有限过去预测与 Durbin-Levinson}

实际中只能使用有限过去 \(X_1,\ldots,X_n\)。最佳线性预测系数由 Toeplitz 正规方程决定。Durbin-Levinson 算法利用 Toeplitz 结构递推求解，大幅降低计算量。

\subsection{Levinson-Durbin 算法}

记 \(\phi_{n,j}\) 为用 \(X_n,\ldots,X_1\) 预测 \(X_{n+1}\) 的系数，\(\phi_{n,n}\) 同时是 n 阶 PACF。递推核心是用上一阶预测误差更新当前阶预测误差。

\subsection{有限与无限预测比较}

原文引入 Baxter 不等式说明：在适当可和条件下，有限过去预测系数会接近无限过去预测系数。这为使用有限样本近似理论预测提供保证。""",
r"""\section{ARMA、Kalman 滤波与非线性预测}

ARMA 预测可通过创新算法或状态空间形式实现。状态空间模型写作
\[
  \alpha_{t+1}=F\alpha_t+G\varepsilon_{t+1},\qquad
  X_t=H\alpha_t.
\]
Kalman 滤波递推更新状态预测和误差协方差，适合处理缺失观测、多变量和更复杂的动态结构。

非线性模型中，ARCH(p) 和 GARCH(1,1) 的重点是预测条件方差。例如 GARCH(1,1)
\[
  X_t=\sigma_tZ_t,\qquad
  \sigma_t^2=\omega+\alpha X_{t-1}^2+\beta\sigma_{t-1}^2.
\]
其下一期波动率预测为
\[
  \hat\sigma_{t+1}^2=\omega+\alpha X_t^2+\beta\sigma_t^2.
\]

\section{Wold 分解与 Kolmogorov 公式}

\begin{theorem}[Wold 分解，原文 Theorem 7.12.1]
任何零均值、有限方差的二阶平稳过程都可分解为确定性部分和不可预测创新驱动的线性部分。纯非确定性部分可写成
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j}.
\]
\end{theorem}

Kolmogorov 公式把最小预测误差方差与谱密度联系起来，说明频域结构也决定可预测性。""",
        ],
        "figs": ["ch07_fig01_ar_forecast.png", "ch07_fig02_forecast_errors.png"],
        "captions": ["AR(1) 递归预测：多步预测逐渐回到长期均值。", "预测误差序列：用于检查预测是否存在系统性偏差或残余相关。"],
        "exercises": [r"用 AR(1) 和 AR(p) 公式计算一步、多步预测；", r"手算 Durbin-Levinson 递推的前几阶；", r"对太阳黑子或温度数据做预测并比较误差；", r"推导 ARCH/GARCH 条件方差预测。"],
        "summary": "第 7 章把投影理论落实为预测算法。AR 预测可递归计算，有限过去预测由 Durbin-Levinson 高效求解，ARMA 可放入 Kalman 滤波框架，非线性模型则常以条件方差预测为核心。"
    },
]


SPECS.extend([
    {
        "code": "ch08",
        "dir": "chapters/ch08_estimation_of_the_mean_and_covariance",
        "file": "第08章_Estimation_mean_covariance_均值与协方差估计.tex",
        "en": "Estimation of the mean and covariance",
        "zh": "均值与协方差估计",
        "title": r"第 8 章 \quad Estimation of the mean and covariance / 均值与协方差估计",
        "objectives": [r"推导相关序列下样本均值的抽样性质；", r"定义样本自协方差和样本自相关；", r"理解自相关检验、Portmanteau 检验及稳健版本；", r"掌握 Newey-West/HAC 长期方差估计；", r"区分长记忆和均值结构变化。"],
        "sections": [
r"""\section{均值估计}

样本均值仍定义为
\[
  \bar X_n=\frac1n\sum_{t=1}^n X_t.
\]
若 \(\{X_t\}\) 为平稳线性过程且协方差绝对可和，则
\[
  \sqrt n(\bar X_n-\mu)\Rightarrow N(0,\sigma_L^2),
\qquad
  \sigma_L^2=\sum_{k=-\infty}^{\infty}c(k).
\]
\begin{theorem}[样本均值的渐近性质，原文 Theorem 8.1.1]
在线性时间序列和适当矩条件下，样本均值相合且渐近正态；渐近方差为长期方差，而不是单期方差 \(c(0)\)。
\end{theorem}""",
r"""\section{协方差估计}

经验自协方差定义为
\[
  \hat c(h)=\frac1n\sum_{t=1}^{n-h}(X_t-\bar X)(X_{t+h}-\bar X),
\]
样本 ACF 为 \(\hat\rho(h)=\hat c(h)/\hat c(0)\)。

\begin{lemma}[经验协方差，原文 Lemma 8.2.1]
若均值已知或由样本均值替代，在平稳和矩条件下，\(\hat c(h)\) 是 \(c(h)\) 的相合估计。
\end{lemma}

\begin{theorem}[样本自协方差渐近分布，原文 Theorem 8.2.1--8.2.3]
对满足短记忆和四阶矩条件的线性序列，有限个样本自协方差组成的向量渐近正态，其协方差由二阶和四阶累积量决定。
\end{theorem}""",
r"""\section{相关性检查}

白噪声检验常基于若干阶样本自相关。Box-Pierce/Ljung-Box 型统计量形如
\[
  Q_m=n\sum_{h=1}^m\hat\rho(h)^2
\]
或带有限样本修正。若序列为白噪声，\(Q_m\) 近似服从 \(\chi_m^2\)。

\subsection{稳健 Portmanteau 检验}

当存在条件异方差或更一般弱依赖时，普通 Portmanteau 检验的方差估计可能失真。稳健版本用 HAC 型协方差替代简单方差，以保持检验大小。

\section{偏相关检查}

样本 PACF 用于识别 AR 阶数。若真实模型为 AR(p)，则 p 阶之后的理论 PACF 为 0；样本 PACF 可用近似置信带判断是否显著。""",
r"""\section{Newey-West 估计与拟合优度}

长期方差
\[
  \sigma_L^2=\sum_{k=-\infty}^{\infty}c(k)
\]
可用截断加权估计：
\[
  \hat\sigma_L^2=\hat c(0)+2\sum_{k=1}^{m}w_k\hat c(k),
\]
其中 Bartlett 权重为
\[
  w_k=1-\frac{k}{m+1}.
\]
这就是 Newey-West/HAC 估计的核心形式。

拟合优度检查通常对模型残差作 ACF、PACF 和 Portmanteau 检验。如果模型捕捉了线性依赖，残差应接近白噪声。

\section{长记忆与结构变化}

原文提醒：样本 ACF 缓慢衰减可能来自长记忆，也可能来自均值变化或趋势未处理。二者在图形上相似，但统计含义不同，需要结合趋势建模、分段分析和频域诊断判断。""",
        ],
        "figs": ["ch08_fig01_sample_mean_dependence.png", "ch08_fig02_sample_acf.png"],
        "captions": ["不同相关强度下样本均值的抽样分布：相关性越强，有效样本量越小。", "样本 ACF 示例：估计序列在不同滞后上的线性依赖。"],
        "exercises": [r"在 iid、MA(1)、AR(1) 条件下推导样本自协方差的方差；", r"用 block bootstrap 估计样本均值的有限样本分布；", r"实现 Portmanteau 检验和稳健版本；", r"计算 Newey-West 标准误并比较普通标准误。"],
        "summary": "第 8 章把平稳理论转化为可计算估计量。均值、协方差、ACF、PACF 和长期方差估计是时间序列实证分析的基本工具，其中关键始终是正确处理相关性。"
    },
    {
        "code": "ch09",
        "dir": "chapters/ch09_parameter_estimation",
        "file": "第09章_Parameter_estimation_参数估计.tex",
        "en": "Parameter estimation",
        "zh": "参数估计",
        "title": r"第 9 章 \quad Parameter estimation / 参数估计",
        "objectives": [r"掌握 AR 模型的 Yule-Walker、条件最小二乘和高斯似然估计；", r"理解 Burg 算法与偏自相关递推；", r"描述 AR 估计量的抽样性质；", r"掌握 ARMA 的精确/近似高斯似然和 Kalman 滤波估计；", r"了解 Hannan-Rissanen 与 ARCH 准最大似然。"],
        "sections": [
r"""\section{自回归模型估计}

AR(p) 模型为
\[
  X_t=\phi_1X_{t-1}+\cdots+\phi_pX_{t-p}+\varepsilon_t.
\]
\subsection{Yule-Walker 估计}

理论方程为
\[
  \Gamma_p\phi=\gamma_p,
\]
其中 \(\Gamma_p=(c(i-j))_{i,j=1}^p\)，\(\gamma_p=(c(1),\ldots,c(p))'\)。用样本自协方差替代即可得
\[
  \hat\phi_{YW}=\hat\Gamma_p^{-1}\hat\gamma_p.
\]

\subsection{高斯似然}

若 \(X=(X_1,\ldots,X_n)'\sim N(0,\Sigma_\theta)\)，高斯负对数似然差一个常数为
\[
  \ell(\theta)=\log|\Sigma_\theta|+X'\Sigma_\theta^{-1}X.
\]
该形式精确但计算协方差矩阵和逆矩阵成本较高。""",
r"""\section{条件高斯似然与最小二乘}

条件在初始 \(X_1,\ldots,X_p\) 上，AR(p) 的条件残差为
\[
  e_t(\phi)=X_t-\phi_1X_{t-1}-\cdots-\phi_pX_{t-p}.
\]
条件最小二乘估计为
\[
  \hat\phi_{CLS}
  =\arg\min_\phi\sum_{t=p+1}^n e_t(\phi)^2.
\]
它把 AR 估计转化为普通回归问题。

\subsection{Burg 算法}

Burg 算法通过同时最小化前向和后向预测误差估计反射系数，保证估计得到的 AR 模型稳定。其递推与 Levinson-Durbin 和 PACF 紧密相关。""",
r"""\section{AR 估计量的抽样性质}

\begin{definition}[鞅差，原文 Definition 9.1.1]
若 \(E(Z_t\mid\mathcal F_{t-1})=0\)，则称 \(\{Z_t\}\) 为鞅差序列。
\end{definition}

在稳定 AR 模型和适当矩条件下，Yule-Walker、条件最小二乘和高斯似然估计量通常相合且渐近正态：
\[
  \sqrt n(\hat\phi-\phi_0)\Rightarrow N(0,V).
\]
证明核心是把估计方程展开为鞅差和可忽略项。""",
r"""\section{ARMA 模型估计}

ARMA(p,q)
\[
  \phi(B)X_t=\theta(B)\varepsilon_t
\]
的似然需要根据参数递归计算创新。常见方法包括精确高斯最大似然、近似高斯似然和 Kalman 滤波。

\begin{theorem}[ARMA GMLE 抽样性质，原文 Theorem 9.2.1]
在因果、可逆、可识别和矩条件下，ARMA 高斯最大似然估计量相合并渐近正态。
\end{theorem}

\subsection{Hannan-Rissanen 方法}

该方法先用高阶 AR 近似 ARMA 的 \(AR(\infty)\) 表示，估计创新，再用回归估计 ARMA 参数，是一种计算上较快的初值或估计方案。

\section{ARCH 准最大似然}

ARCH/GARCH 中即使创新非高斯，也常使用高斯准似然。只要条件均值和条件方差设定正确，参数仍可具有良好渐近性质。""",
        ],
        "figs": ["ch09_fig01_yule_walker_sampling.png", "ch09_fig02_cls_ar1.png"],
        "captions": ["Yule-Walker AR(1) 估计量的抽样分布：样本量有限时估计量围绕真值波动。", r"AR(1) 条件最小二乘：把 \(X_t\) 对 \(X_{t-1}\) 做回归得到参数估计。"],
        "exercises": [r"用 OLS、Yule-Walker 和 MLE 估计同一 AR 模型并比较；", r"推导 AR(1) 高斯似然的简单形式；", r"实现 Burg 算法或调用库函数比较结果；", r"估计随机系数 AR 或 ARCH 模型。"],
        "summary": "第 9 章集中讨论模型参数如何从数据中估计。AR 模型可由协方差方程、回归或似然估计；ARMA 估计更依赖创新递推和数值优化；渐近理论则解释估计误差如何随样本量缩小。"
    },
    {
        "code": "ch10",
        "dir": "chapters/ch10_spectral_representations",
        "file": "第10章_Spectral_Representations_谱表示.tex",
        "en": "Spectral Representations",
        "zh": "谱表示",
        "title": r"第 10 章 \quad Spectral Representations / 谱表示",
        "objectives": [r"回顾 DFT 在周期检测中的作用；", r"理解平稳序列 DFT 的近似不相关性；", r"掌握谱密度、谱分布和 Bochner/Herglotz 定理；", r"理解 Cramer 谱表示定理；", r"推导 MA、AR、ARMA 的谱密度。"],
        "sections": [
r"""\section{Fourier 变换的使用回顾}

前面章节已经用 DFT 找周期。对 \(X_1,\ldots,X_n\)，DFT 为
\[
  J_n(\omega)=\frac1{\sqrt n}\sum_{t=1}^n X_t e^{it\omega},
\]
周期图为 \(I_n(\omega)=|J_n(\omega)|^2\)。本章把频域工具从周期检测推广到平稳过程的完整二阶表示。

\section{DFT 的近似不相关性}

\begin{lemma}[原文 Lemma 10.2.1]
若 \(\{X_t\}\) 二阶平稳且自协方差绝对可和，则不同 Fourier 频率处的 DFT 近似不相关：
\[
  \mathrm{cov}\{J_n(\omega_j),J_n(\omega_k)\}\approx0,\qquad j\ne k.
\]
同一频率处的方差近似为谱密度。
\end{lemma}

该性质解释了为什么频域似然和 Whittle 似然可把复杂相关矩阵近似分解为频率上的独立贡献。""",
r"""\section{谱表示结果概览}

频域分析的中心思想是：平稳序列的协方差函数和频率能量分布互为 Fourier 对。

\subsection{谱密度}

若 \(\sum_k|c(k)|<\infty\)，谱密度定义为
\[
  f(\omega)=\frac1{2\pi}\sum_{k=-\infty}^{\infty}c(k)e^{-ik\omega}.
\]
反演公式为
\[
  c(k)=\int_{-\pi}^{\pi}e^{ik\omega}f(\omega)\,d\omega.
\]

\begin{theorem}[谱密度非负性，原文 Theorem 10.4.1]
合法协方差序列的谱密度非负；反过来，非负可积函数通过反演公式定义合法协方差。
\end{theorem}""",
r"""\section{谱分布与 Bochner 定理}

若协方差不绝对可和，也可用谱分布 \(F\) 表示：
\[
  c(k)=\int_{-\pi}^{\pi}e^{ik\omega}\,dF(\omega).
\]
\begin{theorem}[Herglotz/Bochner 定理，原文 Theorem 10.4.2]
序列 \(c(k)\) 非负定，当且仅当存在有限非负测度 \(F\)，使上述表示成立。
\end{theorem}

\section{谱表示定理}

\begin{theorem}[Cramer 谱表示，原文 Theorem 10.5.1]
零均值二阶平稳过程可写成
\[
  X_t=\int_{-\pi}^{\pi}e^{it\omega}\,dZ(\omega),
\]
其中 \(Z(\omega)\) 是正交增量过程，且增量方差由谱分布决定。
\end{theorem}

这一定理是 Wold 分解在频域中的对应物。""",
r"""\section{MA、AR 和 ARMA 的谱密度}

线性过程
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j}
\]
的谱密度为
\[
  f_X(\omega)=\frac{\sigma^2}{2\pi}
  \left|\sum_{j=0}^{\infty}\psi_je^{-ij\omega}\right|^2.
\]
ARMA(p,q) 的谱密度为
\[
  f_X(\omega)=\frac{\sigma^2}{2\pi}
  \frac{|\theta(e^{-i\omega})|^2}{|\phi(e^{-i\omega})|^2}.
\]
AR 根接近单位圆会在相应频率附近产生高谱峰。

\section{高阶谱与扩展}

原文还介绍累积量和高阶谱。二阶谱描述协方差结构，高阶谱则可捕捉非高斯和非线性依赖。缺失观测情形下，谱密度估计还需修正采样机制带来的影响。""",
        ],
        "figs": ["ch10_fig01_spectral_density.png", "ch10_fig02_dft_energy.png"],
        "captions": ["AR 与 MA 谱密度形态：频域中不同模型表现为不同频率能量分布。", "AR(1) 序列的 DFT 能量：低频能量较强对应高持续性。"],
        "exercises": [r"推导 MA(1)、AR(1) 和 ARMA(p,q) 谱密度；", r"模拟 AR(2)，观察 DFT 和周期图峰值；", r"验证协方差和谱密度的 Fourier 反演；", r"阅读高阶谱定义并联系非高斯过程。"],
        "summary": "第 10 章给出了平稳过程的频域语言。协方差函数、谱密度和谱分布互相等价，DFT 近似去相关使频域估计成为可能，ARMA 谱密度则把模型根的位置转化为频率峰值。"
    },
])


SPECS.extend([
    {
        "code": "ch11",
        "dir": "chapters/ch11_spectral_analysis",
        "file": "第11章_Spectral_Analysis_谱分析.tex",
        "en": "Spectral Analysis",
        "zh": "谱分析",
        "title": r"第 11 章 \quad Spectral Analysis / 谱分析",
        "objectives": [r"理解 DFT 和周期图的抽样分布；", r"掌握谱密度估计的滞后窗和平滑周期图方法；", r"理解 Whittle 似然及其与高斯似然的关系；", r"了解比率统计在时间序列中的作用；", r"进行线性模型拟合优度检验。"],
        "sections": [
r"""\section{DFT 与周期图}

周期图定义为
\[
  I_n(\omega)=\frac1n\left|\sum_{t=1}^n X_t e^{it\omega}\right|^2.
\]
\begin{lemma}[原文 Lemma 11.1.1]
在零均值二阶平稳和短记忆条件下，DFT 的二阶矩由谱密度近似控制，不同 Fourier 频率近似不相关。
\end{lemma}

周期图是谱密度的原始估计，但它本身不相合：样本量增大时方差并不自动消失。""",
r"""\section{DFT 和周期图的分布}

对线性过程，在适当系数可和和矩条件下，
\[
  J_n(\omega_j)\approx \mathcal{CN}(0,2\pi f(\omega_j)),
\]
因此
\[
  \frac{I_n(\omega_j)}{2\pi f(\omega_j)}
\]
近似服从指数分布。原文用一系列引理和定理证明这一近似，并说明不同频率近似独立。""",
r"""\section{谱密度估计}

\subsection{滞后窗估计}

用样本自协方差和窗口 \(w(\cdot)\) 可定义
\[
  \hat f(\omega)=\frac1{2\pi}\sum_{|k|\le m}w(k/m)\hat c(k)e^{-ik\omega}.
\]
窗口截断降低方差，但会引入偏差。

\subsection{平滑周期图}

另一种等价做法是在频域中平均邻近周期图：
\[
  \hat f(\omega)=\sum_j W_m(\omega-\omega_j)I_n(\omega_j).
\]
\begin{theorem}[谱估计抽样性质，原文 Theorem 11.3.1]
在平稳、短记忆和带宽条件下，平滑谱估计渐近无偏且方差随带宽增加而下降。
\end{theorem}""",
r"""\section{Whittle 似然与比率统计}

Whittle 似然把 DFT 近似独立性用于参数估计：
\[
  L_W(\theta)=\sum_{\omega_j}
  \left\{\log f_\theta(\omega_j)+\frac{I_n(\omega_j)}{f_\theta(\omega_j)}\right\}.
\]
它近似高斯似然，但避免直接处理大型 Toeplitz 协方差矩阵。

\subsection{比率统计}

若把周期图与拟合谱密度作比
\[
  R(\omega_j)=\frac{I_n(\omega_j)}{f_{\hat\theta}(\omega_j)},
\]
模型拟合良好时，比率应近似白噪声频域形态。原文进一步讨论了基于比率的检验统计量。

\section{拟合优度检验}

线性时间序列模型拟合后，应检查残差和标准化周期图是否仍含系统性频率结构。谱域拟合优度检验与第 8 章的 ACF/Portmanteau 检验互为补充。""",
        ],
        "figs": ["ch11_fig01_smoothed_periodogram.png", "ch11_fig02_two_frequency_signal.png"],
        "captions": ["周期图平滑：原始周期图方差大，平滑后更接近谱密度形状。", "双频信号：时域叠加的周期成分会在频域形成多个峰。"],
        "exercises": [r"模拟线性过程并比较周期图与理论谱密度；", r"实现 Bartlett、Daniell 等平滑窗口；", r"用 Whittle 似然拟合 ARMA 模型；", r"基于标准化周期图检查模型拟合优度。"],
        "summary": "第 11 章从谱表示走向谱估计。周期图是入口但不相合，平滑和窗口提供稳定估计；Whittle 似然利用频域近似独立性，给出高效的参数估计和拟合检验工具。"
    },
    {
        "code": "ch12",
        "dir": "chapters/ch12_multivariate_time_series",
        "file": "第12章_Multivariate_time_series_多元时间序列.tex",
        "en": "Multivariate time series",
        "zh": "多元时间序列",
        "title": r"第 12 章 \quad Multivariate time series / 多元时间序列",
        "objectives": [r"复习序列卷积和矩阵谱表示；", r"建立多元时间序列回归模型；", r"理解条件独立、偏相关和相干性；", r"定义交叉谱密度和谱偏相关；", r"解释逆谱密度矩阵的条件依赖含义。"],
        "sections": [
r"""\section{背景}

\subsection{序列与卷积}

若 \(a=\{a_j\}\)、\(b=\{b_j\}\)，卷积定义为
\[
  (a*b)_k=\sum_j a_jb_{k-j}.
\]
多元线性滤波中，系数可为矩阵，卷积描述不同序列和不同滞后之间的相互作用。

\subsection{谱表示}

多元平稳序列 \(X_t\in\mathbb R^d\) 的自协方差矩阵为
\[
  \Gamma(h)=E(X_{t+h}X_t').
\]
谱密度矩阵定义为
\[
  f(\omega)=\frac1{2\pi}\sum_{h=-\infty}^{\infty}\Gamma(h)e^{-ih\omega}.
\]
它在每个频率上是 Hermitian 非负定矩阵。""",
r"""\section{多元时间序列回归}

多元线性模型可写为
\[
  Y_t=\sum_{j}A_jX_{t-j}+\varepsilon_t.
\]
向量自回归 VAR(p) 是典型例子：
\[
  X_t=A_1X_{t-1}+\cdots+A_pX_{t-p}+\varepsilon_t.
\]
矩阵 \(A_j\) 描述一个变量过去值对另一个变量当前值的动态影响。

\subsection{条件独立}

若一个分量在给定其他序列后不能由另一分量改善预测，则称二者条件线性不相关。高斯情形下，这可进一步解释为条件独立。""",
r"""\section{偏相关、相干性与交叉谱}

两个序列的交叉谱密度 \(f_{12}(\omega)\) 是交叉协方差的 Fourier 变换。相干性定义为
\[
  \mathrm{coh}_{12}(\omega)
  =\frac{|f_{12}(\omega)|^2}{f_{11}(\omega)f_{22}(\omega)}.
\]
它是频域中的相关系数平方，取值在 \([0,1]\)。

谱偏相关是在给定其他序列后定义的频域相关，类似多元分析中的偏相关。""",
r"""\section{逆谱密度矩阵}

设
\[
  g(\omega)=f(\omega)^{-1}.
\]
逆谱密度矩阵的零元素表示频域条件不相关结构。对高斯平稳序列，若 \(g_{ij}(\omega)=0\) 对所有 \(\omega\) 成立，则第 \(i\) 和第 \(j\) 个序列在给定其他序列后条件独立。

原文还证明了公式 (12.6)，把谱偏相关和逆谱密度矩阵联系起来。这一结构是高维多元时间序列图模型的基础。""",
        ],
        "figs": ["ch12_fig01_var_series.png", "ch12_fig02_coherence.png"],
        "captions": ["二元 VAR(1) 模拟序列：两个变量通过滞后矩阵相互影响。", "相干性曲线：展示两个序列在不同频率上的线性关联强度。"],
        "exercises": [r"计算二元 VAR 的自协方差矩阵；", r"估计交叉谱和相干性；", r"解释逆谱密度矩阵零元素；", r"比较时域偏相关与频域谱偏相关。"],
        "summary": "第 12 章把单变量频域理论推广到矩阵情形。多元序列的关键不只是每个变量自身的谱密度，还包括交叉谱、相干性和逆谱密度所揭示的条件依赖网络。"
    },
    {
        "code": "ch13",
        "dir": "chapters/ch13_nonlinear_time_series_models",
        "file": "第13章_Nonlinear_Time_Series_Models_非线性时间序列模型.tex",
        "en": "Nonlinear Time Series Models",
        "zh": "非线性时间序列模型",
        "title": r"第 13 章 \quad Nonlinear Time Series Models / 非线性时间序列模型",
        "objectives": [r"理解非线性递推模型的平稳解条件；", r"用金融数据动机说明波动聚集；", r"掌握 ARCH、GARCH、IGARCH 模型；", r"理解双线性模型和随机系数 AR；", r"了解非参数时间序列模型。"],
        "sections": [
r"""\section{非线性模型的一般形式}

原文以随机递推方程为入口：
\[
  X_t=F(X_{t-1},\varepsilon_t).
\]
\begin{theorem}[Brandt 定理，原文 Theorem 13.0.1]
在随机映射满足平均收缩等条件时，上述递推存在唯一严格平稳解，并可由过去创新的可测函数表示。
\end{theorem}

该定理为 ARCH、GARCH 和双线性模型的存在性提供统一思路。""",
r"""\section{数据动机}

金融收益序列常呈现三个特征：收益均值相关弱、平方收益或绝对收益相关强、波动成团出现。线性 ARMA 均值模型难以解释这种条件方差变化，因此需要非线性模型。

\section{ARCH 模型}

ARCH(p) 定义为
\[
  X_t=\sigma_t Z_t,\qquad
  \sigma_t^2=a_0+a_1X_{t-1}^2+\cdots+a_pX_{t-p}^2,
\]
其中 \(Z_t\) 通常为 iid 标准化创新。若 \(a_i\ge0\)，可保证条件方差非负。

\subsection{ARCH 的特征}

虽然 \(X_t\) 可不相关，但 \(X_t^2\) 相关，因此模型能刻画波动聚集。""",
r"""\section{GARCH 模型}

GARCH(1,1) 为
\[
  X_t=\sigma_tZ_t,\qquad
  \sigma_t^2=a_0+a_1X_{t-1}^2+b_1\sigma_{t-1}^2.
\]
若 \(a_1+b_1<1\)，常见二阶平稳条件成立，且
\[
  E(X_t^2)=\frac{a_0}{1-a_1-b_1}.
\]

\begin{example}[GARCH(1,1) 反演，原文 Example 13.3.1]
当 \(b_1<1\) 时，\(\sigma_t^2\) 可展开为过去平方收益的无限加权和，权重按 \(b_1\) 衰减。
\end{example}

\begin{definition}[IGARCH，原文 Definition 13.3.1]
若 GARCH 模型满足 \(a_1+b_1=1\)，称为 IGARCH。此时波动冲击具有极强持续性。
\end{definition}""",
r"""\section{双线性模型与非参数模型}

双线性模型包含过去观测和过去创新的乘积项，例如
\[
  X_t=\phi X_{t-1}+\theta\varepsilon_{t-1}
      +bX_{t-1}\varepsilon_{t-1}+\varepsilon_t.
\]
它比线性 ARMA 更灵活，可产生非线性依赖。

非参数时间序列模型则把条件均值或条件方差写成未知函数：
\[
  X_t=m(X_{t-1},\ldots,X_{t-p})+\varepsilon_t,
\]
再用核方法、局部线性、样条或机器学习方法估计 \(m\)。原文将其作为高级扩展。""",
        ],
        "figs": ["ch13_fig01_garch_returns.png", "ch13_fig02_conditional_volatility.png"],
        "captions": ["GARCH(1,1) 收益模拟：收益本身均值稳定，但波动呈现聚集。", "条件波动率路径：GARCH 模型通过递推方差刻画风险随时间变化。"],
        "exercises": [r"推导 ARCH(1) 二阶平稳条件；", r"模拟 ARCH 与 GARCH 并比较 ACF 和平方 ACF；", r"分析 IGARCH 的持续性；", r"模拟双线性或随机系数 AR 模型。"],
        "summary": "第 13 章从线性均值模型转向条件方差和非线性依赖。ARCH/GARCH 解释金融数据的波动聚集，双线性和非参数模型则展示了更一般的非线性动态。"
    },
])


SPECS.extend([
    {
        "code": "ch14",
        "dir": "chapters/ch14_consistency_and_asymptotic_normality_of_esti",
        "file": "第14章_Consistency_asymptotic_normality_一致性与渐近正态性.tex",
        "en": "Consistency and asymptotic normality of estimators",
        "zh": "一致性与渐近正态性",
        "title": r"第 14 章 \quad Consistency and asymptotic normality / 一致性与渐近正态性",
        "objectives": [r"区分几乎必然收敛、依概率收敛和分布收敛；", r"定义估计量的一致性和渐近正态性；", r"掌握 argmax/argmin 一致性定理；", r"理解随机等连续和随机 Ascoli 引理；", r"应用于 Hannan-Rissanen 和高斯 MLE。"],
        "sections": [
r"""\section{收敛模式}

\begin{definition}[收敛，原文 Definition 14.1.1]
若 \(X_n\to X\) 几乎处处，记 \(X_n\xrightarrow{a.s.}X\)；若对任意 \(\epsilon>0\)，
\[
  P(|X_n-X|>\epsilon)\to0,
\]
记 \(X_n\xrightarrow{p}X\)；若分布函数收敛，记 \(X_n\Rightarrow X\)。
\end{definition}

\begin{definition}[有界性，原文 Definition 14.1.2]
\(X_n=O_p(1)\) 表示随机变量序列依概率有界，\(X_n=o_p(1)\) 表示依概率收敛到 0。
\end{definition}""",
r"""\section{抽样性质与一致性}

\begin{definition}[一致估计，原文 Definition 14.2.1]
若估计量 \(\hat a_n\) 满足
\[
  \hat a_n\xrightarrow{a.s.}a_0
\]
或 \(\hat a_n\xrightarrow{p}a_0\)，则分别称为几乎必然一致或依概率一致。
\end{definition}

\section{估计量的几乎必然收敛}

\begin{definition}[一致收敛，原文 Definition 14.3.1]
若
\[
  \sup_{a\in\Theta}|L_n(a)-L(a)|\xrightarrow{a.s.}0,
\]
称 \(L_n\) 几乎必然一致收敛到 \(L\)。
\end{definition}

\begin{theorem}[Argmax 一致性，原文 Theorem 14.3.1]
若 \(\hat a_n=\arg\max L_n(a)\)，\(a_0=\arg\max L(a)\)，且 \(L_n\) 一致收敛到 \(L\)、\(L\) 的最大点唯一，则 \(\hat a_n\to a_0\)。
\end{theorem}""",
r"""\section{随机等连续与玩具例子}

\begin{definition}[随机等连续，原文 Definition 14.3.2]
随机函数族在参数空间上若小距离参数点的函数值差可一致控制，则称随机等连续。
\end{definition}

\begin{theorem}[随机 Ascoli 引理，原文 Theorem 14.3.2]
若参数空间紧、随机函数点态收敛且随机等连续，则可推出一致收敛。
\end{theorem}

原文用 AR(1) 估计的玩具例子说明如何把样本目标函数写成极限函数加误差项，并证明
\[
  \hat\phi\xrightarrow{a.s.}\phi.
\]""",
r"""\section{渐近正态性}

若目标函数 \(L_n(\theta)\) 在真值附近可二阶展开，则一阶条件给出
\[
  0=L_n'(\hat\theta)
  =L_n'(\theta_0)+L_n''(\theta_0)(\hat\theta-\theta_0)+R_n.
\]
若
\[
  \sqrt n L_n'(\theta_0)\Rightarrow N(0,V),
  \qquad
  L_n''(\theta_0)\xrightarrow{p}H,
\]
则
\[
  \sqrt n(\hat\theta-\theta_0)\Rightarrow N(0,H^{-1}VH^{-1}).
\]

\section{Hannan-Rissanen 与 GMLE 渐近性质}

原文后半部分把上述工具用于 Hannan-Rissanen 估计和 ARMA 高斯最大似然。核心任务是证明初步 AR 近似误差足够小、目标函数一致收敛，并用 Taylor 展开得到渐近正态性。""",
        ],
        "figs": ["ch14_fig01_consistency_mse.png", "ch14_fig02_asymptotic_normality.png"],
        "captions": ["一致性示意：样本量增大时样本均值的均方误差下降。", "渐近正态性示意：标准化估计误差逐渐接近正态分布。"],
        "exercises": [r"判断不同收敛模式之间的关系；", r"验证一个目标函数的一致收敛；", r"用 AR(1) 估计推导一致性；", r"对 M 估计量做 Taylor 展开得到渐近正态。"],
        "summary": "第 14 章是全书理论证明工具箱。一致性来自目标函数的统一收敛和唯一极值，渐近正态性来自一阶条件、Taylor 展开和中心极限定理；这些工具支撑前面估计方法的抽样性质。"
    },
    {
        "code": "ch15",
        "dir": "chapters/ch15_residual_bootstrap_for_estimation_in_autoreg",
        "file": "第15章_Residual_Bootstrap_残差Bootstrap.tex",
        "en": "Residual Bootstrap for estimation in autoregressive processes",
        "zh": "自回归估计中的残差 Bootstrap",
        "title": r"第 15 章 \quad Residual Bootstrap / 残差 Bootstrap",
        "objectives": [r"理解 AR 模型残差 Bootstrap 的算法步骤；", r"区分真实残差、中心化残差和 bootstrap 残差；", r"理解 bootstrap 估计量抽样性质；", r"掌握 Wasserstein/分布距离在证明中的作用；", r"说明何时 residual bootstrap 能近似参数估计分布。"],
        "sections": [
r"""\section{残差 Bootstrap}

对 AR(p)
\[
  X_t=\phi_1X_{t-1}+\cdots+\phi_pX_{t-p}+\varepsilon_t,
\]
先估计 \(\hat\phi\)，得到残差
\[
  \hat\varepsilon_t=X_t-\hat\phi_1X_{t-1}-\cdots-\hat\phi_pX_{t-p}.
\]
中心化后从 \(\{\hat\varepsilon_t-\bar{\hat\varepsilon}\}\) 中有放回抽样，得到 bootstrap 创新 \(\varepsilon_t^+\)，再递推生成
\[
  X_t^+=\hat\phi_1X_{t-1}^++\cdots+\hat\phi_pX_{t-p}^+ + \varepsilon_t^+.
\]
对 bootstrap 样本重新估计参数，重复多次即可近似 \(\hat\phi\) 的抽样分布。""",
r"""\section{残差 Bootstrap 的抽样性质}

原文通过若干引理证明 bootstrap 残差分布接近真实创新分布，并进一步证明 bootstrap 估计量能近似原估计量的分布。

\begin{lemma}[分布距离，原文 Lemma 15.2.1]
两个概率测度在适当距离 \(d(\alpha,\beta)\) 下收敛，可等价刻画相应随机变量分布的弱收敛。
\end{lemma}

\begin{lemma}[bootstrap 残差，原文 Lemma 15.2.2]
在 AR 参数估计相合和残差中心化条件下，bootstrap 残差的经验分布逼近真实创新分布。
\end{lemma}

\begin{lemma}[bootstrap 序列近似，原文 Lemma 15.2.3--15.2.4]
由 bootstrap 创新递推生成的序列，其样本矩阵和协方差项可逼近理论对应量，从而支持 bootstrap 参数估计的渐近有效性。
\end{lemma}""",
r"""\section{算法总结}

残差 Bootstrap 的实务步骤为：
\begin{enumerate}
  \item 拟合 AR(p) 并保存参数 \(\hat\phi\)；
  \item 计算并中心化残差；
  \item 重抽样残差生成 \(\varepsilon_t^+\)；
  \item 使用 \(\hat\phi\) 和 \(\varepsilon_t^+\) 递推生成 \(X_t^+\)；
  \item 对 \(X_t^+\) 重新估计，得到 \(\hat\phi^+\)；
  \item 用 \(\hat\phi^+-\hat\phi\) 的经验分布构造标准误、置信区间或分位数。
\end{enumerate}

该方法依赖 AR 模型设定合理、残差近似独立同分布和参数估计稳定。""",
        ],
        "figs": ["ch15_fig01_residual_bootstrap.png", "ch15_fig02_residuals.png"],
        "captions": ["AR(1) 残差 Bootstrap 参数分布：重抽样近似估计量的不确定性。", "AR(1) 拟合残差图：残差应接近独立同分布创新。"],
        "exercises": [r"手写 AR(1) residual bootstrap 算法；", r"比较正态近似区间和 bootstrap 分位数区间；", r"研究残差未中心化对 bootstrap 的影响；", r"改变 AR 阶数，观察 bootstrap 分布的稳定性。"],
        "summary": "第 15 章把 bootstrap 引入自回归估计。核心思想是用拟合残差近似未知创新分布，再在拟合模型下重造样本。理论部分说明这种重抽样分布何时能逼近真实估计误差分布。"
    },
])


SPECS.extend([
    {
        "code": "appA",
        "dir": "chapters/appA_background",
        "file": "附录A_Background_背景知识.tex",
        "en": "Background",
        "zh": "背景知识",
        "title": r"附录 A \quad Background / 背景知识",
        "objectives": [r"复习常用不等式和概率收敛工具；", r"理解鞅差和 Burkholder 不等式；", r"掌握 Fourier 级数和正交展开；", r"理解 FFT 的分治思想；", r"为正文中的渐近证明和频域计算提供背景。"],
        "sections": [
r"""\section{定义与不等式}

附录首先整理概率界和矩不等式。常用工具包括 Markov 不等式、Chebyshev 不等式、Cauchy-Schwarz 不等式和 Jensen 不等式。例如
\[
  P(|X|>\epsilon)\le \frac{E|X|^p}{\epsilon^p}.
\]

\begin{lemma}[原文 Lemma A.1.1]
若随机变量或随机过程满足给定矩界，则可用最大不等式控制其上确界或部分和，从而推出收敛率。
\end{lemma}

\begin{theorem}[Helly 定理，原文 Theorem A.1.1]
分布函数序列若紧，则存在弱收敛子序列。该结果用于分布收敛的紧性论证。
\end{theorem}""",
r"""\section{鞅}

\begin{definition}[鞅差，原文 Definition A.2.1]
若 \(E(X_t\mid\mathcal F_{t-1})=0\)，则 \(\{X_t\}\) 关于过滤 \(\{\mathcal F_t\}\) 为鞅差序列。
\end{definition}

鞅差是时间序列渐近理论中的核心对象。许多估计方程可分解为鞅差和小余项，然后用鞅中心极限定理或最大不等式处理。""",
r"""\section{Fourier 级数}

周期函数可展开为
\[
  f(x)=a_0+\sum_{k=1}^{\infty}\{a_k\cos(kx)+b_k\sin(kx)\}.
\]
复指数形式为
\[
  f(x)=\sum_{k=-\infty}^{\infty}c_ke^{ikx},
  \qquad
  c_k=\frac1{2\pi}\int_{-\pi}^{\pi}f(x)e^{-ikx}\,dx.
\]
正文中的谱密度、DFT 和周期检测都建立在这一正交展开思想上。""",
r"""\section{Burkholder 不等式与 FFT}

\begin{theorem}[Burkholder 不等式，原文 Theorem A.4.1--A.4.2]
对鞅差部分和 \(S_n=\sum_{t=1}^nY_t\)，其 \(p\) 阶矩可由条件方差和单项矩控制。该工具用于证明时间序列估计中的最大界和收敛率。
\end{theorem}

\section{快速 Fourier 变换}

DFT 定义为
\[
  d(\omega_j)=\sum_{t=0}^{n-1}x_t e^{-i2\pi jt/n}.
\]
当 \(n=2m\) 时，可把偶数项和奇数项分开：
\[
  d_n(j)=d_m^{(even)}(j)+e^{-i2\pi j/n}d_m^{(odd)}(j),
\]
从而递归计算，把复杂度从 \(O(n^2)\) 降到 \(O(n\log n)\)。""",
        ],
        "figs": ["appA_fig01_fourier_series.png", "appA_fig02_fft_energy.png"],
        "captions": ["Fourier 级数近似：用有限个正弦项逼近方波。", "FFT 能量示例：快速 Fourier 变换用于高效计算频域能量。"],
        "exercises": [r"用 Markov 和 Chebyshev 不等式证明简单概率界；", r"验证鞅差的条件期望为 0；", r"计算简单周期函数的 Fourier 系数；", r"手推 \(n=4\) 时 FFT 的偶奇分解。"],
        "summary": "附录 A 收集正文所需的概率和分析工具。鞅不等式支撑渐近证明，Fourier 级数和 FFT 支撑频域表示与计算。"
    },
    {
        "code": "appB",
        "dir": "chapters/appB_mixingales_and_physical_dependence",
        "file": "附录B_Mixingales_physical_dependence_Mixingales与物理依赖.tex",
        "en": "Mixingales and physical dependence",
        "zh": "Mixingales 与物理依赖",
        "title": r"附录 B \quad Mixingales and physical dependence / Mixingales 与物理依赖",
        "objectives": [r"定义 mixingale 并理解其依赖衰减含义；", r"获得几乎必然收敛率；", r"理解 Theorem 14.7.3 的证明结构；", r"掌握物理依赖度量；", r"把 ARMA 过程放入依赖衰减框架。"],
        "sections": [
r"""\section{Mixingale}

\begin{definition}[Mixingale，原文 Definition B.0.1]
设 \(\mathcal F_t\) 为过滤。若随机变量 \(X_t\) 满足对过去和未来条件期望的影响随滞后衰减，例如
\[
  \|E(X_t\mid\mathcal F_{t-m})\|_p\le c_t\psi_m,
\]
其中 \(\psi_m\to0\)，则称 \(\{X_t\}\) 为 mixingale。
\end{definition}

\begin{lemma}[分解，原文 Lemma B.0.1]
mixingale 可分解成若干近似鞅差项和可控余项，因此能使用鞅工具证明收敛。
\end{lemma}""",
r"""\section{几乎必然收敛率}

\begin{lemma}[原文 Lemma B.1.1]
若随机序列 \(S_T\) 的最大二阶矩满足
\[
  E\left(\sup_{t\le T}|S_t|^2\right)\le \phi(T),
\]
则可通过分块和 Borel-Cantelli 引理得到几乎必然收敛率。
\end{lemma}

该节服务于第 14 章估计量收敛率证明：不仅要知道误差趋于 0，还要知道趋于 0 的速度。""",
r"""\section{Theorem 14.7.3 的证明}

原文证明 ARMA 过程在根离单位圆条件下具有足够快的依赖衰减。若
\[
  X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j},
\]
且 \(|\psi_j|\) 几何衰减，则远过去创新对当前的影响迅速变小。

\begin{lemma}[ARMA mixingale 性质，原文 Lemma B.2.1--B.2.2]
满足因果可逆条件的 ARMA 过程可构造为 mixingale，并满足第 14 章所需的几乎必然界。
\end{lemma}""",
r"""\section{物理依赖性质}

物理依赖度量把过程写成
\[
  X_t=G(\ldots,\varepsilon_{t-1},\varepsilon_t).
\]
将某个过去创新 \(\varepsilon_{t-k}\) 替换为独立副本，得到耦合变量 \(X_t^{*(t-k)}\)。依赖度量定义为
\[
  \delta_p(k)=\|X_t-X_t^{*(t-k)}\|_p.
\]
若 \(\delta_p(k)\) 快速衰减，说明遥远冲击对当前影响很小。

\begin{lemma}[原文 Lemma B.3.1]
在适当 \(p\) 阶矩和物理依赖可和条件下，可得到部分和、样本协方差和估计量所需的矩界。
\end{lemma}""",
        ],
        "figs": ["appB_fig01_dependence_decay.png", "appB_fig02_physical_dependence.png"],
        "captions": ["依赖衰减率：几何衰减通常比多项式衰减带来更强的渐近结果。", "物理依赖示意：替换一个早期冲击后，其影响随时间逐渐消失。"],
        "exercises": [r"验证简单 MA(q) 过程的 mixingale 条件；", r"用分块法推出几乎必然收敛率；", r"计算 AR(1) 的物理依赖度量；", r"比较几何衰减和多项式衰减对定理条件的影响。"],
        "summary": "附录 B 提供处理弱依赖过程的技术框架。Mixingale 和物理依赖都在量化“远处冲击影响变小”，它们是第 14 章渐近证明背后的依赖控制工具。"
    },
])


def main() -> None:
    for spec in SPECS:
        path = ROOT / str(spec["dir"]) / str(spec["file"])
        path.write_text(tex_document(spec), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
