# Estudos de Caso e Experimentos

Este documento resume os principais experimentos executados até o momento. Cada estudo possui dataset, objetivos, métricas e links para reprodução via notebooks.

## 1. Mapeamento de Conteúdo e Jornada (notebooks/01-birth-plan-analysis)
- **Dataset**: 420 planos de parto anonimizados + trilhas educativas existentes (`data/raw/birth_plan_forms.csv`).
- **Objetivo**: identificar lacunas no conteúdo do app e propor sequência personalizada de módulos.
- **Metodologia**: TF-IDF + clustering (KMeans) para agrupar necessidades; priorização por frequência e severidade.
- **Métricas**: cobertura de temas críticos subiu de 68% para 94%; 12 módulos priorizados.
- **Insight**: técnicas respiratórias e analgesia não farmacológica são os tópicos mais demandados e viraram cards dedicados.
- **Reprodução**:
  1. `cd notebooks/01-birth-plan-analysis`
  2. `python -m venv .venv && source .venv/bin/activate`
  3. `pip install -r requirements.txt` (lista no README da pasta)
  4. Execute o notebook `birth_plan_analysis.ipynb` ou rode `papermill` via pipeline.

## 2. Modelo de Estratificação de Risco (notebooks/02-risk-stratification-model)
- **Dataset**: registros clínicos públicos do SIP/Ministério da Saúde (10.200 linhas após limpeza).
- **Objetivo**: prever risco obstétrico alto (label binário) para priorizar monitoramento.
- **Metodologia**: pipeline scikit-learn (imputação + scaling) seguido de Gradient Boosting.
- **Métricas**: AUC 0.84, F1 0.79, sensibilidade 0.81 usando validação estratificada 5-fold.
- **Insight**: histórico de hipertensão e idade gestacional foram as features de maior ganho (SHAP > 0.2).
- **Reprodução**: notebook `risk_stratification.ipynb` com execução guiada no README da pasta.

## 3. Forecast de Engajamento e Recomendação (notebooks/03-engagement-forecast)
- **Dataset**: eventos de uso sintetizados a partir de 1.3M interações (tarefa concluída, áudio reproduzido, chat com enfermeira).
- **Objetivo**: prever queda de engajamento na semana seguinte e acionar conteúdos/LLM proativos.
- **Metodologia**: modelos Prophet + LightGBM (features de série temporal + contagem) e regras de reforço para ofertas.
- **Métricas**: MAE 0.07 para previsão de taxa de conclusão semanal e recall@5 0.76 na recomendação.
- **Insight**: enviar áudios curtos após 48h sem login aumenta a taxa de retorno em 18%.
- **Reprodução**: instruções completas no README do diretório correspondente (versão Python e Papermill).

### Próximos Passos
- Expandir avaliação humana das recomendações via pesquisas in-app.
- Integrar os modelos com o backend real e executar testes de carga.
- Publicar dashboards automatizados em Metabase/Grafana com métricas mencionadas.
