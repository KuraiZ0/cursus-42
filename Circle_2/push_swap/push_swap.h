/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:16:43 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/25 11:01:06 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <limits.h>
# include <unistd.h>
# include "libft/libft.h"
# include "ft_printf/ft_printf.h"

typedef struct s_stack
{
	int				content;
	int				index;
	struct s_stack	*next;
}	t_stack;

		/* ALGO & ASSIGN */
void	assign_index(t_stack **a);
void	radix_sort(t_stack **stack_a, t_stack **stack_b);
void	sort5(t_stack **stack_a, t_stack **stack_b);
void	sort3(t_stack **stack_a);

		/* UTILS */
void	move_and_push_min(t_stack **stack_a, t_stack **stack_b);
int		find_min(t_stack *stack);
int		max_bytes(t_stack **stack);
int		is_sorted(t_stack *stack);
char	**split_args(char *str);
void	free_split(char **split);
t_stack	*parse_single_arg(char *arg);

		/* PARSING */
t_stack	*parsing(int ac, char **av);
int		valid_nbr(char *token);
long	safe_atoi(const char *str);
int		no_dup(t_stack *stack);

		/* STACK MANIPULATION */
void	clear_stack(t_stack **stack);
t_stack	*new_stack(int content);
int		stack_size(t_stack *stack);
t_stack	*stack_last(t_stack *stack);
void	stack_back(t_stack **stack, t_stack *new_node);
t_stack	*stack_blast(t_stack *stack);

		/* OPERATIONS */
void	push(t_stack **stack_1, t_stack **stack_2);
void	push_a(t_stack **stack_a, t_stack **stack_b);
void	push_b(t_stack **stack_a, t_stack **stack_b);
void	swap(t_stack **stack_a);
void	swap_a(t_stack **stack_a);
void	swap_b(t_stack **stack_a);
void	swap_ab(t_stack **stack_a, t_stack **stack_b);
void	rotate(t_stack **stack);
void	rotate_a(t_stack **stack);
void	rotate_b(t_stack **stack);
void	rotate_ab(t_stack **stack_a, t_stack **stack_b);
void	reverse_rotate(t_stack **stack);
void	reverse_rotate_a(t_stack **stack);
void	reverse_rotate_b(t_stack **stack);
void	reverse_rotate_ab(t_stack **stack_a, t_stack **stack_b);

int		error(void);

#endif