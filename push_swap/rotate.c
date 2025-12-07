/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/19 09:43:24 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/21 15:51:20 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate(t_stack **stack)
{
	t_stack	*elem;

	if (!stack)
		return ;
	elem = *stack;
	*stack = elem->next;
	elem->next = NULL;
	stack_last(*stack)->next = elem;
}

void	rotate_a(t_stack **stack)
{
	rotate(stack);
	ft_printf("ra\n");
}

void	rotate_b(t_stack **stack)
{
	rotate(stack);
	ft_printf("rb\n");
}

void	rotate_ab(t_stack **stack_a, t_stack **stack_b)
{
	rotate(stack_a);
	rotate(stack_b);
	ft_printf("rr\n");
}
