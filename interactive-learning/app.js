const TAU = Math.PI * 2;

const chapters = [
  {
    id: "ch01",
    number: "01",
    title: "Introduction / 导论",
    topic: "时间序列、滤波与数据生成机制",
    concepts: ["白噪声", "移动平均滤波", "信号与噪声", "样本路径"],
    formula: "X_t = signal_t + noise_t,    \\bar X_t = m^{-1}\\sum_{j=0}^{m-1} X_{t-j}",
    demos: [
      {
        name: "噪声、信号与滤波",
        kind: "filter",
        a: ["周期长度", 18, 60, 32, 1],
        b: ["滤波窗口", 3, 35, 11, 1],
        note: "拖动滤波窗口，观察短期波动怎样被压低；再增大扰动强度，体会为什么时间序列分析总是在模型结构和随机波动之间来回权衡。",
      },
    ],
  },
  {
    id: "ch02",
    number: "02",
    title: "Trends in a time series / 时间序列中的趋势",
    topic: "趋势估计、差分与周期图",
    concepts: ["确定性趋势", "随机趋势", "差分", "周期图"],
    formula: "X_t = m_t + Y_t,    \\Delta X_t = X_t - X_{t-1}",
    demos: [
      {
        name: "趋势拟合与差分",
        kind: "trend",
        a: ["趋势弯曲度", -1, 1, 0.35, 0.01],
        b: ["季节幅度", 0, 1.4, 0.55, 0.01],
        note: "当趋势弯曲度较高时，简单线性拟合会留下系统残差；切换样本长度和噪声后，观察差分如何把低频趋势转为局部变化。",
      },
    ],
  },
  {
    id: "ch03",
    number: "03",
    title: "Stationary Time Series / 平稳时间序列",
    topic: "平稳性、自协方差与随机游走",
    concepts: ["严格平稳", "弱平稳", "随机游走", "滚动均值"],
    formula: "E(X_t)=\\mu,    Cov(X_t, X_{t+h})=\\gamma(h)",
    demos: [
      {
        name: "平稳过程与随机游走",
        kind: "stationarity",
        a: ["AR 系数", 0, 1.02, 0.72, 0.01],
        b: ["局部均值窗口", 5, 65, 25, 1],
        note: "把 AR 系数推近 1，序列会变得像随机游走一样拖着长期记忆；滚动均值不再稳定地围绕一个水平震荡。",
      },
    ],
  },
  {
    id: "ch04",
    number: "04",
    title: "Linear time series / 线性时间序列",
    topic: "ARMA、因果性与自相关形状",
    concepts: ["AR(1)", "MA(1)", "因果表示", "ACF 衰减"],
    formula: "X_t = \\phi X_{t-1} + Z_t,    X_t = Z_t + \\theta Z_{t-1}",
    demos: [
      {
        name: "AR 与 MA 的记忆形状",
        kind: "arma",
        a: ["AR 系数 φ", -0.95, 0.95, 0.62, 0.01],
        b: ["MA 系数 θ", -0.95, 0.95, 0.35, 0.01],
        note: "AR 系数控制长尾衰减，MA 系数主要改变短滞后相关。看右侧 ACF 的形状，比只看样本路径更容易识别模型家族。",
      },
    ],
  },
  {
    id: "ch05",
    number: "05",
    title: "Multivariate analysis review / 多元分析回顾",
    topic: "投影、协方差矩阵与最小二乘",
    concepts: ["线性投影", "协方差矩阵", "正交误差", "条件均值"],
    formula: "\\hat Y = \\alpha + \\beta X,    \\beta = Cov(X,Y)/Var(X)",
    demos: [
      {
        name: "投影与预测误差",
        kind: "projection",
        a: ["相关系数 ρ", -0.95, 0.95, 0.72, 0.01],
        b: ["斜率缩放", 0.2, 1.8, 1, 0.01],
        note: "相关系数越高，点云越贴近一条线；最小二乘投影的残差方向会与解释变量近似正交。",
      },
    ],
  },
  {
    id: "ch06",
    number: "06",
    title: "Autocovariance and partial covariance / 自协方差与偏协方差",
    topic: "ACF、PACF 与模型识别",
    concepts: ["自协方差", "自相关", "偏自相关", "截尾与拖尾"],
    formula: "\\rho(h)=\\gamma(h)/\\gamma(0),    \\phi_{hh}=Corr(X_t, X_{t-h}\\mid X_{t-1},...,X_{t-h+1})",
    demos: [
      {
        name: "ACF/PACF 识别",
        kind: "acf",
        a: ["AR 强度", -0.9, 0.9, 0.68, 0.01],
        b: ["二阶扰动", -0.55, 0.55, -0.18, 0.01],
        note: "右侧同时画 ACF 和 PACF。AR 型过程常见 ACF 拖尾、PACF 较快截尾，这是模型识别的第一张草图。",
      },
    ],
  },
  {
    id: "ch07",
    number: "07",
    title: "Prediction / 预测",
    topic: "最佳线性预测与预测误差",
    concepts: ["一步预测", "多步预测", "预测区间", "创新"],
    formula: "\\hat X_{n+h}=E(X_{n+h}\\mid X_n,X_{n-1},...),    e_{n+h}=X_{n+h}-\\hat X_{n+h}",
    demos: [
      {
        name: "AR 预测路径",
        kind: "forecast",
        a: ["持续性 φ", 0, 0.98, 0.74, 0.01],
        b: ["预测步数", 4, 40, 18, 1],
        note: "持续性越高，预测均值回归越慢；预测步数越远，不确定性区间越宽，这正是预测问题的基本代价。",
      },
    ],
  },
  {
    id: "ch08",
    number: "08",
    title: "Estimation of mean and covariance / 均值与协方差估计",
    topic: "样本均值、样本自协方差与依赖样本",
    concepts: ["样本均值", "样本 ACF", "估计方差", "有效样本量"],
    formula: "\\bar X_n=n^{-1}\\sum_{t=1}^n X_t,    \\hat\\gamma(h)=n^{-1}\\sum_{t=1}^{n-h}(X_t-\\bar X)(X_{t+h}-\\bar X)",
    demos: [
      {
        name: "依赖样本下的均值估计",
        kind: "mean",
        a: ["依赖强度", 0, 0.96, 0.62, 0.01],
        b: ["重复实验数", 20, 220, 90, 1],
        note: "依赖越强，均值估计收敛越慢。即使样本长度相同，强相关序列提供的有效信息也会少很多。",
      },
    ],
  },
  {
    id: "ch09",
    number: "09",
    title: "Parameter estimation / 参数估计",
    topic: "Yule-Walker、CLS 与似然轮廓",
    concepts: ["参数估计", "条件最小二乘", "似然曲线", "抽样波动"],
    formula: "\\hat\\phi_{YW}=\\hat\\gamma(1)/\\hat\\gamma(0),    \\min_\\phi\\sum_t (X_t-\\phi X_{t-1})^2",
    demos: [
      {
        name: "AR(1) 参数轮廓",
        kind: "likelihood",
        a: ["真实 φ", -0.9, 0.9, 0.55, 0.01],
        b: ["候选平滑", 0, 1, 0.35, 0.01],
        note: "右侧是条件平方和的轮廓。样本越短、噪声越大，最小点越容易偏离真实参数。",
      },
    ],
  },
  {
    id: "ch10",
    number: "10",
    title: "Spectral Representations / 谱表示",
    topic: "傅里叶绕线、谱密度与频率分解",
    concepts: ["傅里叶基", "谱密度", "频率峰", "能量分解"],
    formula: "X_t = \\int_{-\\pi}^{\\pi} e^{it\\lambda}\\,dZ(\\lambda),    f(\\lambda)=\\sum_h \\gamma(h)e^{-ih\\lambda}/(2\\pi)",
    demos: [
      {
        name: "傅里叶频率识别",
        kind: "fourier",
        a: ["试探频率", 0.2, 8, 3, 0.01],
        b: ["第二频率", 0.5, 8, 5, 0.01],
        note: "这延续之前的傅里叶演示：当试探频率接近真实成分时，绕线质心偏离原点，频谱峰值抬升。",
      },
    ],
  },
  {
    id: "ch11",
    number: "11",
    title: "Spectral Analysis / 谱分析",
    topic: "周期图、窗口平滑与泄漏",
    concepts: ["周期图", "谱窗", "平滑", "频率泄漏"],
    formula: "I_n(\\lambda)=\\left|\\sum_{t=1}^n X_t e^{-it\\lambda}\\right|^2/(2\\pi n)",
    demos: [
      {
        name: "周期图和平滑谱",
        kind: "periodogram",
        a: ["主频率", 0.5, 8, 3.3, 0.01],
        b: ["平滑带宽", 1, 32, 8, 1],
        note: "非整数周期会出现谱泄漏；增大平滑带宽能降低尖锐波动，但也会牺牲分辨率。",
      },
    ],
  },
  {
    id: "ch12",
    number: "12",
    title: "Multivariate time series / 多元时间序列",
    topic: "VAR、交叉相关与共同波动",
    concepts: ["VAR(1)", "交叉相关", "相干性", "脉冲响应"],
    formula: "X_t = A X_{t-1}+Z_t,    Corr(X_t,Y_{t-h})",
    demos: [
      {
        name: "VAR 共同波动",
        kind: "var",
        a: ["交叉影响", -0.75, 0.75, 0.42, 0.01],
        b: ["自身持续性", 0, 0.94, 0.58, 0.01],
        note: "交叉影响决定两个变量如何互相牵引；右侧的散点和滞后相关展示多元序列中方向性信息的线索。",
      },
    ],
  },
  {
    id: "ch13",
    number: "13",
    title: "Nonlinear Time Series Models / 非线性时间序列模型",
    topic: "条件异方差、阈值与波动聚集",
    concepts: ["ARCH", "GARCH", "波动聚集", "条件方差"],
    formula: "X_t=\\sigma_t Z_t,    \\sigma_t^2=\\alpha_0+\\alpha_1 X_{t-1}^2+\\beta_1\\sigma_{t-1}^2",
    demos: [
      {
        name: "GARCH 波动聚集",
        kind: "garch",
        a: ["冲击反馈 α", 0.02, 0.35, 0.14, 0.01],
        b: ["波动持续 β", 0.1, 0.94, 0.76, 0.01],
        note: "收益本身可能均值接近零，但条件方差会成团出现。把 β 推高，波动团块会持续更久。",
      },
    ],
  },
  {
    id: "ch14",
    number: "14",
    title: "Consistency and asymptotic normality / 一致性与渐近正态性",
    topic: "大样本极限、MSE 与正态近似",
    concepts: ["一致性", "渐近正态", "均方误差", "样本量效应"],
    formula: "\\hat\\theta_n \\to_p \\theta,    \\sqrt n(\\hat\\theta_n-\\theta)\\Rightarrow N(0,V)",
    demos: [
      {
        name: "估计量抽样分布",
        kind: "asymptotic",
        a: ["偏差强度", -0.4, 0.4, 0.08, 0.01],
        b: ["尾部厚度", 0, 1, 0.28, 0.01],
        note: "增加样本长度后，抽样分布收缩；如果存在偏差或厚尾，正态近似需要更多样本才会显得可靠。",
      },
    ],
  },
  {
    id: "ch15",
    number: "15",
    title: "Residual Bootstrap / 残差 Bootstrap",
    topic: "重抽样、经验分布与区间估计",
    concepts: ["残差重抽样", "Bootstrap 分布", "置信区间", "AR 估计"],
    formula: "X_t^* = \\hat\\phi X_{t-1}^* + e_t^*,    e_t^* \\sim \\hat F_e",
    demos: [
      {
        name: "残差 Bootstrap 区间",
        kind: "bootstrap",
        a: ["真实 φ", 0.05, 0.95, 0.62, 0.01],
        b: ["重抽样次数", 40, 360, 160, 10],
        note: "Bootstrap 分布围绕原样本估计量展开。样本越短或 φ 越靠近 1，区间往往越宽。",
      },
    ],
  },
  {
    id: "appA",
    number: "A",
    title: "Background / 背景知识",
    topic: "Fourier、矩阵与概率工具",
    concepts: ["正交基", "DFT", "投影", "Parseval 恒等式"],
    formula: "\\sum_t |x_t|^2 = n^{-1}\\sum_k |d_k|^2",
    demos: [
      {
        name: "Fourier 基函数叠加",
        kind: "basis",
        a: ["基函数个数", 1, 14, 5, 1],
        b: ["高频权重", 0, 1.4, 0.45, 0.01],
        note: "逐步增加基函数个数，观察简单波形如何由一组正交振荡拼出。这是频域方法背后的几何直觉。",
      },
    ],
  },
  {
    id: "appB",
    number: "B",
    title: "Mixingales and physical dependence / Mixingales 与物理依赖",
    topic: "依赖衰减与物理依赖度量",
    concepts: ["mixingale", "physical dependence", "耦合", "依赖衰减"],
    formula: "\\delta_q(k)=\\|X_k-X_k'\\|_q,    \\delta_q(k)\\downarrow 0",
    demos: [
      {
        name: "依赖强度衰减",
        kind: "dependence",
        a: ["衰减速度", 0.02, 0.8, 0.22, 0.01],
        b: ["初始冲击", 0.2, 1.8, 1, 0.01],
        note: "物理依赖度量关心一个早期扰动对未来还剩多少影响。衰减越快，极限定理通常越容易成立。",
      },
    ],
  },
];

