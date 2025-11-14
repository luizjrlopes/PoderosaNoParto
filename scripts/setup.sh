#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
REQ_FILE="$ROOT_DIR/requirements.txt"

log() {
  echo -e "\033[1;32m[setup]\033[0m $1"
}

die() {
  echo -e "\033[1;31m[error]\033[0m $1" >&2
  exit 1
}

command -v npm >/dev/null 2>&1 || die "npm não encontrado. Instale Node.js 18+ e tente novamente."
command -v python3 >/dev/null 2>&1 || die "python3 não encontrado. Instale Python 3.10+ e tente novamente."

log "Instalando dependências do front-end"
(cd "$ROOT_DIR" && npm install)

log "Criando ambiente virtual em $VENV_DIR"
python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip

if [[ -f "$REQ_FILE" ]]; then
  log "Instalando dependências Python listadas em requirements.txt"
  pip install -r "$REQ_FILE"
else
  log "Nenhum requirements.txt encontrado; pulando instalação Python"
fi

log "Setup concluído. Ative o ambiente com 'source $VENV_DIR/bin/activate' antes de rodar notebooks e scripts Python."
