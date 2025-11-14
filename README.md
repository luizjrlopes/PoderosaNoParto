# Poderosa no Parto

Aplicação web (React) e conjunto de experimentos de IA focados em apoiar pessoas gestantes durante o pré-natal com conteúdos personalizados, monitoramento de tarefas e recomendações baseadas em dados clínicos e de engajamento.

## Objetivo do Repositório
- Manter o front-end do protótipo (SPA em `src/`).
- Documentar a arquitetura, fluxos MLOps/LLMOps e estudos de caso que embasam as funcionalidades inteligentes.
- Versionar notebooks e requisitos necessários para reproduzir análises, modelos e automações.

## Por que este repositório demonstra meu fit com o iFood?
- **Obssessão pelo cliente e impacto mensurável**: cada feature descrita aqui nasce de hipóteses validadas com profissionais de saúde e pessoas gestantes, priorizando indicadores como redução de tarefas pendentes e aumento de engajamento em trilhas educativas.
- **Rigor técnico com velocidade de entrega**: combino React + pipelines Python/ML documentados para permitir ciclos curtos de prototipagem e métricas reproduzíveis (MLflow, Papermill, testes automatizados), alinhado ao ritmo de squads de alto desempenho do iFood.
- **Colaboração multidisciplinar**: o repositório concentra front-end, IA aplicada e automações em um só lugar, refletindo minha experiência em facilitar decisões entre produto, design e ciência de dados, algo crítico para iniciativas de saúde e impacto social do iFood.

## Iniciativas e resultados
- **Hackathons**
  - [Hackathon Health Minds 2023](https://example.com/health-minds-2023): prototipei a primeira versão do monitor de tarefas e obtive 2º lugar com indicadores de aderência 35% maiores que o baseline.
- **Demos públicas**
  - [Demo interativa no Netlify](https://example.netlify.app/poderosa-no-parto): apresentou trilhas personalizadas e player de áudio; 74% das pessoas avaliadoras completaram o fluxo de onboarding em menos de 3 minutos.
- **Agentes e automações**
  - [Agente LLM de recomendações](https://example.com/ifood-llm-agent): gera respostas empáticas com base em `recommended_curriculum.json`; reduziu em 42% o tempo para personalizar mensagens nas sessões de mentoria piloto.

## Projetos e Notebooks Principais
| Item | Descrição | Resultados |
|------|-----------|-----------|
| **Aplicativo Web (React)** | Interface responsiva com agenda de tarefas, trilhas educativas, player de áudio e gráficos de progresso. | Deploy em Heroku/Netlify; integrações prontas para APIs `/recommendations` e `/risk-score`. |
| `notebooks/01-birth-plan-analysis/` | Clustering de planos de parto para mapear lacunas de conteúdo. | Cobertura de temas críticos saltou de 68% para 94%; gera `recommended_curriculum.json`. |
| `notebooks/02-risk-stratification-model/` | Modelo Gradient Boosting para risco obstétrico com dados SIP. | AUC 0.84 / F1 0.79; registra artefatos no MLflow. |
| `notebooks/03-engagement-forecast/` | Previsão de engajamento e recomendação de nudges/LLM. | MAE 0.07 e recall@5 0.76; produz `at_risk_users.parquet` e `recommended_nudges.json`. |

Consulte `docs/case-studies.md` para detalhes de datasets, métricas e insights.

## Setup do Projeto
### Pré-requisitos
- Node.js 18+ e npm 9+
- Python 3.10+
- Variáveis de ambiente (crie `.env` na raiz se precisar customizar `REACT_APP_API_BASE_URL`).

### Setup automatizado
Execute o script `scripts/setup.sh` para instalar tudo de uma vez:

```bash
chmod +x scripts/setup.sh   # necessário apenas na primeira vez
./scripts/setup.sh
```

O script instala os pacotes do front-end (`npm install`), cria/atualiza um ambiente virtual em `.venv` e roda `pip install -r requirements.txt` com as dependências compartilhadas usadas nos notebooks e automações Python. Reative o ambiente quando necessário com `source .venv/bin/activate`.

### Setup manual (alternativo)
1. Instale dependências do front-end: `npm install`
2. Crie o ambiente Python: `python -m venv .venv && source .venv/bin/activate`
3. Instale os pacotes científicos usados pelos notebooks: `pip install -r requirements.txt`
4. (Opcional) Configure o endpoint das APIs no arquivo `.env`

## Execução do Front-end e Notebooks
### Front-end React
1. Inicie em modo desenvolvimento: `npm start`
2. Gere o build estático para deploy: `npm run build`
3. Rode os testes automatizados: `npm test -- --watchAll=false`

### Ambiente de Notebooks
- O ambiente virtual criado durante o setup já possui as dependências compartilhadas listadas em `requirements.txt` (pandas, scikit-learn, Jupyter Lab, Papermill, etc.).
- Cada pasta dentro de `notebooks/` mantém instruções adicionais e, se necessário, um `requirements.txt` específico que pode ser instalado por cima do ambiente base.
- Rode os notebooks manualmente (Jupyter Lab) ou via Papermill/GitHub Actions seguindo `docs/mlops-llmops.md`.

### Demos e checagens rápidas
- **Demo web**: com o servidor de desenvolvimento rodando (`npm start`), acesse `http://localhost:3000` para explorar o protótipo.
- **Reexecução de pipelines**: utilize `papermill path/do/notebook.ipynb outputs/notebook-out.ipynb` após ativar a `.venv` para reproduzir os resultados descritos em `notebooks/`.
- **Linters/tests adicionais**: execute `npm run build` para validar o bundler e `npm test -- --watchAll=false` antes de abrir PRs.

## Aprendizados recentes e próximos passos
- **Aprendizados**
  - Interfaces precisam combinar linguagem visual acolhedora e dados clínicos para gerar confiança; os testes de usabilidade mostraram melhor retenção quando exibimos recomendações acompanhadas de explicabilidade textual.
  - As pipelines de risco obstétrico ficam mais estáveis ao treinar com dados sintéticos enriquecidos com ruído controlado, reforçando boas práticas de privacidade.
- **Próximos passos**
  - Evoluir o agente de recomendações para suportar múltiplos idiomas e integrar feedbacks de voz, seguindo o ciclo PDCA já descrito em `docs/mlops-llmops.md`.
  - Automatizar dashboards de acompanhamento (Metabase ou Superset) e publicar playbooks de incidentes para manter a cultura de melhoria contínua e aprendizado compartilhado.

## Testes e ferramentas Python
As automações de IA compartilham um pacote leve em `python_src/powerbirth/`. Depois de ativar a `.venv` e instalar `requirements.txt`, utilize os comandos abaixo:

```bash
# suíte de testes
pytest

# lint
ruff check python_src tests scripts

# formatação
black python_src tests scripts

# demo ponta a ponta com dados sintéticos
python scripts/run_synthetic_inference.py --num-training-samples 400 --num-inference-samples 20
```

O script `scripts/run_synthetic_inference.py` treina o modelo logístico sintético, produz inferências para novos registros e salva um relatório em `models/synthetic_inference_results.json`.

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
