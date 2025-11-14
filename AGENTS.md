# AGENTS Instructions

## Scope
Estas diretrizes se aplicam a todo o repositório. Subdiretórios podem definir instruções adicionais em seus próprios `AGENTS.md` quando necessário.

## Estrutura de diretórios
- `src/`: código-fonte principal da aplicação.
- `public/`: ativos estáticos servidos diretamente (imagens, HTML base, etc.).
- `docs/`: documentação do projeto e guias de uso (crie quando necessário).
- `notebooks/`: experimentos exploratórios, prototipagem e análises (crie conforme surgirem notebooks).
- `models/`: artefatos de IA treinados, pesos e versões (crie se for armazenar modelos).
- `scripts/`: utilitários de automação (build, deploy, ETL, etc.).

Mantenha a árvore organizada; crie subpastas adicionais apenas quando houver clara necessidade.

## Convenções de código
- Utilize padrões idiomáticos para o ecossistema do arquivo (React/TypeScript, Node, etc.).
- Prefira componentes e funções pequenas, puras e com responsabilidades bem definidas.
- Nomeie arquivos e símbolos de forma descritiva, usando `kebab-case` para arquivos e `camelCase`/`PascalCase` conforme convenção da linguagem.
- Adote linters e formatadores configurados no projeto. Se adicionar dependências novas, atualize a documentação de setup.

## Testes
- Antes de abrir um PR, execute os testes disponíveis (`npm test`, `npm run lint`, etc.).
- Inclua testes automatizados para novos comportamentos relevantes.
- Documente comandos adicionais em sub-`AGENTS.md` quando áreas específicas tiverem fluxos próprios de testes.

## Documentação
- Atualize o `README.md` ou arquivos em `docs/` quando mudanças impactarem configuração, build, deploy ou uso.
- Documente APIs e componentes expostos, mantendo exemplos de uso atualizados.

## Experimentos de IA
Descreva experimentos de IA (em `docs/`, `notebooks/` ou arquivos dedicados) com as seguintes informações mínimas:
1. **Datasets**: origem, licença, pré-processamento aplicado e particionamento (treino/val/teste).
2. **Configuração do modelo**: arquitetura, hiperparâmetros e versões de dependências.
3. **Métricas**: indicadores principais (ex.: accuracy, F1, BLEU) e como são calculados.
4. **Resultados**: tabelas/gráficos com valores absolutos e comparações com baselines.
5. **Reprodutibilidade**: comandos para treinar/avaliar, seeds e requisitos de hardware.

## Sub-`AGENTS.md`
- Áreas específicas (frontend, backend, notebooks, scripts, etc.) devem possuir seus próprios `AGENTS.md` descrevendo padrões adicionais (ex.: estilo de componentes React, convenções de notebooks, requisitos de deploy).
- Coloque o sub-`AGENTS.md` na raiz do respectivo diretório; ele prevalece sobre instruções mais gerais nesta raiz.
- Sempre verifique se já existe um arquivo de instruções antes de adicionar novas regras.
