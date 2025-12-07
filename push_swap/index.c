/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   index.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:07:41 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/24 20:56:30 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	assign_index(t_stack **a)
{
	t_stack	*current;
	t_stack	*cmp;
	int		index;

	current = *a;
	while (current)
	{
		index = 0;
		cmp = *a;
		while (cmp)
		{
			if (cmp->content < current->content)
				index++;
			cmp = cmp->next;
		}
		current->index = index;
		current = current->next;
	}
}
