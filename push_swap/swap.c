/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 11:55:08 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/09 19:58:37 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap(t_stack **stack)
{
	t_stack	*elem;

	if (!*stack || (*stack)->next == NULL)
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

void	swap_ab(t_stack **stack1, t_stack **stack2)
{
	swap(stack1);
	swap(stack2);
	ft_printf("ss\n");
}
