# A Course in Time Series Analysis 中文讲义与 Python 实践任务清单

原始文档：`A course in Time Series Analysis.pdf`

目标产物：按章节建立独立文件夹，每章包含中文主导的 LaTeX 讲义、Python 工程实践脚本、脚本生成的图像，以及可插入 LaTeX 的案例解释。

状态标记：
- `[x]` 已完成
- `[~]` 进行中
- `[ ]` 未开始
- `[?]` 教学覆盖基本接近，建议继续补强

## 全局任务

- [x] 读取 PDF 元数据、页数和目录结构。
- [x] 建立章节化工程目录。
- [x] 建立任务清单，便于持续生成和标注进度。
- [x] 建立 PDF 文本抽取工具。
- [x] 建立第 1 章 LaTeX 中文讲义模板。
- [x] 配置并验证本机 LaTeX 编译环境；已使用 `D:\texlive\2026\bin\windows\xelatex.exe` 成功编译全部章节。
- [x] 建立教学覆盖审计脚本：`tools/audit_translation_coverage.py`。
- [x] 按“教学效果接近原文”标准重新审计，当前 17 个章节/附录全部 PASS。
- [ ] 建立全书统一 LaTeX 样式文件，集中管理字体、标题、定理、例题、代码和图表样式。
- [x] 建立全书总入口 `main.tex`，可按章节组合编译，并已生成根目录 `main.pdf`。
- [x] 建立根目录 `README.md`，面向读者说明项目内容、结构、编译和审计方法。
- [x] 对每章完成 XeLaTeX 编译检查，并生成对应 PDF。

## 分章节任务

- [x] 第 1 章 Introduction / 导论
  - [x] 章节文件夹：`chapters/ch01_introduction`
  - [x] 中文 LaTeX 讲义：`第01章_Introduction_导论.tex`
  - [x] Python 实践脚本：`scripts/ch01_generate_figures.py`
  - [x] 生成图：独立白噪声、模拟 SOI、太阳黑子、移动平均滤波
  - [x] 标注任务完成状态

- [x] 第 2 章 Trends in a time series / 时间序列中的趋势（PASS：教学覆盖审计通过）
- [x] 第 3 章 Stationary Time Series / 平稳时间序列（PASS：教学覆盖审计通过）
- [x] 第 4 章 Linear time series / 线性时间序列（PASS：教学覆盖审计通过）
- [x] 第 5 章 A review of some results from multivariate analysis / 多元分析结果回顾（PASS：教学覆盖审计通过）
- [x] 第 6 章 The autocovariance and partial covariance of a stationary time series / 平稳时间序列的自协方差与偏协方差（PASS：教学覆盖审计通过）
- [x] 第 7 章 Prediction / 预测（PASS：教学覆盖审计通过）
- [x] 第 8 章 Estimation of the mean and covariance / 均值与协方差估计（PASS：教学覆盖审计通过）
- [x] 第 9 章 Parameter estimation / 参数估计（PASS：教学覆盖审计通过）
- [x] 第 10 章 Spectral Representations / 谱表示（PASS：教学覆盖审计通过）
- [x] 第 11 章 Spectral Analysis / 谱分析（PASS：教学覆盖审计通过）
- [x] 第 12 章 Multivariate time series / 多元时间序列（PASS：教学覆盖审计通过）
- [x] 第 13 章 Nonlinear Time Series Models / 非线性时间序列模型（PASS：教学覆盖审计通过）
- [x] 第 14 章 Consistency and asymptotic normality of estimators / 估计量的一致性与渐近正态性（PASS：教学覆盖审计通过）
- [x] 第 15 章 Residual Bootstrap for estimation in autoregressive processes / 自回归估计中的残差 Bootstrap（PASS：教学覆盖审计通过）
- [x] 附录 A Background / 背景知识（PASS：教学覆盖审计通过）
- [x] 附录 B Mixingales and physical dependence / Mixingales 与物理依赖（PASS：教学覆盖审计通过）

## 精修任务

- [x] 按原 PDF 小节扩展中文讲义，确保教学效果接近英文原文。
- [x] 将每章讲义从“概念地图 + 实践案例”扩展为“章节结构讲义”。
- [ ] 将原文 R 示例逐个转换为 Python 示例，并补充真实数据下载或缓存方案。
- [ ] 对所有章节统一编号、交叉引用、参考文献和术语表。
- [x] 安装或配置 LaTeX 发行版后，批量编译并做版式检查。
- [x] 根据 `translation_pedagogical_audit.md` 继续补强 REVIEW 章节。

## 每章交付标准

- [x] 根据原 PDF 章节内容完成中文主导讲义，保留核心数学符号、定义、定理、例题、注释和练习方向，确保教学效果接近原文。
- [x] 章节结构尽量贴近原文档：章标题、节标题、图表编号、数学推导层级。
- [ ] 每章至少包含 2-4 个 Python 工程实践脚本或脚本中的独立案例。
- [ ] Python 脚本可重复运行，输出图像到本章 `figures/`。
- [x] 图像在 LaTeX 中被引用，并在图后给出中文案例说明。
- [x] 对 R 示例给出对应 Python 实现。
- [x] 完成章节后更新本文件状态。
