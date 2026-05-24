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

const state = {
  chapterIndex: 0,
  demoIndex: 0,
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
  chapterList: document.querySelector("#chapterList"),
  chapterKicker: document.querySelector("#chapterKicker"),
  chapterTitle: document.querySelector("#chapterTitle"),
  chapterSubtitle: document.querySelector("#chapterSubtitle"),
  demoSelect: document.querySelector("#demoSelect"),
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
  renderChapterNav();
  bindEvents();
  loadChapter(0);
  requestAnimationFrame(tick);
}

function renderChapterNav() {
  elements.chapterList.innerHTML = "";
  chapters.forEach((chapter, index) => {
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
    elements.chapterList.append(button);
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
    state.demoIndex = Number(elements.demoSelect.value);
    loadDemo();
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

function loadChapter(index) {
  state.chapterIndex = index;
  state.demoIndex = 0;
  const chapter = currentChapter();
  elements.chapterKicker.textContent = chapter.number.length === 1 ? `Appendix ${chapter.number}` : `Chapter ${chapter.number}`;
  elements.chapterTitle.textContent = chapter.title;
  elements.chapterSubtitle.textContent = chapter.topic;
  elements.conceptChips.innerHTML = chapter.concepts.map((item) => `<span class="chip">${item}</span>`).join("");
  elements.formulaText.textContent = chapter.formula;
  [...elements.chapterList.children].forEach((button, i) => {
    button.setAttribute("aria-current", String(i === index));
  });
  elements.demoSelect.innerHTML = "";
  chapter.demos.forEach((demo, demoIndex) => {
    const option = document.createElement("option");
    option.value = String(demoIndex);
    option.textContent = demo.name;
    elements.demoSelect.append(option);
  });
  loadDemo();
}

function loadDemo() {
  const demo = currentDemo();
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
  updateOutputs();
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
