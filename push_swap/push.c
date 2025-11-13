/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 14:34:53 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/10 16:42:07 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push(t_stack **stack1, t_stack **stack2)
{
	t_stack	*elem;

	if (!*stack1)
		return ;
	elem = *stack1;
	*stack1 = (*stack1)->next;
	elem->next = *stack2;
	*stack2 = elem;
}

void	push_a(t_stack **stack1, t_stack **stack2)
{
	push(stack2, stack1);
	ft_printf("pa\n");
}

void	push_b(t_stack **stack1, t_stack **stack2)
{
	push(stack1, stack2);
	ft_printf("pb\n");
}
