/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 10:06:49 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/10 13:05:30 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "ft_printf/ft_printf.h"
# include "libft/libft.h"
# include <limits.h> // int max/min
# include <stdarg.h> //read
# include <stdlib.h> // malloc

typedef struct t_stack
{
	int				content;
	int				index;
	struct t_stack	*next;
}					t_stack;

void				ft_lstadd_front(t_list **lst, t_list *new_node);
t_list				*ft_lstlast(t_list *lst);
int					ft_lstsize(t_list *lst);
void				push(t_stack **stack1, t_stack **stack2);
void				push_a(t_stack **stack1, t_stack **stack2);
void				push_b(t_stack **stack1, t_stack **stack2);
void				swap(t_stack **stack);
void				swap_a(t_stack **stack);
void				swap_b(t_stack **stack);
void				swap_ab(t_stack **stack1, t_stack **stack2);
void				rotate(t_stack **stack);
void				reverse_rotate(t_stack **stack);
void				rotate_a(t_stack **stack);
void				reverse_rotate_a(t_stack **stack);
void				rotate_b(t_stack **stack);
void				reverse_rotate_b(t_stack **stack);
void				clear_stack(t_stack **stack);
int					valid_nbr(char *str);
int					no_dup(t_stack *stack);
t_stack				*parse_arg(int ac, char **av);
t_stack				*stack_last(t_stack *stack);
int					stack_size(t_stack *stack);
void				stack_add_back(t_stack **stack, t_stack *new_node);
t_stack				*new_stack(int content);
void				assign_index(t_stack **stack_a);
void				sort2(t_stack **stack_a);
void				sort3(t_stack **stack_a);
int					verify_all_above(t_stack **a, int max_chunks);
void				push_chunks_b(t_stack **a, t_stack **b);
void				push_back_a(t_stack **a, t_stack **b);
int					pos_index(t_stack *stack, int index);
int					max_index(t_stack *stack);

#endif