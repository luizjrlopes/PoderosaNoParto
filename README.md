# Poderosa no Parto

Aplicação web (React) e conjunto de experimentos de IA focados em apoiar pessoas gestantes durante o pré-natal com conteúdos personalizados, monitoramento de tarefas e recomendações baseadas em dados clínicos e de engajamento.

## Objetivo do Repositório
- Manter o front-end do protótipo (SPA em `src/`).
- Documentar a arquitetura, fluxos MLOps/LLMOps e estudos de caso que embasam as funcionalidades inteligentes.
- Versionar notebooks e requisitos necessários para reproduzir análises, modelos e automações.

## Projetos e Notebooks Principais
| Item | Descrição | Resultados |
|------|-----------|-----------|
| **Aplicativo Web (React)** | Interface responsiva com agenda de tarefas, trilhas educativas, player de áudio e gráficos de progresso. | Deploy em Heroku/Netlify; integrações prontas para APIs `/recommendations` e `/risk-score`. |
| `notebooks/01-birth-plan-analysis/` | Clustering de planos de parto para mapear lacunas de conteúdo. | Cobertura de temas críticos saltou de 68% para 94%; gera `recommended_curriculum.json`. |
| `notebooks/02-risk-stratification-model/` | Modelo Gradient Boosting para risco obstétrico com dados SIP. | AUC 0.84 / F1 0.79; registra artefatos no MLflow. |
| `notebooks/03-engagement-forecast/` | Previsão de engajamento e recomendação de nudges/LLM. | MAE 0.07 e recall@5 0.76; produz `at_risk_users.parquet` e `recommended_nudges.json`. |

Consulte `docs/case-studies.md` para detalhes de datasets, métricas e insights.

## Setup e Execução do Front-end
### Pré-requisitos
- Node.js 18+ e npm 9+
- Variáveis de ambiente (crie `.env` na raiz se precisar customizar `REACT_APP_API_BASE_URL`).

### Passos
1. Instale as dependências: `npm install`
2. (Opcional) Configure o endpoint das APIs no arquivo `.env`.
3. Inicie em modo desenvolvimento: `npm start`
4. Execute testes automatizados: `npm test`
5. Gere o build estático para deploy: `npm run build`

## Ambiente de Notebooks
- Cada pasta dentro de `notebooks/` contém um `README.md` e um `requirements.txt` específicos.
- Utilize Python 3.10+ e crie ambientes virtuais independentes (`python -m venv .venv`).
- Rode os notebooks manualmente (Jupyter Lab) ou via Papermill/GitHub Actions seguindo `docs/mlops-llmops.md`.

## Documentação Relacionada
- `docs/project-overview.md`: contexto histórico e objetivos.
- `docs/architecture.md`: visão detalhada de componentes e fluxos de dados.
- `docs/mlops-llmops.md`: pipelines de dados, treinamento, deploy e governança de prompts.
- `docs/case-studies.md`: experiências conduzidas, datasets e métricas.

## Estrutura de Diretórios
- `src/`: código React.
- `public/`: ativos estáticos.
- `docs/`: documentação de arquitetura, operações e estudos.
- `notebooks/`: experimentos e pipelines de dados.
- `models/`: artefatos treinados (quando publicados).
- `scripts/`: automações auxiliares.
- `tests/`: utilitários de teste.
