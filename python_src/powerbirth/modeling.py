"""Funções de treinamento e inferência para o modelo sintético de risco."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "age",
    "gestational_weeks",
    "systolic_bp",
    "diastolic_bp",
    "bmi",
    "previous_c_sections",
]
CATEGORICAL_FEATURES = [
    "prenatal_education_completed",
    "chronic_hypertension",
    "gestational_diabetes",
]
TARGET_COLUMN = "high_risk_label"


@dataclass
class RiskModelArtifacts:
    """Agrupa objetos importantes após o treinamento."""

    model: Pipeline
    auc: float
    positive_rate: float


def _build_pipeline() -> Pipeline:
    transformers = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    estimator = LogisticRegression(max_iter=1000, solver="lbfgs")
    return Pipeline(steps=[("features", transformers), ("clf", estimator)])


def train_risk_model(
    dataset: pd.DataFrame,
    *,
    random_state: int = 42,
    test_size: float = 0.25,
) -> RiskModelArtifacts:
    """Treina o pipeline logístico usando dados sintéticos."""

    missing_columns = {TARGET_COLUMN} - set(dataset.columns)
    if missing_columns:
        raise ValueError(f"Colunas ausentes no dataset: {missing_columns}")

    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    x_train, x_test, y_train, y_test = train_test_split(
        dataset[feature_columns],
        dataset[TARGET_COLUMN],
        test_size=test_size,
        random_state=random_state,
        stratify=dataset[TARGET_COLUMN],
    )

    pipeline = _build_pipeline()
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict_proba(x_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)

    return RiskModelArtifacts(
        model=pipeline,
        auc=float(auc),
        positive_rate=float(dataset[TARGET_COLUMN].mean()),
    )


def run_batch_inference(
    model: Pipeline,
    new_records: pd.DataFrame,
    *,
    risk_threshold: float = 0.5,
) -> pd.DataFrame:
    """Gera probabilidades e buckets de risco para novos registros."""

    required_columns = set(NUMERIC_FEATURES + CATEGORICAL_FEATURES)
    missing_columns = required_columns - set(new_records.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas ausentes no dataset de inferência: {missing}")

    probabilities = model.predict_proba(new_records)[:, 1]
    result = new_records.copy()
    result["risk_score"] = probabilities
    result["risk_bucket"] = result["risk_score"].apply(
        lambda score: "high" if score >= risk_threshold else "low"
    )
    return result


def top_features() -> Iterable[str]:
    """Expõe as colunas mais influentes para documentação e dashboards."""

    return [
        "systolic_bp",
        "diastolic_bp",
        "bmi",
        "chronic_hypertension",
        "gestational_diabetes",
    ]