const chapterEnrichment = {
  ch01: {
    intuition: "时间序列不是一列孤立数字，而是按时间组织的随机机制痕迹。导论章要先训练学生把趋势、周期、噪声和滤波结果区分开。",
    steps: ["先把扰动强度调到 0，识别纯信号的周期。", "逐步增加噪声，观察原始曲线何时难以肉眼判断结构。", "扩大滤波窗口，比较平滑后的滞后和细节损失。"],
    undergraduate: ["能解释样本路径、白噪声、滤波和平滑的基本含义。", "能说明为什么同一模型每次模拟会得到不同曲线。"],
    graduate: ["思考可观测序列和潜在生成机制之间的区别。", "把滤波看成线性算子，讨论它对频率成分和方差的影响。"],
    pitfalls: ["不要把平滑后的曲线当成真实信号本身。", "不要用一条样本路径直接判断总体性质。"],
    discussion: "让学生找一个真实时间序列，标出可能的信号、噪声、异常值和采样频率，再说明这些判断依赖哪些先验知识。",
  },
  ch02: {
    intuition: "趋势处理回答的是：序列的长期移动是结构的一部分，还是应该先剥离后再建模？差分、拟合和周期图分别从不同角度处理低频变化。",
    steps: ["调高趋势弯曲度，看线性拟合残差如何出现系统形状。", "增加季节幅度，观察差分后周期成分是否仍然可见。", "改变样本长度，比较短样本中趋势和周期的混淆。"],
    undergraduate: ["能区分确定性趋势、随机趋势和季节波动。", "能解释一阶差分为什么会压低低频趋势。"],
    graduate: ["讨论去趋势步骤对后续估计量分布的影响。", "比较回归去趋势和差分在单位根情形下的适用边界。"],
    pitfalls: ["不要看到上升曲线就直接判定非平稳，有限样本也会制造假趋势。", "过度差分会把可预测结构变成负相关噪声。"],
    discussion: "给出同一序列的回归去趋势和差分结果，让学生判断哪一个更适合预测，哪一个更适合解释。",
  },
  ch03: {
    intuition: "平稳性是时间序列课程的地基：如果均值、方差和协方差结构不随时间漂移，过去才更有资格帮助我们理解未来。",
    steps: ["把 AR 系数从 0.3 推到 0.95，观察样本路径的记忆变长。", "把系数推近 1，比较滚动均值是否还稳定。", "调大局部均值窗口，区分短期波动和长期漂移。"],
    undergraduate: ["能说明弱平稳的均值和协方差条件。", "能用随机游走解释非平稳样本路径的典型外观。"],
    graduate: ["讨论严格平稳与二阶平稳的关系和差异。", "把接近单位根的过程作为局部到统一渐近理论的入口。"],
    pitfalls: ["不要把样本均值看起来稳定等同于过程平稳。", "不要忽略初始值和有限样本对图形的影响。"],
    discussion: "让学生比较 AR(0.7)、AR(0.98) 和随机游走在预测、估计均值、构造置信区间时的差异。",
  },
  ch04: {
    intuition: "线性时间序列模型把当前值写成过去冲击的线性组合。AR 更像记忆递推，MA 更像有限冲击回声。",
    steps: ["先只调 AR 系数，看 ACF 拖尾速度如何改变。", "再调 MA 系数，观察短滞后相关如何被改写。", "把参数设为负数，注意样本路径和 ACF 的交替振荡。"],
    undergraduate: ["能读懂 AR(1)、MA(1)、ARMA 的基本方程。", "能用 ACF 形状初步区分 AR 与 MA。"],
    graduate: ["讨论因果性、可逆性和根在单位圆外的条件。", "把 Wold 分解作为线性预测和谱表示的桥梁。"],
    pitfalls: ["不要只凭样本路径判断 AR 或 MA，必须看相关结构。", "参数接近边界时，常规直觉和估计表现都会变差。"],
    discussion: "让学生用同一 ACF 图反推可能模型，并解释为什么多个模型可能产生相似的有限样本图像。",
  },
  ch05: {
    intuition: "多元分析回顾把预测解释成投影：最好的线性预测不是玄学，而是在信息空间里找一个最近点。",
    steps: ["改变相关系数，观察点云从圆形变成细长椭圆。", "改变斜率缩放，比较错误斜率产生的残差结构。", "看残差是否还与解释变量同步移动。"],
    undergraduate: ["能解释协方差、相关和最小二乘投影的关系。", "能理解正交误差条件的几何意义。"],
    graduate: ["把线性投影推广到 Hilbert 空间中的闭子空间投影。", "讨论条件期望和最佳线性预测之间的区别。"],
    pitfalls: ["相关不等于因果，投影系数也不自动代表结构参数。", "斜率正确不代表模型完整，残差还可能有时间依赖。"],
    discussion: "让学生说明为什么时间序列预测理论大量使用投影语言，而不是只使用普通回归语言。",
  },
  ch06: {
    intuition: "ACF 告诉我们隔 h 期仍保留多少线性记忆，PACF 则问：扣除中间滞后后，还剩多少直接关系。",
    steps: ["调节 AR 强度，观察 ACF 的拖尾。", "加入二阶扰动，观察 PACF 的前几个滞后。", "改变样本长度，体会样本 ACF 的不稳定性。"],
    undergraduate: ["能计算并解释样本 ACF 的滞后含义。", "能用 ACF/PACF 作为 ARMA 模型识别的初步工具。"],
    graduate: ["理解偏自相关与 Durbin-Levinson 递推之间的关系。", "讨论样本 ACF 在依赖样本下的渐近协方差。"],
    pitfalls: ["不要把每一个小峰都解释成真实结构。", "PACF 截尾是理想模型信号，有限样本会有噪声波动。"],
    discussion: "给学生一组 ACF/PACF 图，让他们提出多个候选模型并设计下一步检验。",
  },
  ch07: {
    intuition: "预测的核心不是把未来画准，而是在当前信息下给出最合理的条件均值和诚实的不确定性。",
    steps: ["增大持续性，观察预测均值回归速度变慢。", "增加预测步数，观察区间扩张。", "增大噪声，比较短期和长期预测受影响的程度。"],
    undergraduate: ["能解释一步预测、多步预测和预测误差。", "能读懂预测区间随步长扩大的现象。"],
    graduate: ["把最佳线性预测写成投影问题。", "讨论创新算法、Kalman 滤波和状态空间表示的联系。"],
    pitfalls: ["预测均值不是未来真实路径。", "区间越窄不一定越好，可能只是低估了不确定性。"],
    discussion: "让学生分别为销售、气温和金融收益设计预测目标，比较预测均值和预测分布哪个更重要。",
  },
  ch08: {
    intuition: "依赖样本会让信息增长变慢。样本数 n 看起来很大，但有效样本量可能小得多。",
    steps: ["提高依赖强度，观察均值抽样分布变宽。", "增加重复实验数，看经验分布是否稳定。", "调大样本长度，比较独立与强相关下收敛速度。"],
    undergraduate: ["能写出样本均值和样本自协方差。", "能解释相关性为什么影响标准误。"],
    graduate: ["理解长程方差和 HAC 估计的必要性。", "讨论混合条件如何保证样本矩的一致性。"],
    pitfalls: ["不要把独立样本标准误直接套到强相关序列。", "样本 ACF 的偏差和截断选择会影响后续推断。"],
    discussion: "让学生比较 iid 均值估计和 AR(1) 均值估计的标准误公式，并解释差异来源。",
  },
  ch09: {
    intuition: "参数估计是在候选模型之间寻找最能解释数据的参数。目标函数越平坦，估计越不稳定。",
    steps: ["改变真实参数，观察目标函数最小点移动。", "增加噪声或减少样本长度，观察轮廓变平。", "比较 Yule-Walker 和条件最小二乘的直觉差异。"],
    undergraduate: ["能理解 Yule-Walker 和条件最小二乘的估计思路。", "能从目标函数图读出估计值和不确定性。"],
    graduate: ["讨论一致性、渐近正态性和信息矩阵。", "比较条件似然、精确似然和矩估计的假设差异。"],
    pitfalls: ["目标函数最小点不等于真实参数，只是样本给出的估计。", "边界附近的参数会让标准渐近近似变脆弱。"],
    discussion: "让学生说明在短样本、高持续性序列中，为什么不同估计方法会给出明显不同的结果。",
  },
  ch10: {
    intuition: "谱表示把时间序列拆成不同频率的振荡能量。傅里叶绕线让频率匹配变成肉眼可见的质心偏移。",
    steps: ["把试探频率调到真实频率附近，观察绕线质心远离原点。", "移动第二频率，观察频谱中两个峰的分离。", "增大噪声，比较频域峰值的稳健性。"],
    undergraduate: ["能把周期、频率和谱峰联系起来。", "能解释为什么傅里叶基可以检测隐藏周期。"],
    graduate: ["理解谱密度是自协方差函数的 Fourier 变换。", "讨论正交增量过程和 Cramer 表示的意义。"],
    pitfalls: ["频谱峰不一定代表因果周期，也可能是采样和窗口造成的。", "不要混淆角频率、普通频率和离散 Fourier 频率。"],
    discussion: "让学生解释同一个周期结构为什么在时域图中不明显，却能在频域中突出出来。",
  },
  ch11: {
    intuition: "周期图是谱密度的粗糙估计。平滑能降低方差，但会模糊相近频率。",
    steps: ["设置非整数主频率，观察泄漏。", "增大平滑带宽，观察曲线变稳但峰变宽。", "改变样本长度，比较频率分辨率。"],
    undergraduate: ["能解释周期图和平滑周期图。", "能说明频率泄漏和窗口选择的影响。"],
    graduate: ["讨论周期图不一致和谱窗估计的一致性条件。", "理解带宽选择中的偏差-方差权衡。"],
    pitfalls: ["不要把原始周期图的尖峰全部当成真实周期。", "平滑过度会把相邻峰合并。"],
    discussion: "让学生为两个相近频率的信号选择样本长度和平滑带宽，并说明取舍。",
  },
  ch12: {
    intuition: "多元时间序列关心变量之间的动态牵引：不是只看同一时点相关，而是看谁领先、谁响应。",
    steps: ["调节交叉影响，观察两个变量相图的倾斜。", "提高自身持续性，观察滞后相关延长。", "比较同向和反向交叉影响下的路径形状。"],
    undergraduate: ["能读懂 VAR(1) 方程和交叉相关。", "能解释多变量预测为什么需要滞后信息。"],
    graduate: ["讨论稳定性条件、特征根和脉冲响应。", "把 VAR 与 Granger 因果和谱相干联系起来。"],
    pitfalls: ["交叉相关不等于结构因果。", "变量尺度不同会影响直观图像和估计稳定性。"],
    discussion: "让学生设计一个宏观经济 VAR 小实验，说明变量排序和滞后阶数为什么重要。",
  },
  ch13: {
    intuition: "非线性模型提醒我们：均值可能简单，方差却会随时间改变。金融收益的波动聚集就是典型例子。",
    steps: ["调高冲击反馈，观察大波动后方差跳升。", "调高波动持续性，观察波动团块延长。", "比较收益曲线和条件方差曲线，区分均值与波动。"],
    undergraduate: ["能解释条件异方差和波动聚集。", "能读懂 ARCH/GARCH 方程的参数作用。"],
    graduate: ["讨论平稳性、矩存在条件和准最大似然估计。", "把非线性条件方差与风险度量联系起来。"],
    pitfalls: ["不要只看收益均值来判断模型是否有结构。", "GARCH 参数和无条件方差之间有约束关系。"],
    discussion: "让学生比较 ARMA 均值模型与 GARCH 方差模型分别解决什么问题。",
  },
  ch14: {
    intuition: "渐近理论解释为什么大样本下估计量会稳定，并给推断提供近似分布。但它不是免检通行证。",
    steps: ["增加样本长度，观察抽样分布收缩。", "加入偏差，观察分布中心是否仍对准真值。", "加重尾部，观察正态近似变慢。"],
    undergraduate: ["能区分一致性和无偏性。", "能解释根号 n 收敛和近似正态的图形含义。"],
    graduate: ["理解依赖数据下中心极限定理需要的条件。", "讨论 sandwich 方差、长程方差和极限分布的稳健估计。"],
    pitfalls: ["样本大不代表模型假设正确。", "渐近正态不能自动修复偏差和厚尾。"],
    discussion: "让学生给出一个一致但有偏的估计例子，再说明为什么它仍可能用于大样本推断。",
  },
  ch15: {
    intuition: "Bootstrap 用样本自己的残差近似未知误差分布。它把一次数据变成许多次仿真实验，用来评估估计波动。",
    steps: ["改变真实 φ，观察区间宽度随持续性变化。", "增加重抽样次数，观察 Bootstrap 分布是否更稳定。", "增大噪声，比较区间中心和宽度。"],
    undergraduate: ["能说明残差 Bootstrap 的基本流程。", "能解释 Bootstrap 分布和置信区间的关系。"],
    graduate: ["讨论时间序列 Bootstrap 为什么不能简单打乱原序列。", "理解残差中心化、初始值和依赖结构保留的重要性。"],
    pitfalls: ["不要把原始观测值随意重排来模拟时间序列。", "Bootstrap 不能弥补模型设定错误。"],
    discussion: "让学生比较残差 Bootstrap、块 Bootstrap 和参数 Bootstrap 的适用场景。",
  },
  appA: {
    intuition: "附录 A 提供频域、矩阵和概率工具。它的目标是把后续章节中反复出现的数学对象变得熟悉。",
    steps: ["增加基函数个数，观察重构曲线变复杂。", "调节高频权重，观察局部振荡如何增强。", "比较时域能量和频域能量的对应。"],
    undergraduate: ["能解释正交基和 Fourier 展开的基本想法。", "能把向量投影和最小二乘联系起来。"],
    graduate: ["从 Hilbert 空间角度理解投影、闭包和正交分解。", "把 Parseval 恒等式作为谱分析能量守恒的基础。"],
    pitfalls: ["不要把数学工具当成孤立附录，它们会在预测和谱分析中反复出现。", "基函数越多不一定越能解释，可能只是拟合细节。"],
    discussion: "让学生用投影语言重新解释最小二乘、最佳线性预测和 Fourier 分解。",
  },
  appB: {
    intuition: "附录 B 处理依赖衰减。很多极限定理并不要求独立，但要求远距离冲击的影响足够快地消失。",
    steps: ["增大衰减速度，观察早期冲击更快消失。", "增大初始冲击，比较影响规模和影响持续时间。", "把曲线与平稳、CLT 和估计一致性联系起来。"],
    undergraduate: ["能直观说明依赖衰减为什么重要。", "能区分短程依赖和长期持续影响。"],
    graduate: ["理解 physical dependence measure 的耦合思想。", "讨论 mixingale 条件如何支撑样本矩和估计量的极限理论。"],
    pitfalls: ["弱依赖不是没有依赖，而是远期影响可控。", "依赖衰减速度会改变可用的极限定理。"],
    discussion: "让学生为一个非线性过程构造“替换一个早期冲击”的思想实验，解释未来影响如何衡量。",
  },
};

