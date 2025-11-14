# Scripts

Centralize scripts de automação (build, deploy, ETL, migrações, etc.) neste diretório. Mantenha cada script documentado com instruções de uso, dependências e variáveis de ambiente necessárias.

## Scripts disponíveis

### `run_synthetic_inference.py`
Executa uma pipeline de demonstração com dados sintéticos:

```bash
python scripts/run_synthetic_inference.py --num-training-samples 400 --num-inference-samples 32
```

O script utiliza o pacote `powerbirth` para treinar o modelo logístico, gerar previsões e salvar o resumo em `models/synthetic_inference_results.json`.
