# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/19 09:44:21 by iliasalmani       #+#    #+#              #
#    Updated: 2025/12/05 19:07:58 by iliasalmani      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap
CC = cc
CFLAGS = -Wall -Werror -Wextra
RM = rm -f

# Library paths
LIBFT_DIR = ./libft
LIBFT = $(LIBFT_DIR)/libft.a
PRINTF_DIR = ./ft_printf
PRINTF = $(PRINTF_DIR)/libftprintf.a

SRC = push_swap.c \
		push.c\
		push_swap_utils.c\
		parsing_utils.c\
		parsing.c\
		reverse_rotate.c\
		swap.c\
		rotate.c\
		small_sort.c\
		radix.c\
		index.c\
		error_handle.c\

OBJ = $(SRC:.c=.o)Updated!``
ok





%.o: %.c push_swap.h
	$(CC) $(CFLAGS) -I$(LIBFT_DIR) -I$(PRINTF_DIR) -c $< -o $@

$(NAME): $(OBJ) $(LIBFT) $(PRINTF)
	$(CC) $(CFLAGS) $(OBJ) $(LIBFT) $(PRINTF) -o $(NAME)

$(LIBFT):
	make -C $(LIBFT_DIR)

$(PRINTF):
	make -C $(PRINTF_DIR)
clean:
	$(RM) $(OBJ)
	make clean -C $(LIBFT_DIR)
	make clean -C $(PRINTF_DIR)

fclean: clean
	$(RM) $(NAME)
	make fclean -C $(LIBFT_DIR)
	make fclean -C $(PRINTF_DIR)

re: fclean all

.PHONY: all clean fclean re
