# **************************************************************************** #
#                                                                              #
#                                                          :::      ::::::::   #
#   Makefile                                             :+:      :+:    :+:   #
#                                                      +:+ +:+         +:+     #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+        #
#                                                  +#+#+#+#+#+   +#+           #
#   Created: 2026/03/28 14:27:29 by ialmani             #+#    #+#             #
#   Updated: 2026/06/10 11:41:15 by ialmani            ###   ########.fr       #
#                                                                              #
# **************************************************************************** #

GREEN	= \033[1;32m
RED		= \033[1;31m
BLUE	= \033[1;34m
YELLOW	= \033[1;33m
RESET	= \033[0m

PYTHON = python3
MAIN = main.py
NAME = Fly-In
MAP = maps/challenger/01_the_impossible_dream.txt
VENV_PYTHON = .venv/bin/python

all: run

install:
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install flake8 mypy arcade

run:
	@echo "$(YELLOW)🚀 Launching $(NAME)...$(RESET)"
	$(PYTHON) $(MAIN) $(MAP)

debug:
	@echo "$(BLUE)Debugging...$(RESET)"
	@$(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	@echo "$(RED)Removing cache...$(RESET)"
	@rm -rf .mypy_cache .pytest_cache .DS_Store mazegen/.DS_Store
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	@echo "$(GREEN)Running Linter...$(RESET)"
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	@echo "$(GREEN)Running Strict Linter...$(RESET)"
	flake8 .
	mypy --strict .

.PHONY: all install run debug clean lint lint-strict