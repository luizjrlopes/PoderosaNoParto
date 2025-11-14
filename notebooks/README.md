# Notebooks

Este diretório agrupa estudos exploratórios e pipelines executados via Papermill/GitHub Actions. Cada subpasta contém um `README.md` com contexto, datasets e instruções para reprodução local.

## Organização Atual
| Pasta | Objetivo | Principais Resultados |
|-------|----------|-----------------------|
| `01-birth-plan-analysis/` | Mapear lacunas no conteúdo educativo a partir de planos de parto reais. | Aumentou a cobertura de temas críticos de 68% para 94% e gerou `recommended_curriculum.json`. |
| `02-risk-stratification-model/` | Prever risco obstétrico alto usando dados clínicos do SIP e do app. | AUC 0.84 / F1 0.79; modelo registrado no MLflow com tag `Production`. |
| `03-engagement-forecast/` | Antecipar queda de engajamento semanal e sugerir nudges/LLM. | MAE 0.07 e recall@5 0.76 para recomendações personalizadas. |

## Ambiente de Execução
1. Garanta Python 3.10+ e Jupyter Lab instalados.
2. Dentro de cada pasta, crie um ambiente virtual (`python -m venv .venv`).
3. Instale as dependências específicas via `pip install -r requirements.txt`.
4. Posicione os datasets nas rotas descritas e execute o notebook manualmente ou com Papermill.

Para detalhes sobre automação e integração com pipelines, consulte `docs/mlops-llmops.md`.
