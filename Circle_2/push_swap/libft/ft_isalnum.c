/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 10:11:58 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/16 10:38:13 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isalnum(int character)
{
	if ((character >= 48 && character <= 57) || (character >= 65
			&& character <= 90) || (character >= 97 && character <= 122))
		return (1);
	return (0);
}

/*
int	main(void)
{
	printf("%d\n", ft_isalnum('a'));
	printf("%d\n", ft_isalnum('Z'));
	printf("%d\n", ft_isalnum('5'));
	printf("%d\n", ft_isalnum('!'));
	printf("%d\n", ft_isalnum(' '));
}
*/
