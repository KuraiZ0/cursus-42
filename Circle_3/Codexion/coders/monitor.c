/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 14:01:33 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/25 13:18:50 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	monitor_utils(long now, t_sim *sim, int i)
{
	long	last_co;

	pthread_mutex_lock(&sim->coders[i].state_mutex);
	last_co = sim->coders[i].last_compile;
	pthread_mutex_unlock(&sim->coders[i].state_mutex);
	if (now - last_co > sim->params.time_to_burnout)
		return (1);
	return (0);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	int		i;
	long	now;

	sim = (t_sim *)arg;
	while (get_stop(&sim->params) == 0)
	{
		now = get_time_ms();
		i = 0;
		while (i < sim->params.nb_coders)
		{
			if (monitor_utils(now, sim, i) == 1)
			{
				log_event(&sim->params, sim->coders[i].id, "burned out");
				set_stop(&sim->params);
				return (NULL);
			}
			i++;
		}
		usleep(1000);
	}
	return (NULL);
}
