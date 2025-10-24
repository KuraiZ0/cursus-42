/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_func.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 12:38:26 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/24 12:16:52 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_ptr(unsigned long n)
{
	char	*base;
	char	buffer[17];
	int		i;
	int		count;

	base = "0123456789abcdef";
	i = 0;
	if (n == 0)
		return (write(1, "0x0", 3));
	while (n > 0)
	{
		buffer[i++] = base[n % 16];
		n /= 16;
	}
	count = write(1, "0x", 2);
	while (i--)
		count += write(1, &buffer[i], 1);
	return (count);
}

int	print_str(char *str)
{
	int	count;
	int	i;

	if (!str)
		return (write(1, "(null)", 6));
	count = 0;
	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
		count++;
	}
	return (count);
}

int	print_uns(unsigned int nb)
{
	char	buf[10];
	int		i;
	int		count;

	i = 0;
	count = 0;
	if (nb == 0)
		return (print_char('0'));
	while (nb > 0)
	{
		buf[i++] = (nb % 10) + '0';
		nb /= 10;
	}
	while (i-- > 0)
		count += print_char(buf[i]);
	return (count);
}

int	print_nbr(int nb)
{
	int	i;

	i = 0;
	if (nb == -2147483648)
	{
		write(1, "-2147483648", 11);
		return (11);
	}
	if (nb < 0)
	{
		i += print_char('-');
		nb = -nb;
	}
	if (nb >= 10)
		i += print_nbr(nb / 10);
	i += print_char(nb % 10 + '0');
	return (i);
}

int	print_hex(unsigned int n, int uppercase)
{
	char	*base;
	char	buffer[16];
	int		i;
	int		count;

	if (uppercase)
		base = "0123456789ABCDEF";
	else
		base = "0123456789abcdef";
	i = 0;
	if (n == 0)
		return (write(1, "0", 1));
	while (n > 0)
	{
		buffer[i++] = base[n % 16];
		n /= 16;
	}
	count = 0;
	while (i--)
		count += write(1, &buffer[i], 1);
	return (count);
}
