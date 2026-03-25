/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 14:32:17 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/25 13:18:04 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	routine_pair(t_coder *coder)
{
	pthread_mutex_lock(&coder->left->t_mutex);
	log_event(coder->params, coder->id, "has taken left dongle.");
	pthread_mutex_lock(&coder->right->t_mutex);
	log_event(coder->params, coder->id, "has taken right dongle.");
	log_event(coder->params, coder->id, "is compiling.");
	usleep(coder->params->time_to_compile * 1000);
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile = get_time_ms();
	coder->compile_count++;
	pthread_mutex_unlock(&coder->state_mutex);
	if (coder->compile_count >= coder->params->nb_compiles)
	{
		pthread_mutex_lock(&coder->params->stop_mutex);
		coder->params->stop = 1;
		pthread_mutex_unlock(&coder->params->stop_mutex);
	}
	pthread_mutex_unlock(&coder->left->t_mutex);
	pthread_mutex_unlock(&coder->right->t_mutex);
	log_event(coder->params, coder->id, "is debugging.");
	usleep(coder->params->time_to_debug * 1000);
	log_event(coder->params, coder->id, "is refactoring.");
	usleep(coder->params->time_to_refractor * 1000);
}

static void	routine_impair(t_coder *coder)
{
	pthread_mutex_lock(&coder->right->t_mutex);
	log_event(coder->params, coder->id, "has taken right dongle.");
	pthread_mutex_lock(&coder->left->t_mutex);
	log_event(coder->params, coder->id, "has taken left dongle.");
	log_event(coder->params, coder->id, "is compiling.");
	usleep(coder->params->time_to_compile * 1000);
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile = get_time_ms();
	coder->compile_count++;
	pthread_mutex_unlock(&coder->state_mutex);
	if (coder->compile_count >= coder->params->nb_compiles)
	{
		pthread_mutex_lock(&coder->params->stop_mutex);
		coder->params->stop = 1;
		pthread_mutex_unlock(&coder->params->stop_mutex);
	}
	pthread_mutex_unlock(&coder->right->t_mutex);
	pthread_mutex_unlock(&coder->left->t_mutex);
	log_event(coder->params, coder->id, "is debugging.");
	usleep(coder->params->time_to_debug * 1000);
	log_event(coder->params, coder->id, "is refactoring.");
	usleep(coder->params->time_to_refractor * 1000);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (get_stop(coder->params) == 0)
	{
		if ((coder->id) % 2 == 0)
		{
			routine_pair(coder);
		}
		else
		{
			routine_impair(coder);
		}
	}
	return (NULL);
}
