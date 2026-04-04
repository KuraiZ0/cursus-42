/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 13:45:12 by ialmani           #+#    #+#             */
/*   Updated: 2026/04/04 15:17:41 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	valid_int(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (!(str[i] >= '0' && str[i] <= '9'))
			return (1);
		i++;
	}
	return (0);
}

int	parsing(int ac, char **av)
{
	int	i;

	i = 1;
	while (i < ac)
	{
		if (i == 8)
		{
			if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
				return (printf("ERROR: edf or fifo for the last arg."), 1);
		}
		else
		{
			if (valid_int(av[i]))
				return (printf("ERROR: Arg %d isn't a valid int.", i), 1);
			if (i == 1 && atoi(av[i]) <= 0)
				return (printf("ERROR: nb_coders must be more than 0."), 1);
		}
		i++;
	}
	return (0);
}

static void	manage_param(char **av, t_sim *sim)
{
	sim->params.nb_coders = atoi(av[1]);
	sim->params.time_to_burnout = atoi(av[2]);
	sim->params.time_to_compile = atoi(av[3]);
	sim->params.time_to_debug = atoi(av[4]);
	sim->params.time_to_refractor = atoi(av[5]);
	sim->params.nb_compiles = atoi(av[6]);
	sim->params.dongle_cd = atoi(av[7]);
	if (strcmp(av[8], "edf") == 0)
		sim->params.scheduler = 1;
	else
		sim->params.scheduler = 0;
	sim->params.start_time = get_time_ms();
	sim->params.stop = 0;
	sim->params.finished_coders = 0;
	pthread_mutex_init(&sim->params.log_mutex, NULL);
	pthread_mutex_init(&sim->params.stop_mutex, NULL);
}

int	start_sim(t_sim *sim)
{
	int	i;

	i = 0;
	if (pthread_create(&sim->monitor_thread, NULL, monitor_routine, sim) != 0)
		return (printf("Error on monitor thread creation.\n"), 1);
	while (i < sim->params.nb_coders)
	{
		if (pthread_create(&sim->threads[i], NULL, coder_routine,
				&sim->coders[i]) != 0)
			return (printf("Error on thread creation.\n"), 1);
		i++;
	}
	i = 0;
	while (i < sim->params.nb_coders)
	{
		pthread_join(sim->threads[i], NULL);
		i++;
	}
	pthread_join(sim->monitor_thread, NULL);
	return (0);
}

int	main(int ac, char **av)
{
	t_sim		sim;

	if (ac != 9)
		return (printf("Error: 8 arguments are strictly required\n"));
	if (parsing(ac, av))
		return (1);
	manage_param(av, &sim);
	if (allocate(&sim) != 0)
		return (printf("Error of malloc\n"), 1);
	init_data(&sim);
	start_sim(&sim);
	cleanup(&sim);
	return (0);
}
