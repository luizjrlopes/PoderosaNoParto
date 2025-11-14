# Notas de Experimentação e Aprendizados

## 2024-05-xx — Iteração sobre Fine-Tuning Conversacional
- **Hipótese**: camadas adicionais de LoRA em cabeçalhos de atenção reduziriam alucinações sem aumentar custo.
- **Experimento**: executamos `python_src/powerbirth/training/run_finetune.py --config lora_guardrails.yaml` usando 2 GPUs A10.
- **Resultado**: perplexidade caiu de 12.3 para 10.7 (+13%), custo incremental de inferência < 3% ao reaproveitar adapters.
- **Decisão**: manter a variação com LoRA para agentes de escalonamento clínico e documentar checkpoints em `models/agents/v2`.

## 2024-05-xx — Integração Toqan-like
- **Hipótese**: adicionar um planejador explícito reduziria tempo de resposta quando múltiplas ferramentas são encadeadas.
- **Experimento**: protótipo `src/ai/agents/planner.ts` inspirado no paper Toqan e usando heurística de criticidade.
- **Resultado**: latência média caiu 18% (1.2s → 0.98s) pois eliminamos chamadas redundantes a ferramentas clínicas.
- **Decisão**: promover o planejador para produção após cobertura de testes (`npm run test:agents`) e adicionar métricas em OpenTelemetry.

## 2024-05-xx — Monitoramento pós-deploy
- **Hipótese**: verificar extremos sintéticos após deploy detectaria regressões antes do tráfego real.
- **Experimento**: `scripts/post_deploy_checks.py` enviando 50 requisições com sinais vitais limítrofes.
- **Resultado**: detectou uma regressão na release `2024.05.12` causada por normalização inadequada de idade gestacional.
- **Decisão**: tornou-se gate obrigatório no workflow `.github/workflows/deploy.yml` e adicionamos alerta no Slack `#ml-ops`.
