/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 16:37:31 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/24 11:58:30 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_printf(const char *format, ...)
{
	int				total;
	va_list			ap;

	total = 0;
	va_start(ap, format);
	while (*format)
	{
		if (*format == '%')
		{
			format++;
			if (*format)
			{
				total += ft_search_sign(&ap, *format);
				format++;
			}
		}
		else
		{
			write (1, format, 1);
			total++;
			format++;
		}
	}
	va_end(ap);
	return (total);
}
