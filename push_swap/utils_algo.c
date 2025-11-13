/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils_algo.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 20:04:29 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/11 10:42:58 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	verify_all_above(t_stack **a, int max_chunks)
{
	t_stack	*tmp;

	tmp = *a;
	while (tmp)
	{
		if (tmp->index < max_chunks)
			return (0);
		tmp = tmp->next;
	}
	return (1);
}

int	max_index(t_stack *stack)
{
	int	max;

	if (!stack)
		return (-1);
	max = stack->index;
	while (stack)
	{
		if (stack->index > max)
			max = stack->index;
		stack = stack->next;
	}
	return (max);
}

int	pos_index(t_stack *stack, int index)
{
	int	pos;

	pos = 0;
	while (stack)
	{
		if (stack->index == index)
			return (pos);
		stack = stack->next;
		pos++;
	}
	return (-1);
}
