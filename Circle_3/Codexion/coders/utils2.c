/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 14:01:29 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/25 13:37:02 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	log_event(t_params *params, int id, char *msg)
{
	long	time_now;
	long	time_atm;

	pthread_mutex_lock(&params->log_mutex);
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
		i++;
	}
	free(sim->coders);
	free(sim->dongles);
	free(sim->threads);
}
