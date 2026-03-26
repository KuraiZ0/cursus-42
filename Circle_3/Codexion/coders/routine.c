/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 14:32:17 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/26 15:28:11 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	routine_pair(t_coder *coder)
{
	take_dongle(coder->left, coder);
	log_event(coder->params, coder->id, "has taken a dongle");
	take_dongle(coder->right, coder);
	log_event(coder->params, coder->id, "has taken a dongle");
	log_event(coder->params, coder->id, "is compiling");
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile = get_time_ms();
	coder->compile_count++;
	pthread_mutex_unlock(&coder->state_mutex);
	usleep(coder->params->time_to_compile * 1000);
	routine_utils(coder);
	release_dongle(coder->left, coder->params);
	release_dongle(coder->right, coder->params);
	log_event(coder->params, coder->id, "is debugging");
	usleep(coder->params->time_to_debug * 1000);
	log_event(coder->params, coder->id, "is refactoring");
	usleep(coder->params->time_to_refractor * 1000);
}

static void	routine_impair(t_coder *coder)
{
	take_dongle(coder->right, coder);
	log_event(coder->params, coder->id, "has taken a dongle");
	take_dongle(coder->left, coder);
	log_event(coder->params, coder->id, "has taken a dongle");
	log_event(coder->params, coder->id, "is compiling");
	pthread_mutex_lock(&coder->state_mutex);
	coder->last_compile = get_time_ms();
	coder->compile_count++;
	pthread_mutex_unlock(&coder->state_mutex);
	usleep(coder->params->time_to_compile * 1000);
	routine_utils(coder);
	release_dongle(coder->right, coder->params);
	release_dongle(coder->left, coder->params);
	log_event(coder->params, coder->id, "is debugging");
	usleep(coder->params->time_to_debug * 1000);
	log_event(coder->params, coder->id, "is refactoring");
	usleep(coder->params->time_to_refractor * 1000);
}

static void	routine_for_one(t_coder *coder)
{
	take_dongle(coder->left, coder);
	log_event(coder->params, coder->id, "has taken a dongle");
	while (get_stop(coder->params) == 0)
		usleep(1000);
	release_dongle(coder->left, coder->params);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	if ((coder->params->nb_coders) == 1)
		return (routine_for_one(coder), NULL);
	while (get_stop(coder->params) == 0)
	{
		if ((coder->id) % 2 == 0)
			routine_pair(coder);
		else
			routine_impair(coder);
	}
	return (NULL);
}
