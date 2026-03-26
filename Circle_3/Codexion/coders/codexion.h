/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/18 13:45:00 by ialmani           #+#    #+#             */
/*   Updated: 2026/03/26 15:30:04 by ialmani          ###   ########.fr       */
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
	t_scheduler			scheduler;
	long				start_time;
	int					stop;
	int					finished_coders;
	pthread_mutex_t		log_mutex;
	pthread_mutex_t		stop_mutex;
}	t_params;

typedef struct s_request
{
	int		coder_id;
	long	priority;
}	t_request;

typedef struct s_heap
{
	t_request	*array;
	int			size;
	int			capacity;
}	t_heap;

typedef struct s_dongle
{
	int					available;
	long				available_at;
	pthread_mutex_t		t_mutex;
	pthread_cond_t		t_cond;
	t_heap				queue;
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
	struct s_coder		*left_coder;
	struct s_coder		*right_coder;
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
int			parsing(int ac, char **av);
int			valid_int(char *str);
long		get_time_ms(void);
void		log_event(t_params *params, int id, char *msg);
void		init_data(t_sim *sim);
int			allocate(t_sim *sim);
int			start_sim(t_sim *sim);
void		*coder_routine(void *arg);
int			get_stop(t_params *params);
void		set_stop(t_params *params);
void		*monitor_routine(void *arg);
void		cleanup(t_sim *sim);
void		release_dongle(t_dongle *dongle, t_params *params);
void		take_dongle(t_dongle *dongle, t_coder *coder);
void		swap(t_request *a, t_request *b);
int			init_heap(t_heap *heap, int capacity);
void		pop_utils(t_heap *heap, int i);
void		free_heap(t_heap *heap);
void		push_heap(t_heap *heap, int coder_id, long priority);
t_request	pop_heap(t_heap *heap);
void		routine_utils(t_coder *coder);

#endif