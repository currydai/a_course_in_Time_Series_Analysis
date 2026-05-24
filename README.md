# A Course in Time Series Analysis 中文讲义与 Python 实践

本项目把原书 `A course in Time Series Analysis.pdf` 整理为中文主导的时间序列分析讲义，并为每章补充可运行的 Python 实践脚本、图像和教学说明。目标不是逐句机械翻译，而是在保留原书数学结构、定义、定理、例题、证明思路和练习方向的基础上，让中文读者可以按课程方式学习、复现和扩展。

## 根目录交付件

- `main.tex`：合并后的完整 LaTeX 源文件，包含第 1-15 章和附录 A/B。
- `main.pdf`：由 `main.tex` 编译得到的完整中文讲义 PDF。
- `README.md`：项目说明、目录结构和复现方法。
- `TASKLIST.md`：章节整理与检查进度记录。
- `translation_pedagogical_audit.md`：教学覆盖审计报告。
- `A course in Time Series Analysis.pdf`：原始英文 PDF。
- `interactive-learning/`：面向 GitHub Pages 或静态服务器部署的全书交互学习实验室。

## 内容范围

当前完整讲义覆盖以下章节：

1. Introduction / 导论
2. Trends in a time series / 时间序列中的趋势
3. Stationary Time Series / 平稳时间序列
4. Linear time series / 线性时间序列
5. A review of some results from multivariate analysis / 多元分析结果回顾
6. The autocovariance and partial covariance of a stationary time series / 自协方差与偏协方差
7. Prediction / 预测
8. Estimation of the mean and covariance / 均值与协方差估计
9. Parameter estimation / 参数估计
10. Spectral Representations / 谱表示
11. Spectral Analysis / 谱分析
12. Multivariate time series / 多元时间序列
13. Nonlinear Time Series Models / 非线性时间序列模型
14. Consistency and asymptotic normality of estimators / 估计量的一致性与渐近正态性
15. Residual Bootstrap for estimation in autoregressive processes / 自回归估计中的残差 Bootstrap
16. Appendix A: Background / 背景知识
17. Appendix B: Mixingales and physical dependence / Mixingales 与物理依赖

每章通常包含：

- 本章学习目标
- 贴近原书结构的中文讲解
- 核心公式、定义、定理、引理、命题和例题
- 与原书 R 思路对应的 Python 实践说明
- Python 脚本生成的图像及图后解释
- 面向复习和教学的练习方向

## 目录结构

```text
.
├── main.tex
├── main.pdf
├── README.md
├── TASKLIST.md
├── translation_pedagogical_audit.md
├── A course in Time Series Analysis.pdf
├── chapters/
│   ├── ch01_introduction/
│   │   ├── 第01章_Introduction_导论.tex
│   │   ├── 第01章_Introduction_导论.pdf
│   │   ├── figures/
│   │   └── scripts/
│   ├── ...
│   ├── ch15_residual_bootstrap_for_estimation_in_autoreg/
│   ├── appA_background/
│   └── appB_mixingales_and_physical_dependence/
└── tools/
    ├── build_combined_tex.py
    ├── audit_translation_coverage.py
    └── expand_chapter_translations.py
```

`chapters/` 下每个章节目录都是一个相对独立的教学单元：可以单独编译该章 `.tex`，也可以通过根目录的 `main.tex` 阅读全书合并版。

## 如何编译完整 PDF

本项目使用 XeLaTeX 编译中文文档。若本机已安装 TeX Live，可在根目录运行：

```powershell
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

如果使用本项目当前验证过的 TeX Live 路径，也可以运行：

```powershell
& "D:\texlive\2026\bin\windows\xelatex.exe" -interaction=nonstopmode -halt-on-error main.tex
& "D:\texlive\2026\bin\windows\xelatex.exe" -interaction=nonstopmode -halt-on-error main.tex
```

通常需要编译两次，以确保目录页和页码信息完整刷新。

## 如何打开交互学习实验室

交互版是纯静态网页，可直接打开：

```text
interactive-learning/index.html
```

也可以在根目录启动静态服务器：

```powershell
python -m http.server 8000
```

然后访问：

```text
http://localhost:8000/interactive-learning/
```

若部署到 GitHub Pages，访问路径通常是：

```text
https://用户名.github.io/仓库名/interactive-learning/
```

## 如何重新生成 main.tex

根目录 `main.tex` 由分章 `.tex` 自动合并生成。修改任一章节后，可运行：

```powershell
python tools\build_combined_tex.py
```

该脚本会按第 1-15 章、附录 A、附录 B 的顺序抽取各章正文，统一导言区，并把各章 `figures/` 路径加入完整文档的图片搜索路径。

## 如何运行教学覆盖审计

项目提供了一个轻量审计脚本，用来检查中文讲义与英文抽取文本在教学结构上的接近程度：

```powershell
python tools\audit_translation_coverage.py
```

审计指标包括章节结构、原文小节覆盖、定理/例题/练习等关键项覆盖、正文密度和 PDF 是否存在。当前结果为：

```text
17 PASS, 0 REVIEW, 0 FAIL
```

这表示所有章节在“教学效果接近原文”的标准下通过检查。它不是逐句长度审计，也不声称中文正文逐字多于英文原文；重点是课程学习所需的结构、公式和关键内容是否覆盖到位。

## Python 实践部分

各章的 Python 脚本位于对应章节目录的 `scripts/` 中，生成图像通常输出到该章 `figures/`。脚本用于展示原书中 R 示例背后的计算思想，例如：

- 时间序列模拟与滤波
- 趋势估计与差分
- 自协方差、自相关和偏自相关
- ARMA/VAR/GARCH 等模型示例
- 谱密度、周期图和平滑周期图
- Bootstrap 和渐近性质的数值说明

读者可以先阅读 PDF 中的图后说明，再打开对应脚本查看实现细节。

## 阅读建议

如果是第一次学习时间序列，建议按章节顺序阅读第 1-11 章，先建立时域与频域的基本框架；之后再进入第 12 章多元时间序列、第 13 章非线性模型、第 14 章渐近理论和第 15 章 Bootstrap。附录 A/B 可以在遇到 Fourier、FFT、mixingale、physical dependence 等概念时回查。

如果目标是工程实践，可以从每章的 Python 脚本开始，先复现实验图，再回到讲义正文理解公式和假设。

## 当前状态

- 分章 PDF 已生成。
- 根目录完整 `main.tex` 和 `main.pdf` 已生成。
- 教学覆盖审计全部 PASS。
- XeLaTeX 编译已验证通过。

后续可继续做的增强包括：统一全书定理和例题编号风格、补充真实数据下载缓存方案、进一步扩展每章 Python 案例数量、增加参考文献和术语索引。
