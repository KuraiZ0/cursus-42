/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 14:01:29 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/26 14:59:18 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	log_event(t_params *params, int id, char *msg)
{
	long	time_now;
	long	time_atm;

	pthread_mutex_lock(&params->log_mutex);
	if (params->stop == 1)
	{
		pthread_mutex_unlock(&params->log_mutex);
		return ;
	}
	time_now = get_time_ms();
	time_atm = time_now - params->start_time;
	printf("%ld %d %s\n", time_atm, id, msg);
	pthread_mutex_unlock(&params->log_mutex);
}

void	set_stop(t_params *params)
{
	pthread_mutex_lock(&params->stop_mutex);
	params->stop = 1;
	pthread_mutex_unlock(&params->stop_mutex);
}

void	take_dongle(t_dongle *dongle, t_coder *coder)
{
	long	priority;

	priority = 0;
	pthread_mutex_lock(&dongle->t_mutex);
	if (coder->params->scheduler == FIFO)
		priority = get_time_ms();
	else if (coder->params->scheduler == EDF)
		priority = coder->last_compile + coder->params->time_to_burnout;
	push_heap(&dongle->queue, coder->id, priority);
	while (((dongle->available) == 0) || dongle
		->queue.array[0].coder_id != coder->id || get_time_ms()
		< dongle->available_at)
	{
		if (dongle->available == 0)
			pthread_cond_wait(&dongle->t_cond, &dongle->t_mutex);
		else
		{
			pthread_mutex_unlock(&dongle->t_mutex);
			usleep(1000);
			pthread_mutex_lock(&dongle->t_mutex);
		}
	}
	dongle->available = 0;
	pop_heap(&dongle->queue);
	pthread_mutex_unlock(&dongle->t_mutex);
}

void	release_dongle(t_dongle *dongle, t_params *params)
{
	pthread_mutex_lock(&dongle->t_mutex);
	dongle->available_at = get_time_ms() + params->dongle_cd;
	dongle->available = 1;
	pthread_cond_broadcast(&dongle->t_cond);
	pthread_mutex_unlock(&dongle->t_mutex);
}

void	routine_utils(t_coder *coder)
{
	if (coder->params->nb_compiles > 0 && coder
		->compile_count == coder->params->nb_compiles)
	{
		pthread_mutex_lock(&coder->params->stop_mutex);
		coder->params->finished_coders++;
		if (coder->params->finished_coders == coder->params->nb_coders)
			coder->params->stop = 1;
		pthread_mutex_unlock(&coder->params->stop_mutex);
	}
}