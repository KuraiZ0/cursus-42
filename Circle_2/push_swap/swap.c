/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:16:44 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/21 15:51:27 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap(t_stack **stack)
{
	t_stack	*elem;

	if (!stack || (*stack)->next == NULL)
		return ;
	elem = (*stack)->next;
	(*stack)->next = elem->next;
	elem->next = *stack;
	*stack = elem;
}

void	swap_a(t_stack **stack)
{
	swap(stack);
	ft_printf("sa\n");
}

void	swap_b(t_stack **stack)
{
	swap(stack);
	ft_printf("sb\n");
}

void	swap_ab(t_stack **stack_a, t_stack **stack_b)
{
	swap(stack_a);
	swap(stack_b);
	ft_printf("ss\n");
}
