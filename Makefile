# ============================================================================
# Makefile for Maze Generator
# ============================================================================

# Variables
PY = python3
DEBUGGER = pdb3
SRC = a_maze_ing.py
PIP      = pip

# Colors
RED_COLOR = \033[31m
GREEN_COLOR = \033[32m
YELLOW_COLOR = \033[33m
BLUE_COLOR = \033[34m
NC = \033[0m

# ============================================================================
# Targets
# ============================================================================

all: run

run:
	@$(PY) $(SRC) config.txt

install:
	$(PY) -m $(PIP) install --user flake8 mypy

debug:
	@echo "$(BLUE_COLOR) Starting debugger...$(NC)"
	@$(DEBUGGER) $(SRC) config.txt

lint:
	@echo "$(GREEN_COLOR) Running flake8 and mypy...$(NC)"
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(GREEN_COLOR)✓ Linting complete!$(NC)"

clean:
	@echo "$(YELLOW_COLOR)🧹 Cleaning cache...$(NC)"
	@rm -rf __pycache__
	@rm -rf */*__pycache__
	@rm -rf .mypy_cache
	@echo "$(GREEN_COLOR)✓ Clean complete!$(NC)"

.PHONY: all run install debug lint clean
