/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/26 11:06:14 by ialmani           #+#    #+#             */
/*   Updated: 2026/04/08 12:27:32 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	swap(t_request *a, t_request *b)
{
	t_request	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

int	init_heap(t_heap *heap, int capacity)
{
	heap->capacity = capacity;
	heap->size = 0;
	heap->array = malloc(sizeof(t_request) * capacity);
	if (!heap->array)
		return (1);
	return (0);
}

static int	cond_for_pop(t_heap *heap, int small, int left, int right)
{
	if (left < heap->size && (heap->array[left].priority
			< heap->array[small].priority
			|| (heap->array[left].priority == heap->array[small].priority
			&& heap->array[left].coder_id > heap->array[small].coder_id)))
		small = left;
	if (right < heap->size && (heap->array[right].priority
			< heap->array[small].priority
			|| (heap->array[right].priority == heap->array[small].priority
				&& heap->array[right].coder_id > heap->array[small].coder_id)))
		small = right;
	return (small);
}

void	pop_utils(t_heap *heap, int i)
{
	int	left;
	int	right;
	int	small;

	while (1)
	{
		small = i;
		left = 2 * i + 1;
		right = 2 * i + 2;
		small = cond_for_pop(heap, small, left, right);
		if (small != i)
		{
			swap(&heap->array[small], &heap->array[i]);
			i = small;
		}
		else
			break ;
	}
}
