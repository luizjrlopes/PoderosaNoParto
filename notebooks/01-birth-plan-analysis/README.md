# Notebook: Birth Plan Analysis

## Contexto
Investiga os planos de parto coletados durante as oficinas com enfermeiras para mapear expectativas das gestantes e comparar com o conteúdo já disponível no aplicativo. O estudo identifica tópicos recorrentes, lacunas e oportunidades de novos módulos educacionais.

## Dados Utilizados
- `data/raw/birth_plan_forms.csv`: respostas textuais anonimizadas das gestantes.
- `data/reference/education_tracks.csv`: catálogo de módulos e respectivos objetivos pedagógicos.

## Dependências
Execute em Python 3.10+ com os seguintes pacotes:
```
pip install -r requirements.txt
```
`requirements.txt` lista pandas, numpy, scikit-learn, nltk, matplotlib e seaborn.

## Como Reproduzir
1. `cd notebooks/01-birth-plan-analysis`
2. Crie um ambiente virtual: `python -m venv .venv && source .venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Baixe/copier os datasets para a pasta `data/` indicada.
5. Abra `birth_plan_analysis.ipynb` no Jupyter Lab ou execute com Papermill: `papermill birth_plan_analysis.ipynb output.ipynb`.

## Resultados Esperados
- Relatório de clusters com os temas mais mencionados.
- Tabela de cobertura por módulo exibindo aumento estimado de 68% para 94% dos tópicos críticos.
- Exportação `recommended_curriculum.json` consumida pelo app para montar agendas personalizadas.
