# Notebook: Risk Stratification Model

## Contexto
Modela o risco obstétrico (alto vs. baixo) usando variáveis clínicas extraídas do Sistema de Informações Perinatais (SIP) e dados coletados via aplicativo. O objetivo é antecipar casos que necessitam de acompanhamento intensivo.

## Dados Utilizados
- `data/raw/sip_records.parquet`: base pública do Ministério da Saúde com dados anonimizados.
- `data/processed/risk_features.parquet`: dataset enriquecido com variáveis derivadas (idade gestacional, histórico de pressão, IMC).

## Dependências
```
pip install -r requirements.txt
```
Inclui pandas, numpy, scikit-learn, lightgbm, imbalanced-learn, shap e mlflow.

## Como Reproduzir
1. `cd notebooks/02-risk-stratification-model`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Posicione os arquivos em `data/raw/` e `data/processed/` conforme descrito.
5. Execute `risk_stratification.ipynb` ou rode `papermill risk_stratification.ipynb output.ipynb -p experiment_name production`.

## Resultados Esperados
- Métricas médias (5-fold): AUC 0.84, F1 0.79, sensibilidade 0.81.
- Gráficos SHAP e matriz de confusão salvos em `artifacts/`.
- Registro do modelo no MLflow com tag `Production` quando supera o baseline.
