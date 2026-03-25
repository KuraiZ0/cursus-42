/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 13:45:00 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/25 13:40:45 by ialmani          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

/*|=== INCLUDE PART ===|*/
# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>

/*|=== STRUCT DECLARATION ===|*/
typedef enum e_scheduler
{
	FIFO,
	EDF
}	t_scheduler;

typedef struct s_params
{
	int					nb_coders;
	long				time_to_burnout;
	long				time_to_compile;
	long				time_to_debug;
	long				time_to_refractor;
	int					nb_compiles;
	long				dongle_cd;
	int					scheduler;
	long				start_time;
	int					stop;
	pthread_mutex_t		log_mutex;
	pthread_mutex_t		stop_mutex;
}	t_params;

typedef struct s_dongle
{
	int					available;
	long				available_at;
	pthread_mutex_t		t_mutex;
	pthread_cond_t		t_cond;
}	t_dongle;

typedef struct s_coder
{
	int					id;
	t_params			*params;
	t_dongle			*left;
	t_dongle			*right;
	long				last_compile;
	int					compile_count;
	pthread_mutex_t		state_mutex;
}	t_coder;

typedef struct s_sim
{
	t_params	params;
	t_coder		*coders;
	pthread_t	*threads;
	pthread_t	monitor_thread;
	t_dongle	*dongles;
}	t_sim;

/*|=== FUNCTION PROTOTYPE ===|*/
int		parsing(int ac, char **av);
int		valid_int(char *str);
long	get_time_ms(void);
void	log_event(t_params *params, int id, char *msg);
void	init_data(t_sim *sim);
int		allocate(t_sim *sim);
int		start_sim(t_sim *sim);
void	*coder_routine(void *arg);
int		get_stop(t_params *params);
void	set_stop(t_params *params);
void	*monitor_routine(void *arg);
void	cleanup(t_sim *sim);

#endif