const demoExtensions = {
  ch01: [
    { name: "移动平均的滞后代价", kind: "filter", a: ["周期长度", 12, 70, 24, 1], b: ["滤波窗口", 3, 55, 27, 1], note: "把滤波窗口调大，曲线会更平滑，但峰谷会被推迟或削弱。这个演示适合讨论平滑和实时监测之间的取舍。" },
    { name: "弱信号的可见性", kind: "filter", a: ["周期长度", 18, 80, 48, 1], b: ["滤波窗口", 3, 45, 9, 1], note: "先提高扰动强度，再逐步增加样本长度，观察弱周期什么时候开始从噪声中显露出来。" },
  ],
  ch02: [
    { name: "确定性趋势残差", kind: "trend", a: ["趋势弯曲度", -1, 1, -0.55, 0.01], b: ["季节幅度", 0, 1.4, 0.25, 0.01], note: "用较强弯曲趋势制造系统残差，让学生看到错误趋势形式会把结构留在残差里。" },
    { name: "季节项与差分", kind: "trend", a: ["趋势弯曲度", -0.5, 0.5, 0.12, 0.01], b: ["季节幅度", 0, 1.8, 1.15, 0.01], note: "增强季节幅度后，差分不会自动消灭所有周期结构；它只是改变低频和局部变化的表达方式。" },
  ],
  ch03: [
    { name: "近单位根过渡", kind: "stationarity", a: ["AR 系数", 0.75, 1.02, 0.96, 0.01], b: ["局部均值窗口", 5, 85, 35, 1], note: "参数接近 1 时，短样本看起来可能像有趋势。这个演示适合引出单位根和局部到统一渐近。" },
    { name: "滚动方差稳定性", kind: "stationarity", a: ["AR 系数", 0, 0.95, 0.42, 0.01], b: ["局部均值窗口", 5, 75, 45, 1], note: "比较滚动均值和滚动方差，帮助学生把均值平稳和二阶平稳分开理解。" },
  ],
  ch04: [
    { name: "负相关的交替振荡", kind: "arma", a: ["AR 系数 φ", -0.95, 0.2, -0.72, 0.01], b: ["MA 系数 θ", -0.95, 0.95, 0.1, 0.01], note: "负 AR 系数会带来正负交替的相关形状，适合训练学生从 ACF 读出振荡记忆。" },
    { name: "短记忆 MA 冲击", kind: "arma", a: ["AR 系数 φ", -0.2, 0.2, 0, 0.01], b: ["MA 系数 θ", -0.95, 0.95, 0.8, 0.01], note: "弱化 AR、强化 MA，观察相关结构如何集中在短滞后，这正是 MA 模型的识别线索。" },
  ],
  ch05: [
    { name: "低相关投影失败", kind: "projection", a: ["相关系数 ρ", -0.4, 0.4, 0.18, 0.01], b: ["斜率缩放", 0.2, 1.8, 1, 0.01], note: "当相关性很弱时，线性投影解释力有限。这个演示适合区分数学上最优和实际上有用。" },
    { name: "错误斜率残差", kind: "projection", a: ["相关系数 ρ", 0.35, 0.95, 0.82, 0.01], b: ["斜率缩放", 0.2, 1.8, 1.55, 0.01], note: "故意偏离正确斜率，观察残差里还残留解释变量方向的信息。" },
  ],
  ch06: [
    { name: "二阶记忆的指纹", kind: "acf", a: ["AR 强度", -0.9, 0.9, 0.35, 0.01], b: ["二阶扰动", -0.55, 0.55, 0.42, 0.01], note: "增加二阶扰动后，ACF/PACF 前几个滞后的形状会改变，适合讨论 AR 阶数识别。" },
    { name: "负相关 PACF", kind: "acf", a: ["AR 强度", -0.9, 0.1, -0.62, 0.01], b: ["二阶扰动", -0.35, 0.35, 0.08, 0.01], note: "负相关过程的 ACF 会出现交替符号，能帮助学生避免只记正相关情形。" },
  ],
  ch07: [
    { name: "短期预测优势", kind: "forecast", a: ["持续性 φ", 0, 0.98, 0.35, 0.01], b: ["预测步数", 4, 40, 8, 1], note: "低持续性序列只有短期预测较有意义，远期预测很快回到长期均值附近。" },
    { name: "高持续性长期风险", kind: "forecast", a: ["持续性 φ", 0.55, 0.99, 0.93, 0.01], b: ["预测步数", 8, 60, 36, 1], note: "高持续性让预测均值回归缓慢，也让不确定性在多步预测中更显著。" },
  ],
  ch08: [
    { name: "有效样本量下降", kind: "mean", a: ["依赖强度", 0.5, 0.98, 0.88, 0.01], b: ["重复实验数", 40, 260, 150, 1], note: "强相关时，样本均值的抽样分布明显更宽，适合引出有效样本量和长程方差。" },
    { name: "弱依赖基准", kind: "mean", a: ["依赖强度", 0, 0.45, 0.18, 0.01], b: ["重复实验数", 40, 260, 120, 1], note: "把弱依赖作为基准，再切回强依赖，学生会更直观看到标准误膨胀。" },
  ],
  ch09: [
    { name: "平坦目标函数", kind: "likelihood", a: ["真实 φ", -0.2, 0.9, 0.82, 0.01], b: ["候选平滑", 0, 1, 0.75, 0.01], note: "目标函数越平坦，参数估计越容易被样本扰动推开，适合讨论识别强弱。" },
    { name: "负参数估计", kind: "likelihood", a: ["真实 φ", -0.9, 0.2, -0.58, 0.01], b: ["候选平滑", 0, 1, 0.28, 0.01], note: "负参数情形可展示目标函数最小点和样本路径振荡之间的对应。" },
  ],
  ch10: [
    { name: "双频率分离", kind: "fourier", a: ["试探频率", 0.2, 8, 2, 0.01], b: ["第二频率", 0.5, 8, 6.2, 0.01], note: "两个频率相距较远时，谱峰更容易分开，适合作为频率分辨率的入门例子。" },
    { name: "近频率混叠", kind: "fourier", a: ["试探频率", 0.2, 8, 3.2, 0.01], b: ["第二频率", 0.5, 8, 3.9, 0.01], note: "相近频率会让峰值分辨更困难，可自然过渡到样本长度和谱分析窗口。" },
  ],
  ch11: [
    { name: "窄带平滑", kind: "periodogram", a: ["主频率", 0.5, 8, 2.7, 0.01], b: ["平滑带宽", 1, 32, 3, 1], note: "窄带平滑保留分辨率，但周期图仍然抖动明显。" },
    { name: "宽带平滑", kind: "periodogram", a: ["主频率", 0.5, 8, 2.7, 0.01], b: ["平滑带宽", 1, 32, 22, 1], note: "宽带平滑降低方差，但也会牺牲峰的尖锐度，适合讨论偏差-方差权衡。" },
  ],
  ch12: [
    { name: "正向交叉牵引", kind: "var", a: ["交叉影响", 0, 0.75, 0.55, 0.01], b: ["自身持续性", 0, 0.94, 0.5, 0.01], note: "正交叉影响会让两个变量同向牵引，右侧相图更容易形成倾斜结构。" },
    { name: "反向交叉牵引", kind: "var", a: ["交叉影响", -0.75, 0, -0.48, 0.01], b: ["自身持续性", 0, 0.94, 0.62, 0.01], note: "反向影响可用于讨论多元系统中的反馈、振荡和解释难度。" },
  ],
  ch13: [
    { name: "短暂波动团块", kind: "garch", a: ["冲击反馈 α", 0.02, 0.35, 0.25, 0.01], b: ["波动持续 β", 0.1, 0.94, 0.42, 0.01], note: "高冲击反馈但低持续性会产生尖锐但短暂的方差跳升。" },
    { name: "长期波动记忆", kind: "garch", a: ["冲击反馈 α", 0.02, 0.28, 0.08, 0.01], b: ["波动持续 β", 0.55, 0.96, 0.9, 0.01], note: "高 β 让波动团块持续更久，适合连接风险预测和条件方差。" },
  ],
  ch14: [
    { name: "偏差与一致性", kind: "asymptotic", a: ["偏差强度", -0.4, 0.4, 0.22, 0.01], b: ["尾部厚度", 0, 1, 0.15, 0.01], note: "分布收缩不代表中心正确，偏差会让估计量稳定到错误位置。" },
    { name: "厚尾下的慢近似", kind: "asymptotic", a: ["偏差强度", -0.1, 0.1, 0, 0.01], b: ["尾部厚度", 0, 1, 0.85, 0.01], note: "厚尾会拖慢正态近似，适合讨论矩条件和稳健推断。" },
  ],
  ch15: [
    { name: "少量重抽样的不稳定", kind: "bootstrap", a: ["真实 φ", 0.05, 0.95, 0.48, 0.01], b: ["重抽样次数", 20, 140, 50, 10], note: "重抽样次数较少时，Bootstrap 分布本身也会明显抖动。" },
    { name: "近单位根 Bootstrap", kind: "bootstrap", a: ["真实 φ", 0.65, 0.98, 0.9, 0.01], b: ["重抽样次数", 80, 420, 260, 10], note: "φ 接近 1 时，区间会更宽，残差 Bootstrap 的可靠性也更依赖模型设定。" },
  ],
  appA: [
    { name: "少量基函数近似", kind: "basis", a: ["基函数个数", 1, 14, 3, 1], b: ["高频权重", 0, 1.4, 0.2, 0.01], note: "少量低频基函数给出粗略形状，适合解释投影近似。" },
    { name: "高频细节叠加", kind: "basis", a: ["基函数个数", 4, 18, 12, 1], b: ["高频权重", 0, 1.4, 1.05, 0.01], note: "提高高频权重后，局部振荡增加，适合讨论过拟合与频域能量。" },
  ],
  appB: [
    { name: "快速弱依赖", kind: "dependence", a: ["衰减速度", 0.25, 0.9, 0.62, 0.01], b: ["初始冲击", 0.2, 1.8, 0.9, 0.01], note: "快速衰减展示短程依赖的理想图像，远期冲击影响很快消失。" },
    { name: "慢速依赖尾部", kind: "dependence", a: ["衰减速度", 0.02, 0.25, 0.06, 0.01], b: ["初始冲击", 0.2, 1.8, 1.35, 0.01], note: "慢衰减让早期冲击长时间保留，适合讨论极限定理需要额外条件。" },
  ],
};

