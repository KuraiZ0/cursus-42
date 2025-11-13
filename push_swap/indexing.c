/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   indexing.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 20:04:10 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/10 10:18:42 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	assign_index(t_stack **stack_a)
{
	t_stack	*current;
	t_stack	*cmp;
	int		count;

	current = *stack_a;
	while (current)
	{
		count = 0;
		cmp = *stack_a;
		while (cmp)
		{
			if (cmp->content < current->content)
				count++;
			cmp = cmp->next;
		}
		current->index = count;
		current = current->next;
	}
}
