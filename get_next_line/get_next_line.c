/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 22:12:14 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/27 23:30:59 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

char	*ft_strdup(const char *s1)
{
	char	*new;
	int		i;

	new = malloc(sizeof(char) * ft_strlen((char *)s1) + 1);
	if (!new || !s1)
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

char	*get_next_line(int fd)
{
	static char		*reste;
	char			*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	if (!reste)
		reste = ft_strdup("");
	reste = read_stock(fd, reste);
	if (!reste)
	{
		return (NULL);
	}
	line = extract_line(&reste);
	return (line);
}

// size_t	read(int fd, void *buffer, size_t nbyte)
// 	fd = open("./text.txt", O_RDONLY);