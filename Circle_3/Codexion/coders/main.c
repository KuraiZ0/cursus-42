/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 13:45:12 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/24 13:12:28 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	valid_int(char *str)
{
	int i;
	
	i = 0;
	while (str[i])
	{ 
		if (!(str[i] >= '0' && str[i] <= '9'))
			return (1);
		i++;
	}
	return (0);
}

int parsing(int ac, char **av)
{
	int i;
	
	i = 1;
	while (i < ac)
	{
		if (i == 8)
		{
			if (strcmp(av[i],"fifo") != 0 && strcmp(av[i], "edf") != 0)
				return (printf("Type edf or fifo is only authorized for the last arg."), 1);
		}
		else
		{
			if (valid_int(av[i]))
				return (printf("Arg %d isn't a valid int.", i), 1);
		}
		i++;
	}
	return (0);
}

void	manage_param(char **av, t_sim *sim)
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

	pthread_mutex_init(&sim->params.log_mutex, NULL);
	pthread_mutex_init(&sim->params.stop_mutex, NULL);

}


int main(int ac, char **av)
{
	t_params	params;
	t_sim		sim;
	if (ac != 9)
		return (printf("Error the number of arguments required is 8.\n"));
	if (parsing(ac, av))
		return (1);
	// parameter management
	manage_param(av, &sim);
	if (allocate(&sim) != 0)
		return (printf("Error of malloc\n"), 1);
	init_data(&sim);
	return (0);
	
}
