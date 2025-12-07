/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 17:07:43 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/25 11:13:39 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

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

long	safe_atoi(const char *str)
{
	int		i;
	int		signe;
	long	num;
	long	prev;

	i = 0;
	signe = 1;
	num = 0;
	while ((str[i] >= 9 && str[i] <= 13) || str[i] == 32)
		i++;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			signe = -1;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		prev = num;
		num = num * 10 + (str[i] - '0');
		if (num / 10 != prev)
			return ((long)INT_MAX + 1);
		i++;
	}
	return (num * signe);
}

int	valid_nbr(char *token)
{
	int	i;
	int	len;

	if (!token || !*token)
		return (0);
	i = 0;
	len = 0;
	if (token[i] == '-' || token[i] == '+')
		i++;
	if (!token[i])
		return (0);
	while (token[i])
	{
		if (!ft_isdigit(token[i]))
			return (0);
		len++;
		i++;
	}
	if (len > 11)
		return (0);
	return (1);
}

t_stack	*parse_single_arg(char *arg)
{
	char	**tokens;
	t_stack	*stack;
	long	num;
	int		i;

	tokens = split_args(arg);
	stack = NULL;
	if (!tokens || !tokens[0])
		return (free_split(tokens), NULL);
	i = 0;
	while (tokens[i])
	{
		if (!valid_nbr(tokens[i]))
			return (free_split(tokens), clear_stack(&stack), NULL);
		num = safe_atoi(tokens[i]);
		if (num > INT_MAX || num < INT_MIN)
			return (free_split(tokens), clear_stack(&stack), NULL);
		stack_back(&stack, new_stack((int)num));
		i++;
	}
	if (!no_dup(stack))
		return (free_split(tokens), clear_stack(&stack), NULL);
	free_split(tokens);
	return (stack);
}

t_stack	*parsing(int ac, char **av)
{
	t_stack	*stack_a;
	int		i;
	long	num;

	if (ac < 2)
		return (NULL);
	if (ac == 2)
		return (parse_single_arg(av[1]));
	stack_a = NULL;
	i = 1;
	while (i < ac)
	{
		if (!valid_nbr(av[i]))
			return (clear_stack(&stack_a), NULL);
		num = safe_atoi(av[i]);
		if (num > INT_MAX || num < INT_MIN)
			return (clear_stack(&stack_a), NULL);
		stack_back(&stack_a, new_stack((int)num));
		i++;
	}
	if (!no_dup(stack_a))
		return (clear_stack(&stack_a), NULL);
	return (stack_a);
}
