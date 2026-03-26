# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/18 13:51:41 by ialmani           #+#    #+#              #
#    Updated: 2026/03/26 14:33:53 by ialmani          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

GREEN	= \033[1;32m
RED		= \033[1;31m
BLUE	= \033[1;34m
YELLOW	= \033[1;33m
RESET	= \033[0m


NAME    = codexion
CC      = cc
CFLAGS  = -Wall -Werror -Wextra -pthread -I.
RM      = rm -rf

SRC =   main.c    	 \
        monitor.c 	 \
        utils.c   	 \
        utils2.c  	 \
		routine.c 	 \
		heap.c    	 \
		heap_utils.c \
		clean.c

OBJ_DIR = obj
OBJ = $(addprefix $(OBJ_DIR)/, $(SRC:.c=.o))

all: $(NAME)

$(NAME): $(OBJ)
	@echo "$(YELLOW)Linking $(NAME)...$(RESET)"
	@$(CC) $(CFLAGS) $(OBJ) -o $(NAME)
	@echo "$(GREEN)Compilation successfully done ! $(RESET)"

$(OBJ_DIR)/%.o: %.c codexion.h
	@mkdir -p $(OBJ_DIR)
	@echo "$(BLUE)Compiling $<...$(RESET)"
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	@$(RM) $(OBJ)
	@$(RM) $(OBJ_DIR)
	@echo "$(RED)Object files and folder deleted.$(RESET)"

fclean: clean
	@$(RM) $(NAME)
	@echo "$(RED)Binary $(NAME) deleted. $(RESET)"

re: fclean all

.PHONY: all clean fclean re