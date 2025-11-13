/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_rotate.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 18:31:34 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/11 10:42:52 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	reverse_rotate(t_stack **stack)
{
	t_stack	*b_last;
	t_stack	*last;

	if (!*stack || (!(*stack)->next))
		return ;
	b_last = NULL;
	last = *stack;
	while (last->next)
	{
		b_last = last;
		last = last->next;
	}
	b_last->next = NULL;
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