const quizBank = {
  ch01: { q: "为什么同一个随机模型每次生成的时间序列曲线不同，却仍然可以说它们来自同一机制？", a: "因为模型规定的是分布、依赖结构和参数，而不是唯一的一条路径。样本路径不同，但统计规律可以相同。" },
  ch02: { q: "差分为什么常用于处理趋势？它可能带来什么副作用？", a: "差分把水平变化转为相邻增量，能削弱低频趋势；副作用是可能放大高频噪声，并产生过度差分导致的负相关。" },
  ch03: { q: "弱平稳至少要求哪些量不随时间改变？", a: "均值恒定，方差有限且恒定，自协方差只依赖滞后 h 而不依赖具体时间 t。" },
  ch04: { q: "AR 和 MA 在 ACF 形状上最经典的区别是什么？", a: "理想情况下 AR 的 ACF 通常拖尾，MA(q) 的 ACF 在 q 阶后截尾；有限样本中这种信号会有噪声。" },
  ch05: { q: "线性投影中的正交误差条件是什么意思？", a: "预测误差和用于预测的信息变量线性不相关，表示在线性空间内已经没有可被解释变量继续利用的线性信息。" },
  ch06: { q: "PACF 相比 ACF 多回答了什么问题？", a: "PACF 扣除了中间滞后的线性影响，衡量给定中间历史后某一滞后是否仍有直接线性关系。" },
  ch07: { q: "为什么多步预测的不确定性通常会随步长增加？", a: "未来冲击会逐步累积，而且远期信息条件更弱，所以预测误差方差通常随预测步长扩大。" },
  ch08: { q: "为什么强相关序列的样本均值标准误不能直接套用 iid 公式？", a: "相邻观测携带重复信息，自协方差会进入均值方差，导致有效样本量小于名义样本量。" },
  ch09: { q: "目标函数很平坦时，参数估计会出现什么问题？", a: "小的样本扰动就可能造成较大的估计变化，说明参数识别弱、标准误较大或有限样本不稳定。" },
  ch10: { q: "谱密度和自协方差函数之间有什么核心关系？", a: "谱密度本质上是自协方差函数的 Fourier 变换，描述方差在不同频率上的分布。" },
  ch11: { q: "周期图为什么通常需要平滑？", a: "原始周期图方差很大，不是稳定的一致估计；平滑通过牺牲部分分辨率降低方差。" },
  ch12: { q: "VAR 模型中的交叉滞后系数可以直接解释为因果吗？", a: "不能直接解释为结构因果。它表示预测意义上的动态关联，因果解释还需要识别假设和外生变化。" },
  ch13: { q: "GARCH 模型为什么能描述波动聚集？", a: "条件方差依赖过去平方冲击和过去方差，大冲击会提高后续方差，并通过持续项逐步衰减。" },
  ch14: { q: "一致性和无偏性有什么区别？", a: "无偏性是有限样本期望等于真值；一致性是样本量增大时估计量概率收敛到真值。二者互不等价。" },
  ch15: { q: "时间序列 Bootstrap 为什么不能简单随机重排原观测值？", a: "简单重排会破坏时间依赖结构。残差或块 Bootstrap 需要尽量保留模型或局部依赖信息。" },
  appA: { q: "Parseval 恒等式在频域学习中提供了什么直觉？", a: "它说明时域能量和频域能量是同一件事的两种表示，帮助理解方差如何分配到不同频率。" },
  appB: { q: "物理依赖度量为什么采用替换早期冲击的思想？", a: "它直接衡量一个早期随机冲击对未来变量的影响强度，影响随滞后衰减越快，过程越接近弱依赖。" },
};

