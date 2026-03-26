/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/26 09:49:55 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/26 11:57:25 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	push_heap(t_heap *heap, int coder_id, long priority)
{
	int	i;
	int	parent;

	if (heap->size >= heap->capacity)
		return ;
	i = heap->size;
	heap->array[i].coder_id = coder_id;
	heap->array[i].priority = priority;
	heap->size++;
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (heap->array[i].priority < heap->array[parent].priority)
		{
			swap(&heap->array[i], &heap->array[parent]);
			i = parent;
		}
		else
			break ;
	}
}

t_request	pop_heap(t_heap *heap)
{
	t_request	tmp;
	int			i;

	tmp.coder_id = -1;
	tmp.priority = -1;
	if (heap->size == 0)
		return (tmp);
	i = heap->size - 1;
	tmp = heap->array[0];
	heap->size--;
	swap(&heap->array[i], &heap->array[0]);
	i = 0;
	pop_utils(heap, i);
	return (tmp);
}

