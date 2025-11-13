/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 20:04:20 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/11 11:19:11 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push_chunks_b(t_stack **a, t_stack **b)
{
	int	size;
	int	max_chunks;
	int	chunks_size;
	int	chunks_num;

	size = stack_size(*a);
	if (size <= 100)
		chunks_size = 20;
	else
		chunks_size = 35;
	chunks_num = 0;
	while (stack_size(*a) > 3)
	{
		max_chunks = (chunks_num + 1) * chunks_size;
		if ((*a)->index < max_chunks)
		{
			push_b(a, b);
			if ((*b)->index < max_chunks - (chunks_size / 2))
				rotate_b(b);
		}
		else
			rotate_a(a);
		if (verify_all_above(a, max_chunks))
			chunks_num++;
	}
}

void	push_back_a(t_stack **a, t_stack **b)
{
	int	max;
	int	pos;
	int	size;

	while (*b)
	{
		max = max_index(*b);
		pos = pos_index(*b, max);
		size = stack_size(*b);
		if (pos <= size / 2)
			while ((*b)->index != max)
				rotate_b(b);
		else
			while ((*b)->index != max)
				reverse_rotate_b(b);
		push_a(a, b);
	}
}
