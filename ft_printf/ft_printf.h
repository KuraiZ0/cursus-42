/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 11:16:01 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/24 11:30:35 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include "libft/libft.h"
# include <stdarg.h>
# include <unistd.h>

int		ft_printf(const char *format, ...);
int		print_hex(unsigned int n, int uppercase);
int		print_nbr(int nb);
int		print_uns(unsigned int nb);
int		print_str(char *str);
int		print_percent(void);
int		print_char(char c);
int		ft_search_sign(va_list *ap, char format);
int		print_ptr(unsigned long n);

#endif