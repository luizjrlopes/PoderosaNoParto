# Arquitetura das Soluções

## Visão Geral
O ecossistema Poderosa no Parto combina um front-end React hospedado como SPA, uma camada de APIs Node/Express e fluxos de dados destinados às análises MLOps/LLMOps. O diagrama lógico pode ser resumido em três zonas:
1. **Experiência da gestante** (navegador ou PWA) renderizada pela pasta `src/`.
2. **Serviços de orquestração** responsáveis por autenticação, agenda personalizada e registro de telemetria (deployáveis em containers ou Functions-as-a-Service).
3. **Camada de dados e experimentação** com buckets de dados clínicos anonimizados, Feature Store e pipelines hospedados em notebooks ou jobs automatizados.

## Componentes Principais
| Componente | Tecnologias | Responsabilidades |
|------------|-------------|------------------|
| Interface Web | React 18, React Router, Bootstrap | Cadastro, acompanhamento diário, gráficos de progresso e conteúdo educativo responsivo. |
| API de apoio | Node.js, Express, MongoDB ou PostgreSQL | CRUD de perfis, agendamentos e coleta de eventos para analytics/ML. |
| Telemetria e Observabilidade | Segment/GA4 (client), OpenTelemetry (server) | Envio de métricas de engajamento e logs de falhas para dashboards. |
| Pipelines de ML | Python 3.10, scikit-learn, pandas, MLflow | Treinamento de modelos de risco obstétrico e recomendação de conteúdos. |
| Camada de Integração LLM | LangChain, OpenAI API/Azure OpenAI | Geração de mensagens educativas personalizadas usando prompts condicionados a perfis. |

## Fluxo de Dados
1. A usuária autentica via front-end; tokens são emitidos pela API.
2. Eventos de uso (tarefa concluída, áudio tocado, etc.) são enviados para a fila `engagement-events` (Kafka ou SQS).
3. Jobs ETL consolidados sincronizam os eventos para o data lake (parquet) e populam a Feature Store.
4. Pipelines descritos nos notebooks transformam os dados em embeddings, métricas e previsões.
5. As predições retornam ao front-end via endpoints `/recommendations` e `/risk-score`, atualizando dashboards e notificações.

## Considerações de Segurança e Privacidade
- Todos os dados pessoais são criptografados em repouso (AES-256) e em trânsito (HTTPS/TLS 1.2+).
- O modelo separa identificadores diretos (ID, e-mail) de atributos clínicos, mantendo chaves substitutas nas bases analíticas.
- Logs são pseudonimizados antes de trafegar para ferramentas externas.

## Estratégias de Deploy
- **Front-end**: build estático (`npm run build`) publicado em Vercel/Netlify ou buckets S3+CloudFront.
- **APIs**: containers Docker com health checks; ambiente staging e produção controlados via GitHub Actions.
- **Pipelines**: agendados em Airflow ou GitHub Actions cron, executando notebooks headless com Papermill.

Consulte `docs/mlops-llmops.md` para detalhes dos pipelines e SLAs monitorados.