const focusPrompts = {
  preview: "预习时先用自己的话解释关键概念，再看图形是否符合直觉。",
  experiment: "实验时每次只改一个参数，并记录主图和诊断图分别发生了什么。",
  theory: "理论推导时把图形现象翻译成假设、矩条件、极限或优化目标。",
  review: "复习时先回答课堂自测，再回到公式锚点检查哪些条件被忽略。",
};

const state = {
  chapterIndex: 0,
  demoIndex: 0,
  level: "undergraduate",
  focus: "preview",
  showAnswer: false,
  sampleSize: 160,
  noise: 0.12,
  paramA: 0,
  paramB: 0,
  showTruth: true,
  showBands: true,
  showNotes: true,
  playing: true,
  clock: 0,
};

const elements = {
  courseStats: document.querySelector("#courseStats"),
  chapterList: document.querySelector("#chapterList"),
  chapterKicker: document.querySelector("#chapterKicker"),
  chapterTitle: document.querySelector("#chapterTitle"),
  chapterSubtitle: document.querySelector("#chapterSubtitle"),
  demoTabs: document.querySelector("#demoTabs"),
  demoSelect: document.querySelector("#demoSelect"),
  levelSelect: document.querySelector("#levelSelect"),
  focusSelect: document.querySelector("#focusSelect"),
  prevChapter: document.querySelector("#prevChapter"),
  nextChapter: document.querySelector("#nextChapter"),
  playToggle: document.querySelector("#playToggle"),
  mainCanvas: document.querySelector("#mainCanvas"),
  sideCanvas: document.querySelector("#sideCanvas"),
  primaryTitle: document.querySelector("#primaryTitle"),
  secondaryTitle: document.querySelector("#secondaryTitle"),
  primaryReadout: document.querySelector("#primaryReadout"),
  secondaryReadout: document.querySelector("#secondaryReadout"),
  conceptChips: document.querySelector("#conceptChips"),
  observationText: document.querySelector("#observationText"),
  formulaText: document.querySelector("#formulaText"),
  intuitionText: document.querySelector("#intuitionText"),
  experimentSteps: document.querySelector("#experimentSteps"),
  levelTitle: document.querySelector("#levelTitle"),
  levelPoints: document.querySelector("#levelPoints"),
  pitfallList: document.querySelector("#pitfallList"),
  discussionText: document.querySelector("#discussionText"),
  quizQuestion: document.querySelector("#quizQuestion"),
  revealAnswer: document.querySelector("#revealAnswer"),
  quizAnswer: document.querySelector("#quizAnswer"),
  paramA: document.querySelector("#paramA"),
  paramB: document.querySelector("#paramB"),
  paramALabel: document.querySelector("#paramALabel"),
  paramBLabel: document.querySelector("#paramBLabel"),
  paramAOutput: document.querySelector("#paramAOutput"),
  paramBOutput: document.querySelector("#paramBOutput"),
  sampleSize: document.querySelector("#sampleSize"),
  sampleOutput: document.querySelector("#sampleOutput"),
  noiseLevel: document.querySelector("#noiseLevel"),
  noiseOutput: document.querySelector("#noiseOutput"),
  showTruth: document.querySelector("#showTruth"),
  showBands: document.querySelector("#showBands"),
  showNotes: document.querySelector("#showNotes"),
  notePanel: document.querySelector("#notePanel"),
  noteBody: document.querySelector("#noteBody"),
};

const ctx = {
  main: elements.mainCanvas.getContext("2d"),
  side: elements.sideCanvas.getContext("2d"),
};

const colors = {
  ink: "#f5f1e8",
  muted: "#aeb8bd",
  grid: "rgba(98, 199, 242, 0.17)",
  gridStrong: "rgba(98, 199, 242, 0.28)",
  yellow: "#f7d45c",
  blue: "#62c7f2",
  red: "#ff7f6e",
  green: "#8bd46e",
  violet: "#b6a1ff",
  dim: "rgba(245, 241, 232, 0.2)",
  band: "rgba(98, 199, 242, 0.16)",
};

function currentChapter() {
  return chapters[state.chapterIndex];
}

function currentDemo() {
  return currentChapter().demos[state.demoIndex];
}

function init() {
  extendDemoCatalog();
  renderCourseStats();
  renderChapterNav();
  bindEvents();
  loadChapter(0);
  requestAnimationFrame(tick);
}

function extendDemoCatalog() {
  chapters.forEach((chapter) => {
    if (chapter.extended) return;
    chapter.demos.push(...(demoExtensions[chapter.id] || []));
    chapter.extended = true;
  });
}

function renderCourseStats() {
  const demoCount = chapters.reduce((sum, chapter) => sum + chapter.demos.length, 0);
  elements.courseStats.innerHTML = `
    <div class="stat-pill"><strong>${chapters.length}</strong><span>章节</span></div>
    <div class="stat-pill"><strong>${demoCount}</strong><span>演示</span></div>
    <div class="stat-pill"><strong>2</strong><span>层级</span></div>
  `;
}

function renderChapterNav() {
  elements.chapterList.innerHTML = "";
  chapters.forEach((chapter, index) => {
    const group = document.createElement("section");
    group.className = "chapter-group";
    group.dataset.chapterIndex = String(index);

    const button = document.createElement("button");
    button.className = "chapter-button";
    button.type = "button";
    button.innerHTML = `
      <span class="chapter-number">${chapter.number}</span>
      <span>
        <span class="chapter-name">${chapter.title}</span>
        <span class="chapter-topic">${chapter.topic}</span>
      </span>
    `;
    button.addEventListener("click", () => loadChapter(index));

    const demoList = document.createElement("div");
    demoList.className = "chapter-demos";
    chapter.demos.forEach((demo, demoIndex) => {
      const demoButton = document.createElement("button");
      demoButton.className = "chapter-demo-button";
      demoButton.type = "button";
      demoButton.textContent = demo.name;
      demoButton.addEventListener("click", () => {
        if (state.chapterIndex !== index) {
          state.chapterIndex = index;
          state.demoIndex = demoIndex;
          loadChapter(index, demoIndex);
        } else {
          selectDemo(demoIndex);
        }
      });
      demoList.append(demoButton);
    });

    group.append(button, demoList);
    elements.chapterList.append(group);
  });
}

function bindEvents() {
  elements.prevChapter.addEventListener("click", () => {
    loadChapter((state.chapterIndex - 1 + chapters.length) % chapters.length);
  });
  elements.nextChapter.addEventListener("click", () => {
    loadChapter((state.chapterIndex + 1) % chapters.length);
  });
  elements.playToggle.addEventListener("click", () => {
    state.playing = !state.playing;
    elements.playToggle.textContent = state.playing ? "暂停" : "播放";
    elements.playToggle.setAttribute("aria-pressed", String(state.playing));
  });
  elements.demoSelect.addEventListener("change", () => {
    selectDemo(Number(elements.demoSelect.value));
  });
  elements.levelSelect.addEventListener("change", () => {
    state.level = elements.levelSelect.value;
    state.showAnswer = false;
    renderKnowledgeCards();
  });
  elements.focusSelect.addEventListener("change", () => {
    state.focus = elements.focusSelect.value;
    state.showAnswer = false;
    renderKnowledgeCards();
  });
  elements.revealAnswer.addEventListener("click", () => {
    state.showAnswer = !state.showAnswer;
    renderQuiz();
  });
  elements.paramA.addEventListener("input", () => {
    state.paramA = Number(elements.paramA.value);
    updateOutputs();
  });
  elements.paramB.addEventListener("input", () => {
    state.paramB = Number(elements.paramB.value);
    updateOutputs();
  });
  elements.sampleSize.addEventListener("input", () => {
    state.sampleSize = Number(elements.sampleSize.value);
    updateOutputs();
  });
  elements.noiseLevel.addEventListener("input", () => {
    state.noise = Number(elements.noiseLevel.value);
    updateOutputs();
  });
  elements.showTruth.addEventListener("change", () => {
    state.showTruth = elements.showTruth.checked;
  });
  elements.showBands.addEventListener("change", () => {
    state.showBands = elements.showBands.checked;
  });
  elements.showNotes.addEventListener("change", () => {
    state.showNotes = elements.showNotes.checked;
    elements.notePanel.hidden = !state.showNotes;
  });
  window.addEventListener("resize", draw);
}

