/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 15:22:21 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/16 09:54:35 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(const char *str)
{
	int	i;
	int	signe;
	int	number;

	i = 0;
	signe = 1;
	number = 0;
	while ((str[i] >= 9 && str[i] <= 13) || str[i] == 32)
		i++;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			signe = -1;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		number = number * 10 + (str[i] - '0');
		i++;
	}
	return (number * signe);
}
/*
#include <stdio.h>

printf("%d\n", ft_atoi("   -1234abc")); // -1234
printf("%d\n", ft_atoi(" +42"));        // 42
printf("%d\n", ft_atoi("  0000123"));   // 123
printf("%d\n", ft_atoi("abc"));         // 0
*/