"""Testes mínimos para o pacote `powerbirth`."""

from __future__ import annotations

from powerbirth import generate_synthetic_patient_data, run_batch_inference, train_risk_model


def test_generate_synthetic_patient_data_shape_and_ranges():
    dataset = generate_synthetic_patient_data(num_samples=64, random_state=123)

    assert dataset.shape == (64, 10)
    assert dataset["age"].between(18, 44).all()
    assert dataset["high_risk_label"].isin({0, 1}).all()
    assert 0.2 < dataset["high_risk_label"].mean() < 0.8


def test_training_pipeline_returns_metrics_above_baseline():
    dataset = generate_synthetic_patient_data(num_samples=200, random_state=321)
    artifacts = train_risk_model(dataset)

    assert 0.7 <= artifacts.auc <= 1.0
    assert 0 < artifacts.positive_rate < 1


def test_run_batch_inference_generates_scores_sorted_by_bucket():
    dataset = generate_synthetic_patient_data(num_samples=150, random_state=999)
    artifacts = train_risk_model(dataset)
    new_records = dataset.drop(columns=["high_risk_label"]).sample(10, random_state=7)

    scored = run_batch_inference(artifacts.model, new_records, risk_threshold=0.55)

    assert {"risk_score", "risk_bucket"}.issubset(scored.columns)
    assert scored["risk_score"].between(0, 1).all()
    assert set(scored["risk_bucket"].unique()).issubset({"low", "high"})

    high_scores = scored.loc[scored["risk_bucket"] == "high", "risk_score"]
    low_scores = scored.loc[scored["risk_bucket"] == "low", "risk_score"]
    if not high_scores.empty and not low_scores.empty:
        assert high_scores.min() >= low_scores.max()
