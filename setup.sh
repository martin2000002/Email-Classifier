#!/bin/bash
# Root setup: create venv and install requirements
VENV_PATH=${1:-venv}
REQ_PATH=${2:-requirements.txt}

set -e

CYAN='\033[0;36m'; GREEN='\033[0;32m'; RED='\033[0;31m'; MAGENTA='\033[0;35m'; YEL='\033[1;33m'; NC='\033[0m'

echo -e "${MAGENTA}Unified Setup (root)${NC}"

if command -v python3 &>/dev/null; then PY_CMD=python3; elif command -v python &>/dev/null; then PY_CMD=python; else echo -e "${RED}[X] Python not found${NC}"; exit 1; fi
echo -e "${CYAN} -> Using $($PY_CMD --version)${NC}"

if [ ! -d "$VENV_PATH" ]; then
  echo -e "${CYAN} -> Creating venv at '$VENV_PATH'${NC}"
  $PY_CMD -m venv "$VENV_PATH"
  echo -e "${GREEN} [OK] venv created${NC}"
else
  echo -e "${CYAN} -> venv already exists at '$VENV_PATH'${NC}"
fi

if [ ! -f "$REQ_PATH" ]; then echo -e "${RED}[X] requirements.txt not found at $REQ_PATH${NC}"; exit 1; fi

echo -e "${CYAN} -> Upgrading pip${NC}"
"$VENV_PATH/bin/python" -m pip install --upgrade pip

echo -e "${CYAN} -> Installing requirements from $REQ_PATH${NC}"
"$VENV_PATH/bin/python" -m pip install -r "$REQ_PATH"

echo -e "${YEL}Done. Activate with: source $VENV_PATH/bin/activate${NC}"