function loadChapter(index, demoIndex = 0) {
  state.chapterIndex = index;
  state.demoIndex = demoIndex;
  state.showAnswer = false;
  const chapter = currentChapter();
  elements.chapterKicker.textContent = chapter.number.length === 1 ? `Appendix ${chapter.number}` : `Chapter ${chapter.number}`;
  elements.chapterTitle.textContent = chapter.title;
  elements.chapterSubtitle.textContent = chapter.topic;
  elements.conceptChips.innerHTML = chapter.concepts.map((item) => `<span class="chip">${item}</span>`).join("");
  elements.formulaText.textContent = chapter.formula;
  [...elements.chapterList.children].forEach((group, i) => {
    group.classList.toggle("is-active", i === index);
    const button = group.querySelector(".chapter-button");
    button.setAttribute("aria-current", String(i === index));
  });
  elements.demoSelect.innerHTML = "";
  chapter.demos.forEach((demo, demoIndex) => {
    const option = document.createElement("option");
    option.value = String(demoIndex);
    option.textContent = demo.name;
    elements.demoSelect.append(option);
  });
  elements.demoSelect.value = String(state.demoIndex);
  renderDemoTabs();
  updateDemoNavState();
  renderKnowledgeCards();
  loadDemo();
}

function loadDemo() {
  const demo = currentDemo();
  state.showAnswer = false;
  configureSlider(elements.paramA, demo.a);
  configureSlider(elements.paramB, demo.b);
  state.paramA = Number(demo.a[3]);
  state.paramB = Number(demo.b[3]);
  elements.paramA.value = state.paramA;
  elements.paramB.value = state.paramB;
  elements.paramALabel.textContent = demo.a[0];
  elements.paramBLabel.textContent = demo.b[0];
  elements.observationText.textContent = demo.note;
  elements.noteBody.textContent = demo.note;
  elements.primaryTitle.textContent = demo.name;
  elements.secondaryTitle.textContent = sideTitleFor(demo.kind);
  renderKnowledgeCards();
  updateOutputs();
  updateDemoNavState();
}

function selectDemo(demoIndex) {
  state.demoIndex = demoIndex;
  elements.demoSelect.value = String(demoIndex);
  loadDemo();
}

function renderDemoTabs() {
  elements.demoTabs.innerHTML = "";
  currentChapter().demos.forEach((demo, demoIndex) => {
    const button = document.createElement("button");
    button.className = "demo-tab";
    button.type = "button";
    button.textContent = demo.name;
    button.addEventListener("click", () => selectDemo(demoIndex));
    elements.demoTabs.append(button);
  });
}

function updateDemoNavState() {
  [...elements.demoTabs.children].forEach((button, index) => {
    button.setAttribute("aria-pressed", String(index === state.demoIndex));
  });
  [...elements.chapterList.children].forEach((group, chapterIndex) => {
    [...group.querySelectorAll(".chapter-demo-button")].forEach((button, demoIndex) => {
      const active = chapterIndex === state.chapterIndex && demoIndex === state.demoIndex;
      button.setAttribute("aria-current", String(active));
    });
  });
}

function renderKnowledgeCards() {
  const chapter = currentChapter();
  const profile = chapterEnrichment[chapter.id] || makeFallbackProfile(chapter);
  const levelPoints = state.level === "graduate" ? profile.graduate : profile.undergraduate;
  const focusPrompt = focusPrompts[state.focus] || focusPrompts.preview;
  elements.intuitionText.textContent = profile.intuition;
  elements.experimentSteps.innerHTML = profile.steps.map((item) => `<li>${item}</li>`).join("");
  elements.levelTitle.textContent = state.level === "graduate" ? "研究生深化点" : "本科掌握点";
  elements.levelPoints.innerHTML = levelPoints.map((item) => `<li>${item}</li>`).join("");
  elements.pitfallList.innerHTML = profile.pitfalls.map((item) => `<li>${item}</li>`).join("");
  elements.discussionText.textContent = `${focusPrompt} ${profile.discussion}`;
  renderQuiz();
  if (elements.showNotes.checked) {
    elements.noteBody.textContent = `${currentDemo().note} ${focusPrompt} ${state.level === "graduate" ? profile.graduate[0] : profile.undergraduate[0]}`;
  }
}

function renderQuiz() {
  const quiz = quizBank[currentChapter().id] || { q: "本章最关键的模型假设是什么？", a: "回到公式锚点，逐一检查均值、方差、依赖和样本量条件。" };
  elements.quizQuestion.textContent = quiz.q;
  elements.quizAnswer.textContent = quiz.a;
  elements.quizAnswer.hidden = !state.showAnswer;
  elements.revealAnswer.textContent = state.showAnswer ? "隐藏答案" : "显示答案";
  elements.revealAnswer.setAttribute("aria-expanded", String(state.showAnswer));
}

function makeFallbackProfile(chapter) {
  return {
    intuition: `${chapter.topic} 是本章理解后续模型和推断的入口。`,
    steps: ["先观察主图的样本路径。", "再调节参数并比较右侧诊断视图。", "最后把图形变化和公式锚点对应起来。"],
    undergraduate: [`能解释 ${chapter.concepts[0]} 的基本含义。`, "能用图形语言描述参数变化带来的现象。"],
    graduate: ["能说明本章关键假设在估计和推断中的作用。", "能把图形直觉连接到渐近理论或模型识别。"],
    pitfalls: ["不要只凭单次模拟下结论。", "不要把图形现象和数学条件混为一谈。"],
    discussion: "尝试把本章概念应用到一个真实数据集，并说明模型假设是否可信。",
  };
}

function configureSlider(input, config) {
  input.min = config[1];
  input.max = config[2];
  input.step = config[4];
}

function updateOutputs() {
  const demo = currentDemo();
  elements.paramAOutput.textContent = formatValue(state.paramA, demo.a[4]);
  elements.paramBOutput.textContent = formatValue(state.paramB, demo.b[4]);
  elements.sampleOutput.textContent = String(state.sampleSize);
  elements.noiseOutput.textContent = `${Math.round(state.noise * 100)}%`;
  elements.primaryReadout.textContent = `n = ${state.sampleSize}`;
}

function formatValue(value, step) {
  if (step >= 1) return String(Math.round(value));
  return value.toFixed(step < 0.01 ? 3 : 2);
}

function sideTitleFor(kind) {
  const titles = {
    filter: "滤波结果",
    trend: "差分与残差",
    stationarity: "滚动统计",
    arma: "ACF 形状",
    projection: "投影几何",
    acf: "ACF / PACF",
    forecast: "预测区间",
    mean: "抽样分布",
    likelihood: "目标函数轮廓",
    fourier: "绕线与频谱",
    periodogram: "周期图",
    var: "交叉关系",
    garch: "条件方差",
    asymptotic: "极限分布",
    bootstrap: "Bootstrap 分布",
    basis: "基函数能量",
    dependence: "衰减曲线",
  };
  return titles[kind] || "诊断视图";
}

function tick() {
  if (state.playing) state.clock += 0.012;
  draw();
  requestAnimationFrame(tick);
}

function draw() {
  const demo = currentDemo();
  const data = generateData(demo.kind);
  clearCanvas(elements.mainCanvas, ctx.main);
  clearCanvas(elements.sideCanvas, ctx.side);
  drawMainSeries(data, demo.kind);
  drawSideView(data, demo.kind);
}

function generateData(kind) {
  const n = state.sampleSize;
  const noise = state.noise;
  const a = state.paramA;
  const b = state.paramB;
  const values = [];
  const aux = [];
  let prev = 0;
  let prev2 = 0;
  let variance = 0.35;
  let x = 0;
  let y = 0;

  for (let i = 0; i < n; i += 1) {
    const t = i / Math.max(1, n - 1);
    const eps = seededNoise(i, kind) * (0.35 + noise * 1.4);
    let value = 0;
    let helper = 0;

    if (kind === "filter") {
      const period = a;
      value = Math.sin(TAU * i / period) + 0.45 * Math.sin(TAU * i / (period * 0.42)) + eps;
    } else if (kind === "trend") {
      const centered = t - 0.5;
      const trend = 2.2 * a * centered * centered + 1.2 * centered;
      value = trend + b * Math.sin(TAU * t * 4) + eps * 0.72;
      helper = i > 0 ? value - values[i - 1] : 0;
    } else if (kind === "stationarity") {
      const phi = Math.min(1.02, a);
      prev = phi * prev + eps;
      value = prev + (a > 0.97 ? 0.035 * i : 0);
    } else if (kind === "arma") {
      value = a * prev + eps + b * seededNoise(i - 1, kind) * 0.55;
      prev = value;
    } else if (kind === "projection") {
      const px = 2 * t - 1;
      const py = a * px + Math.sqrt(Math.max(0.04, 1 - a * a)) * eps;
      value = px;
      helper = py * b;
    } else if (kind === "acf") {
      value = a * prev + b * prev2 + eps;
      prev2 = prev;
      prev = value;
    } else if (kind === "forecast") {
      value = a * prev + eps;
      prev = value;
    } else if (kind === "mean") {
      value = a * prev + eps;
      prev = value;
      helper = (aux[i - 1] || 0) + value;
    } else if (kind === "likelihood") {
      value = a * prev + eps;
      prev = value;
    } else if (kind === "fourier") {
      value = Math.sin(TAU * 3 * t * 4 + 0.4) + 0.72 * Math.sin(TAU * b * t * 4 + 1.2) + eps * 0.38;
    } else if (kind === "periodogram") {
      value = Math.sin(TAU * a * t * 4 + 0.3) + 0.45 * Math.sin(TAU * 5.4 * t * 4) + eps * 0.4;
    } else if (kind === "var") {
      const ex = seededNoise(i, "var-x") * (0.35 + noise);
      const ey = seededNoise(i, "var-y") * (0.35 + noise);
      const nextX = b * x + a * y + ex;
      const nextY = a * x + b * y + ey;
      x = nextX;
      y = nextY;
      value = x;
      helper = y;
    } else if (kind === "garch") {
      variance = 0.08 + a * prev * prev + b * variance;
      value = Math.sqrt(Math.max(0.001, variance)) * seededNoise(i, kind);
      helper = variance;
      prev = value;
    } else if (kind === "asymptotic") {
      value = Math.sin(TAU * t * 2) * 0.18 + eps;
      helper = a + value / Math.sqrt(Math.max(1, n / 40));
    } else if (kind === "bootstrap") {
      value = a * prev + eps;
      prev = value;
    } else if (kind === "basis") {
      const terms = Math.max(1, Math.round(a));
      for (let k = 1; k <= terms; k += 1) {
        const weight = k === 1 ? 1 : b / k;
        value += weight * Math.sin(TAU * k * t + k * 0.35);
      }
      value /= Math.max(1, Math.log2(terms + 1));
    } else if (kind === "dependence") {
      value = b * Math.exp(-a * i * 0.16) + eps * 0.1;
      helper = b * Math.exp(-a * i * 0.16);
    }

    values.push(value);
    aux.push(helper);
  }

  return normalizeData({ values, aux, kind });
}

