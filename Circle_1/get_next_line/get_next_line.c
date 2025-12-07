/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 22:12:14 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/01 22:22:06 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

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
		return (free(*reste), *reste = NULL, NULL);
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

/*
#include <stdio.h>
#include <fcntl.h>

int main()
{
    int fd;
    char *line;

    fd = open("./test.txt", O_RDONLY);
    if (fd < 0)
    {
        perror("Error opening file");
        return 1;
    }

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line); // line already has \n if present
        free(line);         // free each line after using it
    }

    close(fd);
    return 0;
}
*/