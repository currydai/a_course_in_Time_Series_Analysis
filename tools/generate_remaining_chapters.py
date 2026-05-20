"""Generate first-pass chapter folders, LaTeX notes, and local scripts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CHAPTERS = [
    ("ch02", "第02章_Trends_in_a_time_series_时间序列中的趋势.tex", "Trends in a time series", "时间序列中的趋势", "趋势估计、差分、非参数平滑、周期函数和周期检测。", ["参数趋势可用最小二乘估计，但残差相关会影响标准误。", "差分用于削弱低频趋势，使序列更接近平稳。", "移动窗口、筛估计和傅里叶工具把趋势与周期放在统一框架中。"], ["ch02_fig01_parametric_trend.png", "ch02_fig02_differencing.png", "ch02_fig03_periodogram.png"]),
    ("ch03", "第03章_Stationary_Time_Series_平稳时间序列.tex", "Stationary Time Series", "平稳时间序列", "形式化时间序列、样本均值标准误、平稳过程、协方差函数。", ["平稳性要求序列的概率结构不随时间平移而改变。", "弱平稳通常只要求均值常数且协方差只依赖滞后。", "相关性会改变样本均值的方差，这是时间序列推断的基本差异。"], ["ch03_fig01_stationary_vs_random_walk.png", "ch03_fig02_rolling_mean.png"]),
    ("ch04", "第04章_Linear_time_series_线性时间序列.tex", "Linear time series", "线性时间序列", "线性过程、MA、AR、ARMA、单位根、模拟和诊断。", ["AR 模型把当前值表示为过去值和新冲击的组合。", "MA 模型把当前值表示为当前和过去冲击的有限或无限组合。", "ACF/PACF 是识别 AR 与 MA 结构的核心诊断图。"], ["ch04_fig01_arma_series.png", "ch04_fig02_acf_pacf.png"]),
    ("ch05", "第05章_Multivariate_analysis_review_多元分析结果回顾.tex", "A review of some results from multivariate analysis", "多元分析结果回顾", "欧氏空间、投影、线性预测、偏相关和精度矩阵。", ["线性预测可以理解为向由解释变量张成的空间做投影。", "偏相关衡量在控制其他变量后两个变量之间的线性关系。", "精度矩阵的零元素与条件不相关结构密切相关。"], ["ch05_fig01_projection_prediction.png", "ch05_fig02_correlation_matrix.png"]),
    ("ch06", "第06章_Autocovariance_partial_covariance_自协方差与偏协方差.tex", "The autocovariance and partial covariance of a stationary time series", "平稳时间序列的自协方差与偏协方差", "自协方差函数、Yule-Walker 方程、样本 ACF、偏自相关和模型识别。", ["自协方差函数描述同一序列不同滞后之间的线性依赖。", "AR 模型的自协方差满足 Yule-Walker 方程。", "PACF 对 AR 阶数识别特别有用。"], ["ch06_fig01_acf_shapes.png", "ch06_fig02_pacf_shapes.png"]),
    ("ch07", "第07章_Prediction_预测.tex", "Prediction", "预测", "自回归预测、有限过去预测、Durbin-Levinson、Kalman 滤波和非线性预测。", ["预测利用过去信息构造未来观测的条件均值或最佳线性预测。", "AR 模型预测可以递归计算。", "Kalman 滤波把 ARMA 预测放入状态空间框架。"], ["ch07_fig01_ar_forecast.png", "ch07_fig02_forecast_errors.png"]),
    ("ch08", "第08章_Estimation_mean_covariance_均值与协方差估计.tex", "Estimation of the mean and covariance", "均值与协方差估计", "样本均值、样本自协方差、相关性检验、Newey-West 和拟合优度。", ["样本均值在相关序列下仍常用，但标准误不同于 iid 情形。", "样本 ACF 是检测相关结构的基本工具。", "HAC/Newey-West 估计用于处理自相关和异方差下的标准误。"], ["ch08_fig01_sample_mean_dependence.png", "ch08_fig02_sample_acf.png"]),
    ("ch09", "第09章_Parameter_estimation_参数估计.tex", "Parameter estimation", "参数估计", "AR 与 ARMA 参数估计、Yule-Walker、高斯似然、条件似然、Burg 和 Hannan-Rissanen。", ["Yule-Walker 估计把自协方差方程转化为参数估计。", "条件最小二乘适合把 AR 模型写成回归问题。", "最大似然方法给出统一框架，但计算复杂度更高。"], ["ch09_fig01_yule_walker_sampling.png", "ch09_fig02_cls_ar1.png"]),
    ("ch10", "第10章_Spectral_Representations_谱表示.tex", "Spectral Representations", "谱表示", "DFT、近似去相关、谱表示定理、谱密度、ARMA 谱密度和高阶谱。", ["频域视角把协方差结构表示为不同频率上的能量分布。", "DFT 对许多平稳序列具有近似去相关性质。", "ARMA 模型的谱密度由 AR 与 MA 多项式决定。"], ["ch10_fig01_spectral_density.png", "ch10_fig02_dft_energy.png"]),
    ("ch11", "第11章_Spectral_Analysis_谱分析.tex", "Spectral Analysis", "谱分析", "周期图、谱密度估计、Whittle 似然、比率统计和拟合优度检验。", ["周期图是谱密度估计的原始材料，但方差大。", "平滑周期图可降低方差，代价是引入偏差。", "Whittle 似然用频域近似简化高斯似然。"], ["ch11_fig01_smoothed_periodogram.png", "ch11_fig02_two_frequency_signal.png"]),
    ("ch12", "第12章_Multivariate_time_series_多元时间序列.tex", "Multivariate time series", "多元时间序列", "多元序列回归、条件独立、相干性、谱密度矩阵和逆谱密度矩阵。", ["多元时间序列关注多个序列之间的动态相互作用。", "相干性是频域中的相关性度量。", "逆谱密度矩阵用于描述条件依赖结构。"], ["ch12_fig01_var_series.png", "ch12_fig02_coherence.png"]),
    ("ch13", "第13章_Nonlinear_Time_Series_Models_非线性时间序列模型.tex", "Nonlinear Time Series Models", "非线性时间序列模型", "ARCH、GARCH、双线性模型和非参数时间序列模型。", ["金融收益常呈现波动聚集，线性均值模型无法充分解释。", "ARCH/GARCH 通过条件方差建模刻画时变波动率。", "非线性模型的重点通常是条件分布而不只是条件均值。"], ["ch13_fig01_garch_returns.png", "ch13_fig02_conditional_volatility.png"]),
    ("ch14", "第14章_Consistency_asymptotic_normality_一致性与渐近正态性.tex", "Consistency and asymptotic normality of estimators", "估计量的一致性与渐近正态性", "收敛模式、抽样性质、强相合、依概率收敛、渐近正态和 GMLE 性质。", ["一致性说明样本量增大时估计量靠近真值。", "渐近正态性为置信区间和检验提供近似依据。", "时间序列中的依赖条件决定大数定律和中心极限定理能否使用。"], ["ch14_fig01_consistency_mse.png", "ch14_fig02_asymptotic_normality.png"]),
    ("ch15", "第15章_Residual_Bootstrap_残差Bootstrap.tex", "Residual Bootstrap for estimation in autoregressive processes", "自回归估计中的残差 Bootstrap", "残差 Bootstrap 与 AR 参数估计抽样性质。", ["残差 Bootstrap 用拟合模型的残差近似创新分布。", "重抽样后重新生成序列并重新估计参数，可以近似估计量分布。", "该方法依赖模型拟合质量和残差近似独立性。"], ["ch15_fig01_residual_bootstrap.png", "ch15_fig02_residuals.png"]),
    ("appA", "附录A_Background_背景知识.tex", "Background", "背景知识", "不等式、鞅、傅里叶级数、Burkholder 不等式和 FFT。", ["附录 A 提供正文推导所需的概率和分析工具。", "傅里叶级数解释周期函数的频率分解。", "FFT 是频域计算的工程基础。"], ["appA_fig01_fourier_series.png", "appA_fig02_fft_energy.png"]),
    ("appB", "附录B_Mixingales_physical_dependence_Mixingales与物理依赖.tex", "Mixingales and physical dependence", "Mixingales 与物理依赖", "Mixingales、几乎必然收敛速率和物理依赖性质。", ["依赖衰减条件用于证明时间序列估计的渐近性质。", "物理依赖度量关注一个早期冲击对未来过程的影响。", "几何衰减通常比多项式衰减带来更强的理论结果。"], ["appB_fig01_dependence_decay.png", "appB_fig02_physical_dependence.png"]),
]


def tex_body(code: str, en: str, zh: str, scope: str, points: list[str], figs: list[str]) -> str:
    item_points = "\n".join(f"  \\item {p}" for p in points)
    fig_blocks = "\n\n".join(
        f"""\\begin{{figure}}[htbp]
  \\centering
  \\includegraphics[width=0.86\\textwidth]{{{fig}}}
  \\caption{{{zh} Python 实践图：{fig.replace('_', '\\_')}}}
