# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/18 13:51:41 by ialmani           #+#    #+#              #
#    Updated: 2026/03/18 14:36:08 by ialmani          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME    = codexion
CC      = cc
CFLAGS  = -Wall -Werror -Wextra -pthread -I includes
RM      = rm -rf

SRC =   src/main.c    \
        src/monitor.c \
        src/utils.c   \
        src/coder.c   \
        src/log.c

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

%.o: %.c includes/codexion.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re