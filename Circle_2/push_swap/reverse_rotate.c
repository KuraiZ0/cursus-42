/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_rotate.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/19 09:44:36 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/21 15:51:13 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*stack_blast(t_stack *stack)
{
	t_stack	*tmp;

	if (!stack)
		return (NULL);
	tmp = stack;
	while (tmp->next && tmp->next->next)
		tmp = tmp->next;
	return (tmp);
}

void	reverse_rotate(t_stack **stack)
{
	t_stack	*last;
	t_stack	*blast;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	blast = stack_blast(*stack);
	last = blast->next;
	blast->next = NULL;
	last->next = *stack;
	*stack = last;
}

void	reverse_rotate_a(t_stack **stack)
{
	reverse_rotate(stack);
	ft_printf("rra\n");
}

void	reverse_rotate_b(t_stack **stack)
{
	reverse_rotate(stack);
	ft_printf("rrb\n");
}

void	reverse_rotate_ab(t_stack **stack_a, t_stack **stack_b)
{
	reverse_rotate(stack_a);
	reverse_rotate(stack_b);
	ft_printf("rrr\n");
}
