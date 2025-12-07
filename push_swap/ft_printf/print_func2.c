/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_func2.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 15:38:22 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/24 12:02:34 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_percent(void)
{
	write (1, "%", 1);
	return (1);
}

int	print_char(char c)
{
	write (1, &c, 1);
	return (1);
}

int	ft_search_sign(va_list *ap, char format)
{
	int	total;

	total = 0;
	if (format == 's')
		total += print_str(va_arg(*ap, char *));
	else if (format == 'c')
		total += print_char(va_arg(*ap, int));
	else if (format == 'p')
		total += print_ptr((unsigned long)va_arg(*ap, void *));
	else if (format == 'd' || format == 'i')
		total += print_nbr(va_arg(*ap, int));
	else if (format == '%')
		total += print_percent();
	else if (format == 'u')
		total += print_uns(va_arg(*ap, unsigned int));
	else if (format == 'x')
		total += print_hex(va_arg(*ap, unsigned int), 0);
	else if (format == 'X')
		total += print_hex(va_arg(*ap, unsigned int), 1);
	return (total);
}
