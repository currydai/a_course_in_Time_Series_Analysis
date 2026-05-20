"""Generate figures for Chapter 1.

The script uses reproducible synthetic data for introductory examples and the
built-in statsmodels sunspots dataset for a real periodic time series.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.datasets import sunspots


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=180)
    plt.close()


def white_noise(seed: int = 20260520) -> None:
    rng = np.random.default_rng(seed)
    n = 220
    y = rng.normal(loc=0.0, scale=1.0, size=n)

    plt.figure(figsize=(7.2, 3.6))
    plt.plot(np.arange(n), y, color="#2f5d7c", linewidth=1.1)
    plt.axhline(0, color="#444444", linewidth=0.8, linestyle="--")
    plt.title("Independent Uncorrelated Random Variables")
    plt.xlabel("Time")
    plt.ylabel("Value")
    savefig("ch01_fig01_white_noise.png")


def simulated_soi(seed: int = 20260520) -> None:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("1876-01-01", periods=12 * 139 + 7, freq="MS")
    t = np.arange(len(dates))
    seasonal = 0.55 * np.sin(2 * np.pi * t / 48) + 0.35 * np.sin(2 * np.pi * t / 62)
    persistence = np.zeros_like(seasonal)
    noise = rng.normal(scale=0.55, size=len(t))
    for i in range(1, len(t)):
        persistence[i] = 0.82 * persistence[i - 1] + noise[i]
    soi = seasonal + 0.45 * persistence

    plt.figure(figsize=(7.2, 3.6))
    plt.plot(dates, soi, color="#5c6f2f", linewidth=0.75)
    plt.title("Simulated Monthly SOI-like Series")
    plt.xlabel("Year")
    plt.ylabel("Index")
    savefig("ch01_fig02_simulated_soi.png")


def sunspot_series() -> None:
    data = sunspots.load_pandas().data
    data = data[(data["YEAR"] >= 1700) & (data["YEAR"] <= 2013)]

    plt.figure(figsize=(7.2, 3.6))
    plt.plot(data["YEAR"], data["SUNACTIVITY"], color="#7a4b8f", linewidth=0.9)
    plt.title("Yearly Sunspot Numbers")
    plt.xlabel("Year")
    plt.ylabel("Sunspots")
    savefig("ch01_fig03_sunspots.png")


def filtering_example(seed: int = 20260520) -> None:
    rng = np.random.default_rng(seed)
    n = 240
    t = np.arange(n)
    trend = 0.015 * t
    signal = trend + np.sin(2 * np.pi * t / 36)
    observed = signal + rng.normal(scale=0.55, size=n)
    smoothed = pd.Series(observed).rolling(window=13, center=True, min_periods=1).mean()

    plt.figure(figsize=(7.2, 3.6))
    plt.plot(t, observed, color="#9aa3aa", linewidth=0.8, label="Observed")
    plt.plot(t, smoothed, color="#b0443c", linewidth=2.0, label="13-point moving average")
    plt.title("Linear Filtering with a Moving Average")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(frameon=False)
    savefig("ch01_fig04_filtering.png")


def main() -> None:
    white_noise()
    simulated_soi()
    sunspot_series()
    filtering_example()
    print(f"Figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()

