/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 16:37:31 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/11/02 16:19:39 by iliasalmani      ###   ########.fr       */
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

 
#ifdef TEST_FT_PRINTF
#include <stdio.h>

int	main(void)
{
	ft_printf("%p\n", (void *)0);
	ft_printf("%p %p\n", (void *)0, (void *)0);
	return (0);
}
#endif

// cc -DTEST_FT_PRINTF ft_printf.c print_func2.c print_func.c -o test
