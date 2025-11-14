# Resultados recentes de modelos de IA

Este documento resume os experimentos conduzidos em março/2025 para dois fluxos críticos da plataforma Poderosa no Parto:
(1) estratificação de risco materno e (2) previsão semanal de engajamento. Todas as execuções foram realizadas no cluster
interno com GPUs A10G e seeds fixas (`42`).

## 1. Estratificação de risco materno

- **Dataset**: 18.420 prontuários anonimizados (2019-2024) provenientes da rede SUS Digital com aprovação ética 992/24.
- **Particionamento**: 70% treino, 15% validação, 15% teste estratificado por hospital.
- **Métricas**: precisão, recall e F1 macro para o rótulo "alto risco".

> **Gráfico offline**: os gráficos comparativos podem ser regenerados localmente executando `python scripts/plot_model_metrics.py`,
> que exporta PNGs temporários em `docs/img/` (mantidos fora do versionamento para evitar binários pesados no repositório).

| Modelo                | Precisão | Recall | F1   | Tempo de inferência (ms) | Observações |
|-----------------------|----------|--------|------|--------------------------|-------------|
| Regressão Logística   | 0.71     | 0.79   | 0.74 | 4.2                      | Base line interpretável, mas sensível a desbalanceamento. |
| Gradient Boosting     | 0.79     | 0.84   | 0.81 | 11.8                     | Melhor recall que a regressão e ainda treinável em CPU. |
| Transformer Clínico   | 0.83     | 0.88   | 0.85 | 35.4                     | Requer GPU para ficar em tempo real, porém reduz falsos negativos em 18%. |

**Interpretação**: O Transformer Clínico oferece o melhor equilíbrio entre recall e precisão, garantindo alertas mais
precoces para gestantes vulneráveis. Contudo, o custo de GPU exige escalonar pods com prioridade apenas para UBS de maior
volume. O Gradient Boosting continua recomendado para unidades sem aceleração.

## 2. Previsão de engajamento semanal

- **Dataset**: 1,2 milhões de interações no app (áudios, quizzes, teleconsultas) alinhadas à idade gestacional.
- **Janela**: séries de 12 semanas com horizonte máximo de 6 semanas à frente.
- **Métrica principal**: RMSE em pontos de engajamento (0-100).

> **Gráfico offline**: gere a curva de RMSE por horizonte com `python scripts/plot_model_metrics.py` para visualizar a diferença
> absoluta entre os modelos (artefatos não versionados por padrão).

| Modelo              | RMSE @ +2s | RMSE @ +4s | RMSE @ +6s | Observações |
|---------------------|------------|------------|------------|-------------|
| Prophet baseline    | 9.9        | 10.4       | 11.5       | Fácil de explicar mas não captura padrões comportamentais complexos. |
| Seq2Seq LSTM        | 8.0        | 8.8        | 9.8        | Balanceia custo computacional e melhora 16% o RMSE vs. Prophet. |
| Temporal Transformer| 7.0        | 7.6        | 8.5        | Mantém erros baixos mesmo para +6 semanas e permite explicar atenção por conteúdo. |

**Interpretação**: O Temporal Transformer reduz o RMSE médio em 24% comparado ao baseline, o que permite recomendar
contenúdos com antecedência. Entretanto, o Seq2Seq LSTM continua útil para execuções em lotes noturnos quando há limite
para memória GPU.

## Reprodutibilidade

1. Ative o ambiente Python descrito em `pyproject.toml` ou `requirements.txt`.
2. Execute `python notebooks/02-risk-stratification-model/train.py --config configs/risk/v3.yaml` para reproduzir o experimento
   de risco (logs disponíveis no MLflow `mlruns/43`).
3. Execute `python notebooks/03-engagement-forecast/train.py --config configs/engagement/v5.yaml` para a previsão de engajamento.
4. Para regenerar os gráficos deste documento rode `python scripts/plot_model_metrics.py`, que salva as imagens na pasta `docs/img`.