\\end{{figure}}"""
        for fig in figs
    )
    script_name = f"{code}_generate_figures.py"
    return f"""\\documentclass[11pt,a4paper]{{ctexart}}

\\usepackage[margin=2.6cm]{{geometry}}
\\usepackage{{amsmath,amssymb,amsthm}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{listings}}
\\usepackage{{caption}}

\\graphicspath{{{{figures/}}}}
\\hypersetup{{colorlinks=true, linkcolor=blue!50!black, urlcolor=blue!60!black}}
\\lstset{{
  basicstyle=\\ttfamily\\small,
  breaklines=true,
  frame=single,
  columns=fullflexible,
  backgroundcolor=\\color{{gray!7}}
}}

\\title{{{zh} \\\\ \\large {en}}}
\\author{{基于 \\textit{{A Course in Time Series Analysis}} 的中文讲义与 Python 实践}}
\\date{{}}

\\begin{{document}}
\\maketitle

\\section*{{本章定位}}

本章对应原文 \\textit{{{en}}}。首版讲义先按照原文的章节主线整理核心概念、教学解释和 Python 工程实践；后续精修时，可继续把原 PDF 中的证明、练习和细节推导逐节扩展进来。

本章范围：{scope}

\\section{{核心知识点}}

\\begin{{itemize}}
{item_points}
\\end{{itemize}}

