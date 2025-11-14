"""Gera gráficos de desempenho para os experimentos documentados em docs/model-performance.md."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_risk_stratification(out_dir: Path) -> None:
    models = ["Regressão Logística", "Gradient Boosting", "Transformer Clínico"]
    metrics = {
        "Precisão": np.array([0.71, 0.79, 0.83]),
        "Recall": np.array([0.79, 0.84, 0.88]),
        "F1": np.array([0.74, 0.81, 0.85]),
    }
    x = np.arange(len(models))
    width = 0.25
    plt.figure(figsize=(9, 5))
    for idx, (label, values) in enumerate(metrics.items()):
        plt.bar(x + (idx - 1) * width, values, width, label=label)
    plt.xticks(x, models, rotation=10)
    plt.ylabel("Pontuação")
    plt.ylim(0.6, 0.95)
    plt.title("Comparativo do modelo de estratificação de risco materno")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(out_dir / "risk-stratification-metrics.png", dpi=200)
    plt.close()


def plot_engagement_forecast(out_dir: Path) -> None:
    weeks = np.array([20, 24, 28, 32, 36, 40])
    rmse = {
        "Prophet baseline": np.array([10.4, 10.1, 10.2, 10.6, 11.1, 11.5]),
        "Seq2Seq LSTM": np.array([8.6, 8.2, 8.4, 8.9, 9.3, 9.8]),
        "Temporal Transformer": np.array([7.4, 7.2, 7.3, 7.7, 8.1, 8.5]),
    }
    plt.figure(figsize=(8, 5))
    for label, values in rmse.items():
        plt.plot(weeks, values, marker="o", label=label)
    plt.xlabel("Semana gestacional prevista")
    plt.ylabel("RMSE de engajamento (pts)")
    plt.title("Erro médio quadrático por horizonte de previsão")
    plt.grid(alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "engagement-forecast-rmse.png", dpi=200)
    plt.close()


def main() -> None:
    out_dir = Path("docs/img")
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_risk_stratification(out_dir)
    plot_engagement_forecast(out_dir)
    print(f"Gráficos salvos em {out_dir.resolve()}")


if __name__ == "__main__":
    main()
