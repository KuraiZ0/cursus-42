/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 15:20:35 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/20 17:20:49 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s1)
{
	char	*new;
	int		i;

	new = malloc(sizeof(char) * ft_strlen((char *)s1) + 1);
	if (new == NULL)
		return (NULL);
	i = 0;
	while (s1[i])
	{
		new[i] = s1[i];
		i++;
	}
	new[i] = '\0';
	return (new);
}

// #include <stdio.h>
// int	main(void)
// {
// 	char *str;
// 	char *dup;

// 	str = "50.000$ d'un coup";
// 	dup = ft_strdup(str);

// 	if (dup != NULL)
// 	{
// 		printf("%s\n", dup);
// 		free(dup);
// 	}
// 	return (0);