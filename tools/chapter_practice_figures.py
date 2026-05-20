"""Shared Python practice figures for the time series course chapters."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.linalg import toeplitz
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.stattools import acf, pacf, yule_walker


def _fig_dir(chapter_dir: str | Path) -> Path:
    path = Path(chapter_dir).resolve()
    if path.is_file():
        base = path.parents[1]
    elif path.name == "scripts":
        base = path.parent
    else:
        base = path
    out = base / "figures"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _save(fig_dir: Path, name: str) -> None:
    plt.tight_layout()
    plt.savefig(fig_dir / name, dpi=180)
    plt.close()


def _ar1(phi: float, n: int, seed: int = 20260520, sigma: float = 1.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    eps = rng.normal(scale=sigma, size=n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + eps[t]
    return x


def _garch11(n: int, omega: float = 0.08, alpha: float = 0.12, beta: float = 0.82, seed: int = 20260520) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=n)
    h = np.empty(n)
    x = np.empty(n)
    h[0] = omega / (1.0 - alpha - beta)
    x[0] = np.sqrt(h[0]) * z[0]
    for t in range(1, n):
        h[t] = omega + alpha * x[t - 1] ** 2 + beta * h[t - 1]
        x[t] = np.sqrt(h[t]) * z[t]
    return x, h


def generate_chapter_figures(chapter: str, chapter_dir: str | Path) -> None:
    fig_dir = _fig_dir(chapter_dir)
    dispatch = {
        "ch02": _ch02,
        "ch03": _ch03,
        "ch04": _ch04,
        "ch05": _ch05,
        "ch06": _ch06,
        "ch07": _ch07,
        "ch08": _ch08,
        "ch09": _ch09,
        "ch10": _ch10,
        "ch11": _ch11,
        "ch12": _ch12,
        "ch13": _ch13,
        "ch14": _ch14,
        "ch15": _ch15,
        "appA": _app_a,
        "appB": _app_b,
    }
    dispatch[chapter](fig_dir)
    print(f"{chapter}: figures written to {fig_dir}")


def _ch02(fig_dir: Path) -> None:
    rng = np.random.default_rng(2)
    t = np.arange(240)
    trend = 0.015 * t + 0.00012 * (t - 120) ** 2
    seasonal = 1.2 * np.sin(2 * np.pi * t / 24)
    y = trend + seasonal + rng.normal(scale=0.45, size=t.size)
    coeff = np.polyfit(t, y, deg=2)
    fit = np.polyval(coeff, t)
    diff = np.diff(y)
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(t, y, color="#8aa0ad", linewidth=0.9, label="Observed")
    plt.plot(t, fit, color="#b0443c", linewidth=2.0, label="Quadratic trend")
    plt.title("Parametric Trend Estimation")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    _save(fig_dir, "ch02_fig01_parametric_trend.png")
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(t[1:], diff, color="#486b48", linewidth=1.0)
    plt.axhline(0, color="#444444", linestyle="--", linewidth=0.8)
    plt.title("First Difference Removes Slow Trend")
    plt.xlabel("Time")
    plt.ylabel("Difference")
    _save(fig_dir, "ch02_fig02_differencing.png")
    freqs, power = signal.periodogram(y - fit)
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(freqs[1:], power[1:], color="#5d4d8a")
    plt.title("Periodogram After Detrending")
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    _save(fig_dir, "ch02_fig03_periodogram.png")


def _ch03(fig_dir: Path) -> None:
    rng = np.random.default_rng(3)
    stationary = _ar1(0.65, 360, seed=3)
    random_walk = np.cumsum(rng.normal(size=360))
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(stationary, label="AR(1), phi=0.65", color="#2f5d7c")
    plt.plot(random_walk, label="Random walk", color="#b0443c", alpha=0.8)
    plt.title("Stationary Series Versus Random Walk")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    _save(fig_dir, "ch03_fig01_stationary_vs_random_walk.png")
    roll = pd.Series(stationary).rolling(40).mean()
    roll_rw = pd.Series(random_walk).rolling(40).mean()
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(roll, label="AR(1) rolling mean", color="#2f5d7c")
    plt.plot(roll_rw, label="Random walk rolling mean", color="#b0443c")
    plt.title("Rolling Mean Stability")
    plt.xlabel("Time")
    plt.ylabel("Rolling mean")
    plt.legend(frameon=False)
    _save(fig_dir, "ch03_fig02_rolling_mean.png")


def _ch04(fig_dir: Path) -> None:
    rng = np.random.default_rng(4)
    ar = np.array([1, -0.75, 0.25])
    ma = np.array([1, 0.55])
    process = ArmaProcess(ar, ma)
    y = process.generate_sample(nsample=400, distrvs=rng.normal)
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(y, color="#2f5d7c", linewidth=0.9)
    plt.title("Simulated ARMA(2,1) Series")
    plt.xlabel("Time")
    plt.ylabel("Value")
    _save(fig_dir, "ch04_fig01_arma_series.png")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    plot_acf(y, lags=30, ax=axes[0])
    plot_pacf(y, lags=30, method="ywm", ax=axes[1])
    axes[0].set_title("ACF")
    axes[1].set_title("PACF")
    _save(fig_dir, "ch04_fig02_acf_pacf.png")


def _ch05(fig_dir: Path) -> None:
    rng = np.random.default_rng(5)
    x1 = rng.normal(size=300)
    x2 = 0.75 * x1 + rng.normal(scale=0.65, size=300)
    y = 1.2 * x1 - 0.8 * x2 + rng.normal(scale=0.6, size=300)
    X = np.column_stack([np.ones_like(x1), x1, x2])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat = X @ beta
    plt.figure(figsize=(5.2, 5.0))
    plt.scatter(yhat, y, s=16, alpha=0.7, color="#2f5d7c")
    lim = [min(yhat.min(), y.min()), max(yhat.max(), y.max())]
    plt.plot(lim, lim, color="#b0443c", linewidth=1.5)
    plt.title("Projection View of Linear Prediction")
    plt.xlabel("Projection")
    plt.ylabel("Observed")
    _save(fig_dir, "ch05_fig01_projection_prediction.png")
    C = np.corrcoef(np.column_stack([y, x1, x2]).T)
    plt.figure(figsize=(4.8, 4.2))
    plt.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    plt.colorbar(label="Correlation")
    plt.xticks([0, 1, 2], ["Y", "X1", "X2"])
    plt.yticks([0, 1, 2], ["Y", "X1", "X2"])
    plt.title("Correlation Matrix")
    _save(fig_dir, "ch05_fig02_correlation_matrix.png")


def _ch06(fig_dir: Path) -> None:
    y_ar = _ar1(0.8, 500, seed=6)
    rng = np.random.default_rng(61)
    eps = rng.normal(size=501)
    y_ma = eps[1:] + 0.7 * eps[:-1]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    plot_acf(y_ar, lags=30, ax=axes[0])
    plot_acf(y_ma, lags=30, ax=axes[1])
    axes[0].set_title("AR(1) ACF")
    axes[1].set_title("MA(1) ACF")
    _save(fig_dir, "ch06_fig01_acf_shapes.png")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    plot_pacf(y_ar, lags=30, method="ywm", ax=axes[0])
    plot_pacf(y_ma, lags=30, method="ywm", ax=axes[1])
    axes[0].set_title("AR(1) PACF")
    axes[1].set_title("MA(1) PACF")
    _save(fig_dir, "ch06_fig02_pacf_shapes.png")


def _ch07(fig_dir: Path) -> None:
    y = _ar1(0.72, 180, seed=7)
    train = y[:140]
    horizon = 40
    phi, sigma = yule_walker(train, order=1)
    forecasts = np.empty(horizon)
    current = train[-1]
    for h in range(horizon):
        current = phi[0] * current
        forecasts[h] = current
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(np.arange(140), train, label="Training", color="#2f5d7c")
    plt.plot(np.arange(140, 180), y[140:], label="Held out", color="#9aa3aa")
    plt.plot(np.arange(140, 180), forecasts, label="Recursive forecast", color="#b0443c", linewidth=2)
    plt.title("AR(1) Recursive Forecast")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    _save(fig_dir, "ch07_fig01_ar_forecast.png")
    errors = y[140:] - forecasts
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(errors, color="#5d4d8a")
    plt.axhline(0, color="#444444", linestyle="--", linewidth=0.8)
    plt.title("Forecast Errors")
    plt.xlabel("Horizon")
    plt.ylabel("Error")
    _save(fig_dir, "ch07_fig02_forecast_errors.png")


def _ch08(fig_dir: Path) -> None:
    rng = np.random.default_rng(8)
    phis = [0.0, 0.4, 0.8]
    means = {}
    for phi in phis:
        means[phi] = [_ar1(phi, 180, seed=int(rng.integers(1, 1_000_000))).mean() for _ in range(700)]
    plt.figure(figsize=(7.2, 3.8))
    for phi, vals in means.items():
        plt.hist(vals, bins=35, density=True, alpha=0.45, label=f"phi={phi}")
    plt.title("Sampling Distribution of the Sample Mean")
    plt.xlabel("Sample mean")
    plt.ylabel("Density")
    plt.legend(frameon=False)
    _save(fig_dir, "ch08_fig01_sample_mean_dependence.png")
    y = _ar1(0.75, 400, seed=88)
    rho = acf(y, nlags=30, fft=True)
    plt.figure(figsize=(7.2, 3.8))
    plt.stem(range(len(rho)), rho)
    plt.title("Sample Autocorrelation")
    plt.xlabel("Lag")
    plt.ylabel("ACF")
    _save(fig_dir, "ch08_fig02_sample_acf.png")


def _ch09(fig_dir: Path) -> None:
    rng = np.random.default_rng(9)
    true_phi = 0.72
    estimates = []
    for _ in range(600):
        y = _ar1(true_phi, 160, seed=int(rng.integers(1, 1_000_000)))
        estimates.append(yule_walker(y, order=1)[0][0])
    plt.figure(figsize=(7.2, 3.8))
    plt.hist(estimates, bins=35, density=True, color="#7a4b8f", alpha=0.75)
    plt.axvline(true_phi, color="#b0443c", linewidth=2, label="True phi")
    plt.title("Sampling Distribution of Yule-Walker AR(1) Estimate")
    plt.xlabel("Estimate")
    plt.ylabel("Density")
    plt.legend(frameon=False)
    _save(fig_dir, "ch09_fig01_yule_walker_sampling.png")
    y = _ar1(true_phi, 220, seed=99)
    x = y[:-1]
    target = y[1:]
    slope = np.linalg.lstsq(x[:, None], target, rcond=None)[0][0]
    plt.figure(figsize=(5.2, 5.0))
    plt.scatter(x, target, s=16, alpha=0.65, color="#2f5d7c")
    xx = np.linspace(x.min(), x.max(), 100)
    plt.plot(xx, slope * xx, color="#b0443c", linewidth=2)
    plt.title("Conditional Least Squares for AR(1)")
    plt.xlabel("X[t-1]")
    plt.ylabel("X[t]")
    _save(fig_dir, "ch09_fig02_cls_ar1.png")


def _ch10(fig_dir: Path) -> None:
    w = np.linspace(0, np.pi, 600)
    phi = 0.85
    theta = 0.65
    ar_spec = 1 / np.abs(1 - phi * np.exp(-1j * w)) ** 2
    ma_spec = np.abs(1 + theta * np.exp(-1j * w)) ** 2
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(w, ar_spec / ar_spec.max(), label="AR(1)", color="#2f5d7c")
    plt.plot(w, ma_spec / ma_spec.max(), label="MA(1)", color="#b0443c")
    plt.title("Normalized Spectral Densities")
    plt.xlabel("Frequency")
    plt.ylabel("Relative density")
    plt.legend(frameon=False)
    _save(fig_dir, "ch10_fig01_spectral_density.png")
    y = _ar1(0.85, 512, seed=10)
    fy = np.fft.rfft(y - y.mean())
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(np.fft.rfftfreq(len(y))[1:], np.abs(fy[1:]) ** 2 / len(y), color="#5d4d8a")
    plt.title("DFT Energy of an AR(1) Series")
    plt.xlabel("Frequency")
    plt.ylabel("Periodogram")
    _save(fig_dir, "ch10_fig02_dft_energy.png")


def _ch11(fig_dir: Path) -> None:
    rng = np.random.default_rng(11)
    t = np.arange(512)
    y = 1.4 * np.sin(2 * np.pi * t / 32) + 0.9 * np.sin(2 * np.pi * t / 80) + rng.normal(scale=0.7, size=t.size)
    freqs, power = signal.periodogram(y)
    smooth = pd.Series(power).rolling(9, center=True, min_periods=1).mean()
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(freqs[1:], power[1:], color="#9aa3aa", label="Periodogram")
    plt.plot(freqs[1:], smooth[1:], color="#b0443c", linewidth=2, label="Smoothed")
    plt.title("Periodogram Smoothing")
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.legend(frameon=False)
    _save(fig_dir, "ch11_fig01_smoothed_periodogram.png")
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(t, y, color="#2f5d7c", linewidth=0.9)
    plt.title("Signal with Two Periodic Components")
    plt.xlabel("Time")
    plt.ylabel("Value")
    _save(fig_dir, "ch11_fig02_two_frequency_signal.png")


def _ch12(fig_dir: Path) -> None:
    rng = np.random.default_rng(12)
    n = 420
    x = np.zeros((n, 2))
    eps = rng.normal(size=(n, 2))
    A = np.array([[0.55, 0.25], [-0.15, 0.45]])
    for t in range(1, n):
        x[t] = A @ x[t - 1] + eps[t]
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(x[:, 0], label="Series 1", color="#2f5d7c")
    plt.plot(x[:, 1], label="Series 2", color="#b0443c", alpha=0.85)
    plt.title("Simulated Bivariate VAR(1)")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    _save(fig_dir, "ch12_fig01_var_series.png")
    f, cxy = signal.coherence(x[:, 0], x[:, 1], nperseg=96)
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(f, cxy, color="#5d4d8a")
    plt.ylim(0, 1)
    plt.title("Magnitude-Squared Coherence")
    plt.xlabel("Frequency")
    plt.ylabel("Coherence")
    _save(fig_dir, "ch12_fig02_coherence.png")


def _ch13(fig_dir: Path) -> None:
    x, h = _garch11(600, seed=13)
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(x, color="#2f5d7c", linewidth=0.8)
    plt.title("Simulated GARCH(1,1) Returns")
    plt.xlabel("Time")
    plt.ylabel("Return")
    _save(fig_dir, "ch13_fig01_garch_returns.png")
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(np.sqrt(h), color="#b0443c", linewidth=1.2)
    plt.title("Conditional Volatility")
    plt.xlabel("Time")
    plt.ylabel("Sigma[t]")
    _save(fig_dir, "ch13_fig02_conditional_volatility.png")


def _ch14(fig_dir: Path) -> None:
    rng = np.random.default_rng(14)
    ns = np.array([40, 80, 160, 320, 640, 1280])
    mse = []
    for n in ns:
        vals = [_ar1(0.55, int(n), seed=int(rng.integers(1, 1_000_000))).mean() for _ in range(500)]
        mse.append(np.mean(np.square(vals)))
    plt.figure(figsize=(7.2, 3.8))
    plt.loglog(ns, mse, marker="o", color="#2f5d7c")
    plt.title("Consistency: MSE of the Sample Mean")
    plt.xlabel("Sample size")
    plt.ylabel("Mean squared error")
    _save(fig_dir, "ch14_fig01_consistency_mse.png")
    vals = [_ar1(0.45, 500, seed=int(rng.integers(1, 1_000_000))).mean() * np.sqrt(500) for _ in range(1200)]
    plt.figure(figsize=(7.2, 3.8))
    plt.hist(vals, bins=40, density=True, alpha=0.7, color="#7a4b8f", label="Simulation")
    xs = np.linspace(min(vals), max(vals), 250)
    plt.plot(xs, stats.norm.pdf(xs, np.mean(vals), np.std(vals)), color="#b0443c", linewidth=2, label="Normal fit")
    plt.title("Asymptotic Normality Illustration")
    plt.xlabel("sqrt(n) * sample mean")
    plt.ylabel("Density")
    plt.legend(frameon=False)
    _save(fig_dir, "ch14_fig02_asymptotic_normality.png")


def _ch15(fig_dir: Path) -> None:
    rng = np.random.default_rng(15)
    y = _ar1(0.68, 220, seed=15)
    phi_hat = np.linalg.lstsq(y[:-1, None], y[1:], rcond=None)[0][0]
    resid = y[1:] - phi_hat * y[:-1]
    boot = []
    for _ in range(600):
        e = rng.choice(resid - resid.mean(), size=len(y) - 1, replace=True)
        z = np.zeros_like(y)
        z[0] = y[0]
        for t in range(1, len(y)):
            z[t] = phi_hat * z[t - 1] + e[t - 1]
        boot.append(np.linalg.lstsq(z[:-1, None], z[1:], rcond=None)[0][0])
    plt.figure(figsize=(7.2, 3.8))
    plt.hist(boot, bins=35, density=True, color="#2f5d7c", alpha=0.75)
    plt.axvline(phi_hat, color="#b0443c", linewidth=2, label="Original estimate")
    plt.title("Residual Bootstrap for AR(1)")
    plt.xlabel("Bootstrap estimate")
    plt.ylabel("Density")
    plt.legend(frameon=False)
    _save(fig_dir, "ch15_fig01_residual_bootstrap.png")
    plt.figure(figsize=(7.2, 3.8))
    plt.scatter(phi_hat * y[:-1], resid, s=16, alpha=0.65, color="#5d4d8a")
    plt.axhline(0, color="#444444", linestyle="--", linewidth=0.8)
    plt.title("AR(1) Residuals")
    plt.xlabel("Fitted")
    plt.ylabel("Residual")
    _save(fig_dir, "ch15_fig02_residuals.png")


def _app_a(fig_dir: Path) -> None:
    x = np.linspace(-np.pi, np.pi, 600)
    target = np.where(x >= 0, 1.0, -1.0)
    approx = np.zeros_like(x)
    for k in range(1, 20, 2):
        approx += 4 / np.pi * np.sin(k * x) / k
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(x, target, color="#9aa3aa", label="Square wave")
    plt.plot(x, approx, color="#b0443c", linewidth=2, label="Fourier partial sum")
    plt.title("Fourier Series Approximation")
    plt.xlabel("x")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    _save(fig_dir, "appA_fig01_fourier_series.png")
    rng = np.random.default_rng(101)
    y = np.sin(2 * np.pi * np.arange(256) / 32) + rng.normal(scale=0.35, size=256)
    spec = np.abs(np.fft.rfft(y)) ** 2
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(np.fft.rfftfreq(len(y)), spec, color="#2f5d7c")
    plt.title("Fast Fourier Transform Energy")
    plt.xlabel("Frequency")
    plt.ylabel("Energy")
    _save(fig_dir, "appA_fig02_fft_energy.png")


def _app_b(fig_dir: Path) -> None:
    lags = np.arange(0, 60)
    curves = {
        "geometric": 0.85 ** lags,
        "polynomial": (1 + lags) ** -1.2,
    }
    plt.figure(figsize=(7.2, 3.8))
    for label, values in curves.items():
        plt.plot(lags, values, marker="o", markersize=2.5, label=label)
    plt.yscale("log")
    plt.title("Dependence Decay Rates")
    plt.xlabel("Lag")
    plt.ylabel("Dependence measure")
    plt.legend(frameon=False)
    _save(fig_dir, "appB_fig01_dependence_decay.png")
    x = _ar1(0.7, 400, seed=202)
    y = x.copy()
    y[0] += 8.0
    influence = np.abs(y - x)
    for t in range(1, len(y)):
        influence[t] = abs(0.7 * influence[t - 1])
    plt.figure(figsize=(7.2, 3.8))
    plt.plot(influence[:80], color="#b0443c")
    plt.title("Physical Dependence Illustration")
    plt.xlabel("Time after perturbation")
    plt.ylabel("Perturbation size")
    _save(fig_dir, "appB_fig02_physical_dependence.png")
