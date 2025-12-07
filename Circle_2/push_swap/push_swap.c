/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:06:47 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/25 01:44:20 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack *stack)
{
	t_stack	*current;

	if (!stack || !stack->next)
		return (1);
	current = stack;
	while (current->next)
	{
		if (current->content > current->next->content)
			return (0);
		current = current->next;
	}
	return (1);
}

int	main(int ac, char **av)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	int		size;

	if (ac < 2)
		return (0);
	stack_a = parsing(ac, av);
	if (!stack_a)
		return (error());
	if (is_sorted(stack_a))
		return (clear_stack(&stack_a), 0);
	stack_b = NULL;
	size = stack_size(stack_a);
	assign_index(&stack_a);
	if (size == 2)
		swap_a(&stack_a);
	else if (size == 3)
		sort3(&stack_a);
	else if (size <= 5)
		sort5(&stack_a, &stack_b);
	else
		radix_sort(&stack_a, &stack_b);
	clear_stack(&stack_a);
	return (0);
}