function normalizeData(data) {
  const maxValue = Math.max(0.5, ...data.values.map((v) => Math.abs(v)), ...data.aux.map((v) => Math.abs(v || 0)));
  return {
    ...data,
    values: data.values.map((v) => v / maxValue),
    aux: data.aux.map((v) => (v || 0) / maxValue),
    rawMax: maxValue,
  };
}

function seededNoise(index, salt = "") {
  const saltValue = [...salt].reduce((sum, ch) => sum + ch.charCodeAt(0), 0);
  const base = Math.sin((index + 1) * 12.9898 + saltValue * 0.071 + Math.floor(state.clock * 8) * 0.17);
  const detail = Math.sin((index + 3) * 78.233 + saltValue * 0.131);
  return fract(base * 43758.5453 + detail * 19431.123);
}

function fract(value) {
  return (value - Math.floor(value) - 0.5) * 2;
}

function canvasSize(canvas, context) {
  const rect = canvas.getBoundingClientRect();
  const ratio = Math.max(1, window.devicePixelRatio || 1);
  const width = Math.max(1, Math.round(rect.width * ratio));
  const height = Math.max(1, Math.round(rect.height * ratio));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  return { width: rect.width, height: rect.height };
}

function clearCanvas(canvas, context) {
  const size = canvasSize(canvas, context);
  context.clearRect(0, 0, size.width, size.height);
  context.fillStyle = "#030506";
  context.fillRect(0, 0, size.width, size.height);
  drawGrid(context, size);
  return size;
}

function drawGrid(context, size) {
  context.save();
  context.strokeStyle = colors.grid;
  context.lineWidth = 1;
  for (let i = 1; i < 6; i += 1) {
    const y = (size.height / 6) * i;
    context.beginPath();
    context.moveTo(0, y);
    context.lineTo(size.width, y);
    context.stroke();
  }
  for (let i = 1; i < 8; i += 1) {
    const x = (size.width / 8) * i;
    context.beginPath();
    context.moveTo(x, 0);
    context.lineTo(x, size.height);
    context.stroke();
  }
  context.restore();
}

function drawMainSeries(data, kind) {
  const size = canvasSize(elements.mainCanvas, ctx.main);
  const pad = { left: 42, right: 24, top: 58, bottom: 36 };
  const zeroY = pad.top + (size.height - pad.top - pad.bottom) / 2;
  drawAxis(ctx.main, pad, size, zeroY);

  if (kind === "projection") {
    drawProjectionMain(data, size, pad);
    return;
  }
  if (kind === "basis") {
    drawSeries(ctx.main, data.values, size, pad, colors.yellow, 2.4);
    drawZeroLine(ctx.main, size, pad);
    drawPlayhead(ctx.main, size, pad);
    return;
  }
  if (kind === "garch" && state.showTruth) {
    drawSeries(ctx.main, data.aux.map((v) => Math.sqrt(Math.abs(v))), size, pad, colors.green, 2);
  }
  if (kind === "var") {
    drawSeries(ctx.main, data.aux, size, pad, colors.violet, 2);
  }
  if (state.showBands && ["forecast", "asymptotic", "bootstrap"].includes(kind)) {
    drawBand(ctx.main, size, pad, 0.28 + state.noise * 0.3);
  }
  drawSeries(ctx.main, data.values, size, pad, colors.yellow, 2.4);
  drawZeroLine(ctx.main, size, pad);
  drawPlayhead(ctx.main, size, pad);
}

function drawAxis(context, pad, size, zeroY) {
  context.save();
  context.strokeStyle = colors.gridStrong;
  context.lineWidth = 1;
  context.beginPath();
  context.moveTo(pad.left, zeroY);
  context.lineTo(size.width - pad.right, zeroY);
  context.stroke();
  context.fillStyle = colors.muted;
  context.font = "12px Segoe UI, sans-serif";
  context.fillText("t", size.width - pad.right - 8, zeroY + 18);
  context.restore();
}

function drawSeries(context, values, size, pad, stroke, lineWidth) {
  const innerW = size.width - pad.left - pad.right;
  const innerH = size.height - pad.top - pad.bottom;
  const zeroY = pad.top + innerH / 2;
  context.save();
  context.strokeStyle = stroke;
  context.lineWidth = lineWidth;
  context.beginPath();
  values.forEach((value, i) => {
    const x = pad.left + (i / Math.max(1, values.length - 1)) * innerW;
    const y = zeroY - value * innerH * 0.43;
    if (i === 0) context.moveTo(x, y);
    else context.lineTo(x, y);
  });
  context.stroke();
  context.restore();
}

function drawZeroLine(context, size, pad) {
  const zeroY = pad.top + (size.height - pad.top - pad.bottom) / 2;
  context.save();
  context.strokeStyle = colors.dim;
  context.setLineDash([5, 5]);
  context.beginPath();
  context.moveTo(pad.left, zeroY);
  context.lineTo(size.width - pad.right, zeroY);
  context.stroke();
  context.restore();
}

function drawPlayhead(context, size, pad) {
  const innerW = size.width - pad.left - pad.right;
  const x = pad.left + ((state.clock * 0.16) % 1) * innerW;
  context.save();
  context.strokeStyle = colors.red;
  context.lineWidth = 1.2;
  context.setLineDash([4, 6]);
  context.beginPath();
  context.moveTo(x, pad.top);
  context.lineTo(x, size.height - pad.bottom);
  context.stroke();
  context.restore();
}

function drawBand(context, size, pad, width) {
  const innerW = size.width - pad.left - pad.right;
  const innerH = size.height - pad.top - pad.bottom;
  const zeroY = pad.top + innerH / 2;
  context.save();
  context.fillStyle = colors.band;
  context.beginPath();
  context.moveTo(pad.left, zeroY - width * innerH);
  context.lineTo(size.width - pad.right, zeroY - width * innerH * 0.7);
  context.lineTo(size.width - pad.right, zeroY + width * innerH * 0.7);
  context.lineTo(pad.left, zeroY + width * innerH);
  context.closePath();
  context.fill();
  context.restore();
}

function drawProjectionMain(data, size, pad) {
  const context = ctx.main;
  const innerW = size.width - pad.left - pad.right;
  const innerH = size.height - pad.top - pad.bottom;
  const cx = pad.left + innerW / 2;
  const cy = pad.top + innerH / 2;
  context.save();
  context.strokeStyle = colors.gridStrong;
  context.beginPath();
  context.moveTo(pad.left, cy);
  context.lineTo(size.width - pad.right, cy);
  context.moveTo(cx, pad.top);
  context.lineTo(cx, size.height - pad.bottom);
  context.stroke();
  context.fillStyle = colors.yellow;
  data.values.forEach((xValue, i) => {
    const x = cx + xValue * innerW * 0.42;
    const y = cy - data.aux[i] * innerH * 0.42;
    context.globalAlpha = 0.72;
    context.beginPath();
    context.arc(x, y, 2.1, 0, TAU);
    context.fill();
  });
  context.globalAlpha = 1;
  context.strokeStyle = colors.red;
  context.lineWidth = 2;
  context.beginPath();
  context.moveTo(pad.left, cy + state.paramA * innerH * 0.42);
  context.lineTo(size.width - pad.right, cy - state.paramA * innerH * 0.42);
  context.stroke();
  context.restore();
}

function drawSideView(data, kind) {
  const size = canvasSize(elements.sideCanvas, ctx.side);
  const pad = { left: 42, right: 22, top: 56, bottom: 36 };
  const handlers = {
    filter: drawFilterSide,
    trend: drawTrendSide,
    stationarity: drawRollingSide,
    arma: drawAcfSide,
    projection: drawProjectionSide,
    acf: drawAcfPacfSide,
    forecast: drawForecastSide,
    mean: drawMeanSide,
    likelihood: drawLikelihoodSide,
    fourier: drawFourierSide,
    periodogram: drawPeriodogramSide,
    var: drawVarSide,
    garch: drawGarchSide,
    asymptotic: drawAsymptoticSide,
    bootstrap: drawBootstrapSide,
    basis: drawBasisSide,
    dependence: drawDependenceSide,
  };
  (handlers[kind] || drawAcfSide)(data, size, pad);
}

function drawFilterSide(data, size, pad) {
  const window = Math.max(1, Math.round(state.paramB));
  const smooth = movingAverage(data.values, window);
  drawSeries(ctx.side, data.values, size, pad, colors.dim, 1.2);
  drawSeries(ctx.side, smooth, size, pad, colors.blue, 2.5);
  elements.secondaryReadout.textContent = `窗口 ${window}`;
}

function drawTrendSide(data, size, pad) {
  drawSeries(ctx.side, data.aux, size, pad, colors.red, 2.2);
  drawZeroLine(ctx.side, size, pad);
  elements.secondaryReadout.textContent = "一阶差分";
}

function drawRollingSide(data, size, pad) {
  const window = Math.max(3, Math.round(state.paramB));
  drawSeries(ctx.side, rollingMean(data.values, window), size, pad, colors.blue, 2.2);
  drawSeries(ctx.side, rollingVariance(data.values, window), size, pad, colors.green, 2);
  elements.secondaryReadout.textContent = `窗口 ${window}`;
}

function drawAcfSide(data, size, pad) {
  drawBars(ctx.side, acf(data.values, 24), size, pad, colors.blue, "ACF");
}

function drawProjectionSide(data, size, pad) {
  const residuals = data.aux.map((y, i) => y - state.paramA * data.values[i]);
  drawSeries(ctx.side, residuals, size, pad, colors.red, 2);
  drawZeroLine(ctx.side, size, pad);
  elements.secondaryReadout.textContent = "残差";
}

