/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 10:04:21 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/10 16:47:23 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sort(t_stack *stack)
{
	while (stack && stack->next)
	{
		if (stack->content > stack->next->content)
			return (0);
		stack = stack->next;
	}
	return (1);
}

int	main(int ac, char **av)
{
	t_stack	*a;
	t_stack	*b;

	if (ac < 2)
		return (1);
	a = parse_arg(ac, av);
	if (!a)
		return (write(2, "Error\n", 6), 1);
	if (is_sort(a))
		return (clear_stack(&a), 0);
	b = NULL;
	assign_index(&a);
	if (stack_size(a) == 2)
		sort2(&a);
	else if (stack_size(a) == 3)
		sort3(&a);
	else
	{
		push_chunks_b(&a, &b);
		sort3(&a);
		push_back_a(&a, &b);
	}
	clear_stack(&a);
	clear_stack(&b);
	return (0);
}

/*
ft_printf(" ___________");
ft_printf("|  a  |  b  |");
ft_printf("|-----|-----|");
ft_printf("|     |     |");
ft_printf("|     |     |");
ft_printf("|     |     |");
ft_printf(" -----------");
*/