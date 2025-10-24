# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/21 16:01:09 by iliasalmani       #+#    #+#              #
#    Updated: 2025/10/24 12:19:07 by iliasalmani      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a
LIBFT_DIR = libft
LIBFT = $(LIBFT_DIR)/libft.h
CC = cc 
CFLAGS = -Wall -Werror -Wextra -I$(LIBFT_DIR)
AR = ar rcs
RM = rm -f

SRC = ft_printf.c print_func.c print_func2.c

OBJ = $(SRC:.c=.o)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

all: $(NAME)

$(LIBFT):
	make -C $(LIBFT_DIR)

$(NAME): $(LIBFT) $(OBJ)
	make -C $(LIBFT_DIR)
	cp $(LIBFT_DIR)/libft.a $(NAME)
	$(AR) $(NAME) $(OBJ)

clean:
		$(RM) $(OBJ)

fclean: clean
		$(RM) $(NAME) 

re: fclean all

.PHONY: all clean re test