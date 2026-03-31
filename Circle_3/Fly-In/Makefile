# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/28 14:27:29 by ialmani           #+#    #+#              #
#    Updated: 2026/03/28 14:34:29 by ialmani          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

GREEN	= \033[1;32m
RED		= \033[1;31m
BLUE	= \033[1;34m
YELLOW	= \033[1;33m
RESET	= \033[0m


PYTHON = python3
MAIN = 
NAME = Fly-In

all: run

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	@echo "$(YELLOW)🚀Launch$(NAME)...$(RESET)"
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	@echo "$(BLUE)Debbuging...$(RESET)"
	@$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@echo "$(RED)Removing cache...$(RESET)"
	@rm -rf .mypy_cache .pytest_cache .DS_Store mazegen/.DS_Store
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .


.PHONY: all install run debug clean lint lint-strict%     