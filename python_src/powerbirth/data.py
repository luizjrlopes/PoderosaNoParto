"""Geração de dados sintéticos representando pacientes em pré-natal."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd

DEFAULT_NUM_SAMPLES = 256


@dataclass
class SyntheticDatasetMetadata:
    """Metadados básicos retornados junto com o DataFrame."""

    num_samples: int
    positive_rate: float
    random_state: int


def _simulate_risk_signal(df: pd.DataFrame) -> np.ndarray:
    """Combina features para criar uma pontuação de risco contínua."""

    base = (
        0.04 * (df["age"] - 25)
        + 0.03 * (df["systolic_bp"] - 110)
        + 0.02 * (df["bmi"] - 23)
        + 0.4 * df["previous_c_sections"]
        + 0.7 * df["chronic_hypertension"].astype(int)
        + 0.5 * df["gestational_diabetes"].astype(int)
        + 0.3 * (1 - df["prenatal_education_completed"])
        + 0.02 * (df["gestational_weeks"] - 28)
    )
    noise = np.random.default_rng().normal(0, 0.5, size=len(df))
    return base + noise


def generate_synthetic_patient_data(
    num_samples: int = DEFAULT_NUM_SAMPLES,
    *,
    random_state: int = 42,
    return_metadata: bool = False,
) -> Dict[str, object] | pd.DataFrame:
    """Cria um DataFrame com variáveis clínicas e rótulo binário de risco."""

    rng = np.random.default_rng(random_state)

    ages = rng.integers(18, 45, size=num_samples)
    gest_weeks = rng.integers(24, 41, size=num_samples)
    systolic = rng.normal(118, 12, size=num_samples).round(1)
    diastolic = rng.normal(75, 8, size=num_samples).round(1)
    bmi = rng.normal(26, 4, size=num_samples).round(1)
    c_sections = rng.poisson(0.3, size=num_samples)
    prenatal_ed = rng.integers(0, 2, size=num_samples)
    chronic_htn = rng.integers(0, 2, size=num_samples)
    gest_diabetes = rng.integers(0, 2, size=num_samples)

    df = pd.DataFrame(
        {
            "age": ages,
            "gestational_weeks": gest_weeks,
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "bmi": bmi,
            "previous_c_sections": c_sections,
            "prenatal_education_completed": prenatal_ed,
            "chronic_hypertension": chronic_htn,
            "gestational_diabetes": gest_diabetes,
        }
    )

    signal = _simulate_risk_signal(df)
    threshold = signal.mean()
    df["high_risk_label"] = (signal > threshold).astype(int)

    if not return_metadata:
        return df

    metadata = SyntheticDatasetMetadata(
        num_samples=num_samples,
        positive_rate=float(df["high_risk_label"].mean()),
        random_state=random_state,
    )
    return {"data": df, "metadata": metadata}
