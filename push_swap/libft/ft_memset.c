/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 11:01:11 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/16 11:10:10 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *ptr, int value, size_t count)
{
	size_t			i;
	unsigned char	*p;

	p = (unsigned char *)ptr;
	i = 0;
	while (i < count)
	{
		p[i] = (unsigned char)value;
		i++;
	}
	return (ptr);
}
/*
#include <stdio.h>

int	main(void)
{
	char	str[10];
	int		tab[5];

	str[10] = "Bonjour";
	printf("Avant: %s\n", str);
	ft_memset(str, 'A', 3);
	printf("Après: %s\n", str);
	tab[5] = {1, 2, 3, 4, 5};
	ft_memset(tab, 0, sizeof(int) * 2);
}
*/