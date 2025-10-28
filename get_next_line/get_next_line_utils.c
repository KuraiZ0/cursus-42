/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 00:43:52 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/28 13:28:37 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"
#include <stdlib.h>

char	*read_stock(int fd, char *reste)
{
	int			readed;
	char		buf[BUFFER_SIZE + 1];
	char		*tmp;

	if (!reste)
		return (NULL);
	while (!(ft_strchr(reste, '\n')))
	{
		readed = read(fd, buf, BUFFER_SIZE);
		if (readed == -1)
		{
			free(reste);
			return (NULL);
		}
		if (!readed)
			return (reste);
		buf[readed] = '\0';
		tmp = ft_strjoin(reste, buf);
		free(reste);
		reste = tmp;
	}
	return (reste);
}

char	*extract_line(char **reste)
{
	char	*line;
	char	*new_reste;
	char	*newline_pos;
	int		index;

	if (!*reste || **reste == '\0')
		return (NULL);
	newline_pos = ft_strchr(*reste, '\n');
	if (newline_pos)
	{
		index = newline_pos - *reste + 1;
		line = ft_substr(*reste, 0, index);
		if (!line)
			return (NULL);
		new_reste = ft_substr(*reste, index, ft_strlen(*reste) - index);
		free(*reste);
		*reste = new_reste;
		return (line);
	}
	line = ft_strdup(*reste);
	free(*reste);
	*reste = NULL;
	return (line);
}

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*res;
	size_t	i;
	size_t	j;
	size_t	len1;
	size_t	len2;

	if (!s1 || !s2)
		return (NULL);
	len1 = ft_strlen(s1);
	len2 = ft_strlen(s2);
	res = malloc(sizeof(char) * (len1 + len2 + 1));
	if (!res)
		return (NULL);
	i = -1;
	while (++i < len1)
		res[i] = s1[i];
	j = -1;
	while (++j < len2)
		res[i + j] = s2[j];
	res[i + j] = '\0';
	return (res);
}

char	*ft_strchr(const char *str, int c)
{
	while (*str)
	{
		if (*str == (char)c)
			return ((char *)str);
		str++;
	}
	if (*str == (char)c)
		return ((char *)str);
	return (NULL);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	i;
	size_t	s_len;
	char	*tab;

	if (!s)
		return (NULL);
	i = 0;
	s_len = ft_strlen(s);
	if (start >= s_len)
		return (ft_strdup(""));
	if (len > s_len - start)
		len = s_len - start;
	tab = malloc(sizeof(char) * (len + 1));
	if (!tab)
		return (NULL);
	while (i < len)
	{
		tab[i] = s[start + i];
		i++;
	}
	tab[i] = '\0';
	return (tab);
}
