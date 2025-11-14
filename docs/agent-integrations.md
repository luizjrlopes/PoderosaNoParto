# Integrações com Agentes, Prompts e Pipelines Toqan-like

## Objetivos
- Orquestrar assistentes multimodais (triagem, educação em saúde e suporte ao parto) com rastreabilidade de decisões.
- Permitir experimentação rápida de prompts e ferramentas sem duplicar lógica de negócio.
- Conectar o pipeline LLMOps existente com fluxos Toqan-like (cadeias de ferramentas e memória curta/longa).

## Arquitetura Geral
1. **Orquestrador de Agentes (`src/ai/agents/orchestrator.ts`)**: abstrai criação de agentes especialistas (triagem, conteúdo, escalonamento clínico) e se integra ao backend via WebSockets.
2. **Prompt Hub (`docs/prompts/`)**: cada prompt possui metadata (`locale`, `persona`, `safety_profile`). Os prompts são versionados em Git e replicados para o bucket S3 `poderosa-prompts` através de `scripts/sync_prompts.sh`.
3. **Memória e Ferramentas**:
   - Memória curta: Redis (`redis://prompt-memory`) guarda o último turno de conversa para cada usuário, chaveado por `encounter_id`.
   - Memória longa: `notebooks/long_memory/indexing.ipynb` gera embeddings com `sentence-transformers` e persiste em Pinecone.
   - Ferramentas expostas aos agentes (consultas médicas, guidelines OMS) vivem em `src/ai/tools/` e seguem contrato `ToolHandler`.
4. **Observabilidade**: `python_src/powerbirth/telemetry/agent_spans.py` envia spans OpenTelemetry com ID do agente, ferramenta utilizada e latência.

## Pipeline Toqan-like
1. **Planejamento**: `src/ai/agents/planner.ts` recebe a intenção do usuário e decompõe em etapas usando heurísticas Toqan (avaliador de criticidade, roteador de contexto, gerador de plano).
2. **Execução com Garantias**:
   - Cada etapa do plano executa um agente especialista e registra o resultado no `PlanLog` (PostgreSQL tabela `agent_plan_events`).
   - `src/ai/agents/validators/safetyGuard.ts` aplica políticas Azure Content Safety e regras médicas (glicemia, pressão arterial) antes de enviar a resposta ao usuário.
3. **Avaliação**: o job `scripts/eval_agents.sh` percorre o conjunto `docs/prompts/regression/*.jsonl` e valida coerência, factualidade e tom. Resultados são sincronizados com MLflow como `agent_eval`.

## Integração com Pipelines de Fine-Tuning
- Quando um novo modelo conversacional é aprovado, `scripts/promote_model.py` publica o identificador do modelo em `agent_registry.yaml`.
- O orquestrador lê esse arquivo em tempo de execução e passa a usar os pesos atualizados sem reiniciar o serviço (hot reload de modelos via endpoint interno `POST /agent/reload`).
- Logs de conversas utilizados para re-treino são coletados por `python_src/powerbirth/datasets/prepare_agent_ft.py` e versionados em DVC (`dvc.yaml` > stage `agent_ft`).

## Integração com Prompts Dinâmicos
- `src/ai/prompts/runtimeResolver.ts` combina template base + variáveis contextuais (semana gestacional, idioma, preferências de parto).
- Regras de fallback garantem que, se um prompt específico não existir, o sistema utiliza o template genérico `support_pt-br_v1`.
- Mudanças em prompts disparam o workflow `.github/workflows/prompt-ci.yml`, que executa `npm run test:prompts` e o benchmark `langchain-bench` descrito em `docs/mlops-llmops.md`.

## Segurança e Compliance
- Todos os agentes executam dentro de uma sandbox Node.js com limite de tempo (5 segundos) e bloqueio a módulos críticos.
- Access tokens para ferramentas clínicas são obtidos via Azure Managed Identity e nunca persistidos em disco.
- Logs contendo PHI são pseudonimizados pela função `maskPhi` em `src/ai/security/pseudonymizer.ts` antes de serem enviados ao Data Lake.
