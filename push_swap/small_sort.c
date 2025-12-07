/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   small_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 12:27:39 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/25 02:20:54 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	find_min(t_stack *stack)
{
	t_stack	*current;
	int		min;
	int		pos;
	int		current_pos;

	if (!stack)
		return (-1);
	min = stack->content;
	pos = 0;
	current_pos = 0;
	current = stack;
	while (current)
	{
		if (current->content < min)
		{
			min = current->content;
			pos = current_pos;
		}
		current = current->next;
		current_pos++;
	}
	return (pos);
}
/* take the min of stack_a amd push min to stack_b */

void	move_and_push_min(t_stack **stack_a, t_stack **stack_b)
{
	int	min;
	int	size;

	size = stack_size(*stack_a);
	min = find_min(*stack_a);
	if (min <= size / 2)
	{
		while (min > 0)
		{
			rotate_a(stack_a);
			min--;
		}
	}
	else
	{
		while (min < size)
		{
			reverse_rotate_a(stack_a);
			min++;
		}
	}
	push_b(stack_a, stack_b);
}

void	sort3(t_stack **stack_a)
{
	int	a;
	int	b;
	int	c;

	if (!stack_a || !*stack_a || !(*stack_a)->next || !(*stack_a)->next->next)
		return ;
	a = (*stack_a)->content;
	b = (*stack_a)->next->content;
	c = (*stack_a)->next->next->content;
	if (a > b && b > c)
		return (rotate_a(stack_a), swap_a(stack_a));
	else if (a > b && b < c && a > c)
		rotate_a(stack_a);
	else if (a < b && b > c && a < c)
		return (reverse_rotate_a(stack_a), swap_a(stack_a));
	else if (a < b && b > c && a > c)
		reverse_rotate_a(stack_a);
	else if (a > b && b < c && a < c)
		swap_a(stack_a);
}

void	sort5(t_stack **stack_a, t_stack **stack_b)
{
	move_and_push_min(stack_a, stack_b);
	move_and_push_min(stack_a, stack_b);
	sort3(stack_a);
	push_a(stack_a, stack_b);
	push_a(stack_a, stack_b);
}
