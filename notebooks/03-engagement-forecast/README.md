# Notebook: Engagement Forecast & Recommendations

## Contexto
Modela a probabilidade de queda de engajamento semanal (ex.: abandono das tarefas) e gera recomendações de conteúdos/LLM para reengajar gestantes.

## Dados Utilizados
- `data/raw/engagement_events.parquet`: eventos de uso (login, tarefas, player de áudio) agregados por usuária.
- `data/processed/weekly_engagement.parquet`: features agregadas (dias sem login, conclusão média, interação com LLM).

## Dependências
```
pip install -r requirements.txt
```
Inclui pandas, numpy, prophet, lightgbm, scikit-learn, plotly, mlflow e evidently.

## Como Reproduzir
1. `cd notebooks/03-engagement-forecast`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Gere as tabelas agregadas executando `python ../../scripts/prepare_engagement_features.py` (descrição no roadmap) ou carregue do data lake.
5. Execute `engagement_forecast.ipynb` e exporte as previsões com `papermill engagement_forecast.ipynb output.ipynb -p horizon_weeks 4`.

## Resultados Esperados
- MAE ~0.07 para previsão da taxa semanal de conclusão.
- Tabela `at_risk_users.parquet` com probabilidade > 0.4 de queda.
- Lista `recommended_nudges.json` alimentando o fluxo de notificações e mensagens de assistente.
