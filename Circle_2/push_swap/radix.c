/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:07:39 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/25 02:19:27 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	max_bytes(t_stack **stack)
{
	t_stack	*head;
	int		max;
	int		bytes;

	head = *stack;
	max = head->index;
	while (head)
	{
		if (head->index > max)
			max = head->index;
		head = head->next;
	}
	bytes = 0;
	while (max > 0)
	{
		bytes++;
		max = max >> 1;
	}
	return (bytes);
}

void	radix_sort(t_stack **stack_a, t_stack **stack_b)
{
	int	max;
	int	i;
	int	j;
	int	size;

	max = max_bytes(stack_a);
	i = 0;
	while (i < max)
	{
		size = stack_size(*stack_a);
		j = 0;
		while (j < size)
		{
			if ((((*stack_a)->index >> i) & 1) == 0)
				push_b(stack_a, stack_b);
			else
				rotate_a(stack_a);
			j++;
		}
		while (*stack_b)
			push_a(stack_a, stack_b);
		i++;
	}
}
