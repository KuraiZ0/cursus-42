/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 13:45:12 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/18 15:28:23 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	valid_int(char *str)
{
	int i = 0;
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
	for (int i = 1; i < ac; i++)
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
	}
	return (0);
}


int main(int ac, char **av)
{
	if (ac != 9)
		return (printf("Error the number of arguments required is 8.\n"));
	if (parsing(ac, av))
		return (1);
	return (0);
	
}
