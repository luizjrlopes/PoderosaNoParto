#!/usr/bin/env python3
"""Executa uma pipeline sintética de risco obstétrico ponta a ponta."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "python_src"))

DEFAULT_OUTPUT = PROJECT_ROOT / "models" / "synthetic_inference_results.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--num-training-samples",
        type=int,
        default=512,
        help="Quantidade de linhas sintéticas para treinar o modelo.",
    )
    parser.add_argument(
        "--num-inference-samples",
        type=int,
        default=32,
        help="Quantidade de registros gerados apenas para inferência.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Arquivo JSON onde os resultados serão salvos.",
    )
    return parser.parse_args()


def main() -> None:
    from powerbirth import generate_synthetic_patient_data, run_batch_inference, train_risk_model

    args = parse_args()

    dataset = generate_synthetic_patient_data(num_samples=args.num_training_samples)
    artifacts = train_risk_model(dataset)

    inference_records = generate_synthetic_patient_data(num_samples=args.num_inference_samples)
    inference_records = inference_records.drop(columns=["high_risk_label"])
    scored = run_batch_inference(artifacts.model, inference_records)

    summary = {
        "auc": artifacts.auc,
        "positive_rate": artifacts.positive_rate,
        "num_predictions": len(scored),
        "high_risk_fraction": float((scored["risk_bucket"] == "high").mean()),
    }

    payload = {
        "summary": summary,
        "predictions": scored.round(3).to_dict(orient="records"),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2))

    print("Resumo da execução:")
    print(json.dumps(summary, indent=2))
    print(f"Predições salvas em {args.output}")


if __name__ == "__main__":
    main()
