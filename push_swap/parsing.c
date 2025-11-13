/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 19:17:45 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/09 19:56:12 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	valid_nbr(char *str)
{
	int	i;

	i = 0;
	if (str[i] == '-' || str[i] == '+')
		i++;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (!ft_isdigit(str[i]))
			return (0);
		i++;
	}
	return (1);
}

int	no_dup(t_stack *stack)
{
	t_stack	*current;
	t_stack	*check;

	current = stack;
	while (current)
	{
		check = current->next;
		while (check)
		{
			if (current->content == check->content)
				return (0);
			check = check->next;
		}
		current = current->next;
	}
	return (1);
}

t_stack	*parse_arg(int ac, char **av)
{
	t_stack	*stack_a;
	long	num;
	int		i;

	stack_a = NULL;
	i = 1;
	while (i < ac)
	{
		if (!valid_nbr(av[i]))
			return (clear_stack(&stack_a), NULL);
		num = ft_atoi(av[i]);
		if (num > INT_MAX || num < INT_MIN)
			return (clear_stack(&stack_a), NULL);
		stack_add_back(&stack_a, new_stack((int)num));
		i++;
	}
	if (!no_dup(stack_a))
		return (clear_stack(&stack_a), NULL);
	return (stack_a);
}
