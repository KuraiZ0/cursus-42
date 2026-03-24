/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 14:01:38 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/24 14:45:59 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long get_time_ms(void)
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000 + tv.tv_usec / 1000);
}

int    allocate(t_sim *sim)
{
	int nb;

	nb = sim->params.nb_coders;
	sim->coders = malloc(sizeof(t_coder) * nb);
	if (!sim->coders)
		return 1;
	sim->dongles = malloc(sizeof(t_dongle) * nb);
	if (!sim->dongles)
		return 1;
	sim->threads = malloc(sizeof(pthread_t) * nb);
	if (!sim->threads)
		return 1;
	return 0;
}

void    init_data(t_sim *sim)
{
	int i;

	i = 0;
	while (i < sim->params.nb_coders)
	{
		pthread_mutex_init(&sim->dongles[i].t_mutex, NULL);
		pthread_mutex_init(&sim->coders[i].state_mutex, NULL);

		pthread_cond_init(&sim->dongles[i].t_cond, NULL);
		sim->dongles[i].available = 1;
		
		sim->coders[i].id = i + 1;
		sim->coders[i].params = &sim->params;
		sim->coders[i].compile_count = 0;
		sim->coders[i].last_compile = sim->params.start_time;
		
		sim->coders[i].left = &sim->dongles[i];
		sim->coders[i].right = &sim->dongles[(i + 1) % sim->params.nb_coders];

		i++;
	}
}

int start_sim(t_sim *sim)
{
	int i;

	i = 0;
	while (i < sim->params.nb_coders)
	{
		if (pthread_create(&sim->threads[i], NULL, coder_routine, &sim->coders[i]) != 0)
			return (printf("Error on thread creation.\n"), 1);
		i++;
	}
	i = 0;
	while (i < sim->params.nb_coders)
	{
		pthread_join(sim->threads[i], NULL);
		i++;
	}
	return (0);
}