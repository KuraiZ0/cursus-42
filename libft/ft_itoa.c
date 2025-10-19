/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 15:34:05 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/19 18:21:49 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_numlen(long n)
{
	int	len;

	len = 0;
	if (n <= 0)
		len = 1;
	while (n)
	{
		n /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	char			*res;
	int				len;
	long			t;

	t = n;
	len = ft_numlen(t);
	res = malloc(sizeof(char) * (len + 1));
	if (!res)
		return (NULL);
	res[len] = '\0';
	if (t < 0)
	{
		res[0] = '-';
		t = -t;
	}
	if (t == 0)
		res[0] = '0';
	while (t)
	{
		res[--len] = (t % 10) + '0';
		t /= 10;
	}
	return (res);
}
