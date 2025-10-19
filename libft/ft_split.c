/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/17 16:50:25 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/18 17:02:54 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdio.h>

int	count_word(char const *s, char c)
{
	unsigned int	i;
	int				count;

	i = 0;
	count = 0;
	while (s[i])
	{
		if (s[i] != c && ((i == 0) || s[i - 1] == c))
			count++;
		i++;
	}
	return (count);
}

char	**ft_split(const char *s, char c)
{
	int				i;
	int				index;
	unsigned int	start;
	unsigned int	end;
	char			**res;

	if (!s)
		return (NULL);
	i = 0;
	res = malloc(sizeof(char *) * (count_word(s, c) + 1));
	index = 0;
	while (s[i])
	{
		if (s[i] != c && ((i == 0) || s[i - 1] == c))
			start = i;
		if (s[i] != c && (s[i + 1] == c || s[i + 1] == '\0'))
		{
			end = i;
			res[index] = ft_substr(s, start, end - start + 1);
			index++;
		}
		i++;
	}
	res[index] = NULL;
	return (res);
}
