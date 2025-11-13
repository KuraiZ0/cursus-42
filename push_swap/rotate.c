/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 15:14:44 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/11 10:43:14 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate(t_stack **stack)
{
	t_stack	*first;
	t_stack	*second;

	if (!*stack || (!(*stack)->next))
		return ;
	first = *stack;
	second = *stack;
	while (second->next)
		second = second->next;
	*stack = first->next;
	first->next = NULL;
	second->next = first;
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
