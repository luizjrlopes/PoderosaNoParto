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
