# Fluxos MLOps e LLMOps

## Objetivos
Garantir que os modelos de risco obstétrico, recomendação de conteúdo e assistentes conversacionais sejam treinados, validados e entregues com rastreabilidade e governança.

## Pipeline de Dados e Features
1. **Ingestão** (`scripts/ingest_events.py` - referenciado no roadmap): consome eventos Kafka/SQS e grava em `data/raw/` em formato Parquet.
2. **Qualidade e anonimização**: Great Expectations valida esquema, enquanto um job Spark remove identificadores diretos e aplica hashing nas chaves.
3. **Feature Store**: tabelas `risk_features` e `engagement_features` são publicadas em um banco relacional (PostgreSQL) e replicadas para Redis para inferência de baixa latência.

## Treinamento e Avaliação
| Etapa | Ferramentas | Descrição |
|------|-------------|-----------|
| Orquestração | GitHub Actions + Papermill | Executa notebooks em modo headless sempre que `notebooks/**` é alterado na branch principal. |
| Rastreamento | MLflow Tracking | Registra hiperparâmetros, métricas e artefatos (matrizes de confusão, gráficos SHAP). |
| Validação | pytest + great_expectations | Testes automatizados de funções de pré-processamento e checagens de dados. |
| Aprovação | Model Registry | Modelos com métrica superior ao baseline e validação manual recebem tag `Production`. |

Para smoke tests rápidos, execute `python scripts/run_synthetic_inference.py` – o script gera dados sintéticos, treina o pipeline logístico definido em `python_src/powerbirth/` e mede AUC com `pytest`/`ruff` garantindo que as funções centrais permaneçam estáveis.

## Deploy e Monitoramento
- **Serviço de inferência**: endpoints FastAPI empacotados em Docker; imagens publicadas no GHCR.
- **Rollouts**: GitHub Actions publica a imagem e atualiza o cluster Kubernetes (ou ECS) com estratégia canário (10% -> 50% -> 100%).
- **Monitoramento**: Prometheus coleta latência e taxa de erro; Evidently monitora drift de features e métricas de F1/AUC.

## Fluxos LLMOps
1. **Prompt Repository**: templates versionados em `docs/prompts/` (a ser criado conforme crescimento) com tags de idioma e persona.
2. **Avaliação automática**: cada mudança de prompt executa testes com `langchain-bench` comparando coerência clínica e tom amigável.
3. **Human-in-the-loop**: enfermeiras revisam semanalmente 20 amostras, anotando feedback via formulário integrado ao Notion.
4. **Proteções**: camadas de moderação via Azure Content Safety e filtros customizados para termos clínicos sensíveis.

## SLA e Alertas
- **Risco obstétrico**: inferência < 300 ms (P95) e AUC semanal > 0.82.
- **Recomendação de conteúdo**: refresh diário com recall@5 >= 0.73.
- **Assistente LLM**: custo por mensagem monitorado; alerta disparado se aumento > 20% em 24h.

Consulte `docs/case-studies.md` para exemplos concretos dos experimentos e notebooks relacionados.

## Pipeline de Fine-Tuning End-to-End

1. **Seleção do modelo base**: modelos encoder-decoder clínicos (BioBERT, Clinical-T5) vivem em `models/base/` com manifestos
   (`modelcard.yaml`) contendo licença e limitações. Atualizamos o manifesto ao sincronizar uma nova versão a partir do Hugging
   Face Hub.
2. **Preparação do dataset**: `notebooks/fine_tuning/preprocess.ipynb` normaliza escalas vitais, aplica técnicas de anonimizaçã
   o e exporta splits balanceados para `data/processed/<dataset>/<timestamp>/`. O notebook gera um `dataset_report.json` usad
   o em auditorias.
3. **Configuração declarativa**: `python_src/powerbirth/training/configs/*.yaml` define hiperparâmetros e destinos de log. O sc
   ript `python_src/powerbirth/training/run_finetune.py` carrega esse YAML, instancia o modelo base e adapta camadas finais se
   gundo a tarefa (classificação de risco, geração de recomendações ou agentes conversacionais).
4. **Execução**: `scripts/launch_training.sh` empacota a execução em um job Argo Workflows, injeta secrets (tokens Hugging Face
   /Azure) e publica métricas em MLflow Tracking. As execuções são versionadas via `mlflow run . -e finetune` com tags de bran
   ch e commit.
5. **Empacotamento**: após o fine-tuning, `scripts/promote_model.py` exporta pesos para `models/<task>/<version>/` e publica u
   m artefato `.tar.gz` no Model Registry com metadados de dataset, seed e custo.

## Avaliação Estruturada

- **Offline**: `python_src/powerbirth/evaluation/offline_eval.py` executa validação cruzada estratificada e gera métricas (AUC,
  F1, perplexidade para LLMs) armazenadas em `artifacts/eval/<run_id>/metrics.json`. Cada métrica referencia o commit exato vi
  a campo `git_sha`.
- **Testes de regressão com prompts**: `notebooks/fine_tuning/prompt_regression.ipynb` avalia respostas dos agentes conversacio
  nais usando um conjunto fixo de prompts críticos (alerta de pré-eclâmpsia, plano de parto humanizado). Scores BLEU e avaliaç
  ões humanas são agregados em `docs/model-performance.md`.
- **Avaliação online**: após o deploy em canário, o job `scripts/monitor_eval.py` captura métricas reais e aplica testes statis
  ticos de Mann–Whitney para comparar com a linha de base das últimas 24h, evitando regressões silenciosas.

## Deploy Detalhado

1. **Empacotamento de inferência**: `python_src/powerbirth/serve/app.py` expõe modelos via FastAPI. O Dockerfile reutiliza uma
   imagem base `poderosa-ml:runtime` e adiciona os pesos aprovados através de um `ARG MODEL_VERSION`.
2. **Pipelines de entrega**: `.github/workflows/deploy.yml` aciona sempre que um modelo recebe tag `Production`. O workflow faz
   push da imagem para GHCR, atualiza manifests Helm (`deploy/k8s/templates/model-serving.yaml`) e injeta variáveis de feature
   store.
3. **Verificação pós-deploy**: `scripts/post_deploy_checks.py` envia 50 requisições sintéticas com valores extremos e valida se
   as respostas obedecem às faixas clínicas. Falhas bloqueiam a conclusão do job GitHub Actions.
4. **Rollback guiado**: mantemos `deploy/releases.json` com histórico dos últimos 10 rollouts, permitindo `scripts/rollback.sh`
   aplicar `kubectl rollout undo` ou `ecs deploy --previous` em menos de 5 minutos.
