/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 14:01:29 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/24 10:50:34 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void    log_event(t_sim *sim, int id, char *msg)
{
    pthread_mutex_lock(&sim->params.log_mutex);
    long time_now = get_time_ms();
    long time_atm = time_now - sim->params.start_time;
    printf("%ld %d %s\n", time_atm, id, msg);
    pthread_mutex_unlock(&sim->params.log_mutex);
}