function drawAcfPacfSide(data, size, pad) {
  const acfValues = acf(data.values, 18);
  const pacfValues = acfValues.map((v, i) => (i === 0 ? v : v * Math.exp(-i * 0.22)));
  drawBars(ctx.side, acfValues, size, pad, colors.blue, "ACF");
  drawBars(ctx.side, pacfValues, size, { ...pad, top: pad.top + 120 }, colors.violet, "PACF");
}

function drawForecastSide(data, size, pad) {
  const horizon = Math.round(state.paramB);
  const last = data.values[data.values.length - 1] || 0;
  const forecast = [];
  for (let h = 1; h <= horizon; h += 1) forecast.push(last * Math.pow(state.paramA, h));
  const combined = data.values.slice(-Math.min(80, data.values.length)).concat(forecast);
  if (state.showBands) drawBand(ctx.side, size, pad, 0.2 + horizon / 90);
  drawSeries(ctx.side, combined, size, pad, colors.yellow, 2.2);
  drawSeries(ctx.side, new Array(data.values.slice(-Math.min(80, data.values.length)).length).fill(null).concat(forecast).map((v) => v ?? 0), size, pad, colors.red, 2.2);
  elements.secondaryReadout.textContent = `${horizon} 步`;
}

function drawMeanSide(data, size, pad) {
  const reps = Math.round(state.paramB);
  const means = [];
  for (let r = 0; r < reps; r += 1) {
    let prev = 0;
    let sum = 0;
    for (let i = 0; i < state.sampleSize; i += 1) {
      prev = state.paramA * prev + seededNoise(i + r * 13, "mean-rep") * (0.35 + state.noise);
      sum += prev;
    }
    means.push(sum / state.sampleSize);
  }
  drawHistogram(ctx.side, means, size, pad, colors.blue);
  elements.secondaryReadout.textContent = `${reps} 次`;
}

function drawLikelihoodSide(data, size, pad) {
  const candidates = [];
  for (let i = 0; i <= 80; i += 1) {
    const phi = -0.98 + (i / 80) * 1.96;
    let sse = 0;
    for (let t = 1; t < data.values.length; t += 1) {
      const err = data.values[t] - phi * data.values[t - 1];
      sse += err * err;
    }
    candidates.push(-sse / data.values.length);
  }
  drawCurve(ctx.side, candidates, size, pad, colors.green);
  elements.secondaryReadout.textContent = "CLS";
}

function drawFourierSide(data, size, pad) {
  const winding = fourierAt(data.values, state.paramA);
  const cx = size.width * 0.5;
  const cy = size.height * 0.5 + 12;
  const radius = Math.min(size.width, size.height) * 0.31;
  ctx.side.save();
  ctx.side.strokeStyle = colors.gridStrong;
  ctx.side.beginPath();
  ctx.side.arc(cx, cy, radius, 0, TAU);
  ctx.side.stroke();
  ctx.side.strokeStyle = colors.yellow;
  ctx.side.lineWidth = 1.4;
  ctx.side.beginPath();
  winding.points.forEach((p, i) => {
    const x = cx + p.x * radius;
    const y = cy + p.y * radius;
    if (i === 0) ctx.side.moveTo(x, y);
    else ctx.side.lineTo(x, y);
  });
  ctx.side.stroke();
  ctx.side.fillStyle = colors.red;
  ctx.side.beginPath();
  ctx.side.arc(cx + winding.center.x * radius, cy + winding.center.y * radius, 6, 0, TAU);
  ctx.side.fill();
  ctx.side.restore();
  elements.secondaryReadout.textContent = `质心 ${winding.mag.toFixed(2)}`;
}

function drawPeriodogramSide(data, size, pad) {
  const spec = spectrum(data.values, 48);
  const smooth = movingAverage(spec, Math.round(state.paramB));
  drawCurve(ctx.side, spec, size, pad, colors.dim);
  drawCurve(ctx.side, smooth, size, pad, colors.blue);
  elements.secondaryReadout.textContent = `带宽 ${Math.round(state.paramB)}`;
}

function drawVarSide(data, size, pad) {
  drawProjectionMain({ values: data.values, aux: data.aux }, size, pad);
  elements.secondaryReadout.textContent = "相图";
}

function drawGarchSide(data, size, pad) {
  drawSeries(ctx.side, data.aux, size, pad, colors.green, 2.2);
  elements.secondaryReadout.textContent = "σ²";
}

function drawAsymptoticSide(data, size, pad) {
  const samples = [];
  for (let i = 0; i < 220; i += 1) {
    const z = seededNoise(i, "asym") + state.paramB * seededNoise(i * 3, "tail") ** 3;
    samples.push(state.paramA + z / Math.sqrt(state.sampleSize / 25));
  }
  drawHistogram(ctx.side, samples, size, pad, colors.violet);
  elements.secondaryReadout.textContent = "抽样";
}

function drawBootstrapSide(data, size, pad) {
  const reps = Math.round(state.paramB);
  const estimates = [];
  for (let r = 0; r < reps; r += 1) {
    let numerator = 0;
    let denominator = 0.001;
    for (let i = 1; i < data.values.length; i += 1) {
      const y = data.values[(i + r * 7) % data.values.length];
      const lag = data.values[(i - 1 + r * 5) % data.values.length];
      numerator += y * lag;
      denominator += lag * lag;
    }
    estimates.push(numerator / denominator);
  }
  drawHistogram(ctx.side, estimates, size, pad, colors.blue);
  elements.secondaryReadout.textContent = `${reps} 次`;
}

function drawBasisSide(data, size, pad) {
  const terms = Math.round(state.paramA);
  const bars = [];
  for (let k = 1; k <= 14; k += 1) bars.push(k <= terms ? (k === 1 ? 1 : state.paramB / k) : 0);
  drawBars(ctx.side, bars, size, pad, colors.yellow, "能量");
  elements.secondaryReadout.textContent = `${terms} 个基`;
}

function drawDependenceSide(data, size, pad) {
  drawSeries(ctx.side, data.aux, size, pad, colors.green, 2.5);
  drawSeries(ctx.side, data.values, size, pad, colors.dim, 1);
  elements.secondaryReadout.textContent = "δq(k)";
}

function movingAverage(values, window) {
  return values.map((_, i) => {
    let sum = 0;
    let count = 0;
    for (let j = Math.max(0, i - window + 1); j <= i; j += 1) {
      sum += values[j];
      count += 1;
    }
    return sum / count;
  });
}

function rollingMean(values, window) {
  return values.map((_, i) => {
    const start = Math.max(0, i - window + 1);
    const part = values.slice(start, i + 1);
    return part.reduce((sum, value) => sum + value, 0) / part.length;
  });
}

function rollingVariance(values, window) {
  return values.map((_, i) => {
    const start = Math.max(0, i - window + 1);
    const part = values.slice(start, i + 1);
    const mean = part.reduce((sum, value) => sum + value, 0) / part.length;
    return part.reduce((sum, value) => sum + (value - mean) ** 2, 0) / part.length;
  });
}

function acf(values, maxLag) {
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const denom = values.reduce((sum, value) => sum + (value - mean) ** 2, 0) || 1;
  const result = [];
  for (let lag = 0; lag <= maxLag; lag += 1) {
    let num = 0;
    for (let i = 0; i < values.length - lag; i += 1) num += (values[i] - mean) * (values[i + lag] - mean);
    result.push(num / denom);
  }
  return result;
}

function spectrum(values, bins) {
  const result = [];
  for (let k = 0; k < bins; k += 1) {
    let re = 0;
    let im = 0;
    for (let t = 0; t < values.length; t += 1) {
      const angle = -TAU * k * t / values.length;
      re += values[t] * Math.cos(angle);
      im += values[t] * Math.sin(angle);
    }
    result.push(Math.hypot(re, im) / values.length);
  }
  return result;
}

function fourierAt(values, freq) {
  const points = [];
  let sumX = 0;
  let sumY = 0;
  values.forEach((value, i) => {
    const t = i / Math.max(1, values.length - 1);
    const angle = -TAU * freq * t * 4;
    const x = value * Math.cos(angle);
    const y = value * Math.sin(angle);
    points.push({ x, y });
    sumX += x;
    sumY += y;
  });
  const center = { x: sumX / values.length, y: sumY / values.length };
  return { points, center, mag: Math.hypot(center.x, center.y) };
}

function drawBars(context, values, size, pad, fill, label) {
  const innerW = size.width - pad.left - pad.right;
  const innerH = size.height - pad.top - pad.bottom;
  const zeroY = pad.top + innerH / 2;
  const maxAbs = Math.max(0.2, ...values.map((v) => Math.abs(v)));
  context.save();
  context.strokeStyle = colors.dim;
  context.beginPath();
  context.moveTo(pad.left, zeroY);
  context.lineTo(size.width - pad.right, zeroY);
  context.stroke();
  context.fillStyle = fill;
  values.forEach((value, i) => {
    const x = pad.left + (i / values.length) * innerW + 2;
    const w = Math.max(3, innerW / values.length - 4);
    const h = (value / maxAbs) * innerH * 0.42;
    context.fillRect(x, zeroY - h, w, h);
  });
  context.fillStyle = colors.muted;
  context.font = "12px Segoe UI, sans-serif";
  context.fillText(label, pad.left, pad.top - 14);
  context.restore();
  elements.secondaryReadout.textContent = label;
}

function drawCurve(context, values, size, pad, stroke) {
  const max = Math.max(...values);
  const min = Math.min(...values);
  const span = max - min || 1;
  const mapped = values.map((value) => ((value - min) / span) * 1.7 - 0.85);
  drawSeries(context, mapped, size, pad, stroke, 2.2);
}

function drawHistogram(context, values, size, pad, fill) {
  const bins = 26;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const counts = new Array(bins).fill(0);
  values.forEach((value) => {
    const index = Math.max(0, Math.min(bins - 1, Math.floor(((value - min) / span) * bins)));
    counts[index] += 1;
  });
  const maxCount = Math.max(1, ...counts);
  const innerW = size.width - pad.left - pad.right;
  const innerH = size.height - pad.top - pad.bottom;
  context.save();
  context.fillStyle = fill;
  counts.forEach((count, i) => {
    const h = (count / maxCount) * innerH * 0.82;
    const x = pad.left + (i / bins) * innerW + 2;
    const y = size.height - pad.bottom - h;
    const w = Math.max(3, innerW / bins - 4);
    context.fillRect(x, y, w, h);
  });
  context.restore();
}

init();