\\section{{教学说明}}

学习本章时，建议先区分三个层次：第一，模型或概念试图刻画哪一种时间序列现象；第二，对应的数学对象是什么，例如均值函数、自协方差函数、谱密度或条件方差；第三，在 Python 中如何通过仿真、估计和图形诊断把抽象概念落到可观察对象上。

对于原文中的 R 代码，本项目统一改写为 Python。常用工具包括 \\texttt{{numpy}}、\\texttt{{pandas}}、\\texttt{{matplotlib}}、\\texttt{{scipy}} 和 \\texttt{{statsmodels}}。这些库覆盖了数据组织、数值计算、图形生成、频域分析、ARMA 仿真和 ACF/PACF 诊断。

\\section{{Python 工程实践}}

在本章目录下运行：

\\begin{{lstlisting}}[language=bash]
python scripts/{script_name}
\\end{{lstlisting}}

脚本会把图像写入本章 \\texttt{{figures/}} 目录。图像既可用于教学解释，也可作为后续扩充案例的基础。

{fig_blocks}

\\section{{本章小结}}

本章首版的重点是建立概念地图和可运行实践。后续精修建议按原文小节逐段扩展：先补齐定义和定理，再补证明思路，最后增加练习题解析和真实数据案例。

\\end{{document}}
"""


def script_body(code: str) -> str:
    return f'''"""Generate figures for {code}."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.chapter_practice_figures import generate_chapter_figures


if __name__ == "__main__":
    generate_chapter_figures("{code}", Path(__file__).resolve())
'''


def main() -> None:
    for code, tex_name, en, zh, scope, points, figs in CHAPTERS:
        chapter_dir = ROOT / "chapters" / f"{code}_{en.lower().replace(' ', '_').replace('/', '_').replace(',', '').replace('(', '').replace(')', '')[:44]}"
        if code.startswith("app"):
            chapter_dir = ROOT / "chapters" / f"{code}_{en.lower().replace(' ', '_')}"
        (chapter_dir / "figures").mkdir(parents=True, exist_ok=True)
        (chapter_dir / "scripts").mkdir(parents=True, exist_ok=True)
        (chapter_dir / tex_name).write_text(tex_body(code, en, zh, scope, points, figs), encoding="utf-8")
        (chapter_dir / "scripts" / f"{code}_generate_figures.py").write_text(script_body(code), encoding="utf-8")
        print(chapter_dir)


if __name__ == "__main__":
    main()

