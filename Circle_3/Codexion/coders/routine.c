/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 14:32:17 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/24 14:58:45 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*coder_routine(void *arg)
{
	t_coder	*coder;
	coder = (t_coder *)arg;

	while ((coder->params->stop_mutex) == 0)
	{
		if ((coder->id) % 2 == 0)
		{
			pthread_mutex_lock(&coder->left->t_mutex);
			pthread_mutex_lock(&coder->right->t_mutex);
		}
		else
		{	
			pthread_mutex_lock(&coder->left->t_mutex);
			pthread_mutex_lock(&coder->right->t_mutex);
		}
			
		pthread_mutex_unlock(&coder->left->t_mutex);
		pthread_mutex_unlock(&coder->right->t_mutex);
	}
	return (NULL);
}
