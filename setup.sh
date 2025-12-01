#!/bin/bash
# Root setup: create venv and install requirements
VENV_PATH=${1:-venv}
REQ_PATH=${2:-requirements.txt}

set -e

CYAN='\033[0;36m'; GREEN='\033[0;32m'; RED='\033[0;31m'; MAGENTA='\033[0;35m'; YEL='\033[1;33m'; NC='\033[0m'

echo -e "${MAGENTA}SETUP${NC}"

if command -v python3 &>/dev/null; then PY_CMD=python3; elif command -v python &>/dev/null; then PY_CMD=python; else echo -e "${RED}[X] Python not found${NC}"; exit 1; fi
echo -e "${CYAN} -> Using $($PY_CMD --version)${NC}"

if [ ! -d "$VENV_PATH" ]; then
  echo -e "${CYAN} -> Creating venv at '$VENV_PATH'${NC}"
  $PY_CMD -m venv "$VENV_PATH"
  echo -e "${GREEN} [OK] venv created${NC}"

  if [ ! -f "$REQ_PATH" ]; then echo -e "${RED}[X] requirements.txt not found at $REQ_PATH${NC}"; exit 1; fi

  echo -e "${CYAN} -> Upgrading pip${NC}"
  "$VENV_PATH/bin/python" -m pip install --upgrade pip

  echo -e "${CYAN} -> Installing requirements from $REQ_PATH${NC}"
  "$VENV_PATH/bin/python" -m pip install -r "$REQ_PATH"
else
  echo -e "${CYAN} -> venv already exists at '$VENV_PATH'. Skipping setup steps...${NC}"
fi

echo -e "${YEL}Done. Activate with: source $VENV_PATH/bin/activate${NC}"

# --- Interactive Menu ---
while true; do
    echo ""
    echo -e "${CYAN}==============================================${NC}"
    echo -e "\033[44;37m       EMAIL CLASSIFIER - CONTROL PANEL       \033[0m"
    echo -e "${CYAN}==============================================${NC}"
    echo -e "${GREEN} [1] Start Backend API (New Terminal)${NC}"
    echo -e "${GREEN} [2] Open Frontend (Default Browser)${NC}"
    echo -e "${GREEN} [3] Retrain Model (Current Window)${NC}"
    echo -e "${GREEN} [4] Run Tests (pytest -q)${NC}"
    echo -e "${RED} [5] Exit${NC}"
    echo -e "${CYAN}==============================================${NC}"
    
    read -p " Select an option: " choice
    
    case $choice in
        1)
            echo -e "${YEL} >> Launching Backend API...${NC}"
            # Detect OS for new terminal command
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                osascript -e "tell application \"Terminal\" to do script \"cd '$(pwd)/code/backend' && source '$(pwd)/$VENV_PATH/bin/activate' && python -m uvicorn main:app --reload\""
            else
                # Linux (try gnome-terminal, xterm, or fallback)
                if command -v gnome-terminal &>/dev/null; then
                    gnome-terminal -- bash -c "cd code/backend; source ../../$VENV_PATH/bin/activate; python -m uvicorn main:app --reload; exec bash"
                elif command -v xterm &>/dev/null; then
                    xterm -e "cd code/backend; source ../../$VENV_PATH/bin/activate; python -m uvicorn main:app --reload; exec bash"
                else
                    echo -e "${RED}No supported terminal emulator found (gnome-terminal/xterm). Running in background...${NC}"
                    (cd code/backend && source "../../$VENV_PATH/bin/activate" && python -m uvicorn main:app --reload) &
                fi
            fi
            ;;
        2)
            echo -e "${YEL} >> Opening Frontend...${NC}"
            HTML_FILE="$(pwd)/code/frontend/index.html"
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open "$HTML_FILE"
            elif command -v xdg-open &>/dev/null; then
                xdg-open "$HTML_FILE"
            else
                echo -e "${RED}Could not detect browser opener.${NC}"
            fi
            ;;
        3)
            echo -e "${YEL} >> Retraining Model...${NC}"
            (cd code/backend && "../../$VENV_PATH/bin/python" train.py)
            ;;
        4)
            echo -e "${YEL} >> Running Tests...${NC}"
            "$VENV_PATH/bin/pytest" -q
            ;;
        5)
            echo -e "${CYAN}Bye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option.${NC}"
            ;;
    esac
done
