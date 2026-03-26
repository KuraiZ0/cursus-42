/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clean.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/26 11:56:43 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/26 11:57:33 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	cleanup(t_sim *sim)
{
	int	i;

	i = 0;
	pthread_mutex_destroy(&sim->params.log_mutex);
	pthread_mutex_destroy(&sim->params.stop_mutex);
	while (i < sim->params.nb_coders)
	{
		pthread_mutex_destroy(&sim->coders[i].state_mutex);
		i++;
	}
	i = 0;
	while (i < sim->params.nb_coders)
	{
		pthread_mutex_destroy(&sim->dongles[i].t_mutex);
		pthread_cond_destroy(&sim->dongles[i].t_cond);
		free_heap(&sim->dongles[i].queue);
		i++;
	}
	free(sim->coders);
	free(sim->dongles);
	free(sim->threads);
}

void	free_heap(t_heap *heap)
{
	if (heap->array)
		free(heap->array);
}
