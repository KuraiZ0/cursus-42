/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 12:19:38 by iliasalmani       #+#    #+#             */
/*   Updated: 2025/10/24 12:19:39 by iliasalmani      ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <limits.h>

// Déclarez votre ft_printf ici
int ft_printf(const char *format, ...);

void test_section(const char *title) {
    printf("\n========== %s ==========\n", title);
}

int main(void) {
    int ret1, ret2;
    
    test_section("TEST CARACTERES (%c)");
    ret1 = printf("printf    : [%c] [%c] [%c]\n", 'A', '0', '\n');
    ret2 = ft_printf("ft_printf : [%c] [%c] [%c]\n", 'A', '0', '\n');
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST CHAINES (%s)");
    ret1 = printf("printf    : [%s] [%s] [%s]\n", "Hello", "", "World!");
    ret2 = ft_printf("ft_printf : [%s] [%s] [%s]\n", "Hello", "", "World!");
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    ret1 = printf("printf    : NULL -> [%s]\n", (char *)NULL);
    ret2 = ft_printf("ft_printf : NULL -> [%s]\n", (char *)NULL);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST POINTEURS (%p)");
    int x = 42;
    ret1 = printf("printf    : [%p] [%p] [%p]\n", &x, (void *)0, (void *)0xDEADBEEF);
    ret2 = ft_printf("ft_printf : [%p] [%p] [%p]\n", &x, (void *)0, (void *)0xDEADBEEF);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST ENTIERS (%d et %i)");
    ret1 = printf("printf    : [%d] [%d] [%d] [%d]\n", 42, -42, 0, INT_MAX);
    ret2 = ft_printf("ft_printf : [%d] [%d] [%d] [%d]\n", 42, -42, 0, INT_MAX);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    ret1 = printf("printf    : [%i] [%i] [%i]\n", INT_MIN, INT_MAX, INT_MIN);
    ret2 = ft_printf("ft_printf : [%i] [%i] [%i]\n", INT_MIN, INT_MAX, INT_MIN);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST UNSIGNED (%u)");
    ret1 = printf("printf    : [%u] [%u] [%u]\n", 0, 42, UINT_MAX);
    ret2 = ft_printf("ft_printf : [%u] [%u] [%u]\n", 0, 42, UINT_MAX);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    ret1 = printf("printf    : [%u]\n", -1);
    ret2 = ft_printf("ft_printf : [%u]\n", -1);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST HEXADECIMAL MINUSCULE (%x)");
    ret1 = printf("printf    : [%x] [%x] [%x] [%x]\n", 0, 42, 255, UINT_MAX);
    ret2 = ft_printf("ft_printf : [%x] [%x] [%x] [%x]\n", 0, 42, 255, UINT_MAX);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST HEXADECIMAL MAJUSCULE (%X)");
    ret1 = printf("printf    : [%X] [%X] [%X] [%X]\n", 0, 42, 255, UINT_MAX);
    ret2 = ft_printf("ft_printf : [%X] [%X] [%X] [%X]\n", 0, 42, 255, UINT_MAX);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST POURCENTAGE (%%)");
    ret1 = printf("printf    : [%%] [100%%] [%%d]\n");
    ret2 = ft_printf("ft_printf : [%%] [100%%] [%%d]\n");
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST MIXTE");
    ret1 = printf("printf    : Char:%c Str:%s Ptr:%p Int:%d Hex:%x %%\n", 
                  'X', "test", &x, -123, 0xABC);
    ret2 = ft_printf("ft_printf : Char:%c Str:%s Ptr:%p Int:%d Hex:%x %%\n", 
                     'X', "test", &x, -123, 0xABC);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    test_section("TEST CAS LIMITES");
    ret1 = printf("printf    : [%d %d %d]\n", 0, -0, +0);
    ret2 = ft_printf("ft_printf : [%d %d %d]\n", 0, -0, +0);
    printf("Retours: %d vs %d\n", ret1, ret2);
    
    ret1 = printf("printf    : ");
    ret2 = ft_printf("ft_printf : ");
    printf("\nRetours vide: %d vs %d\n", ret1, ret2);
    
    test_section("TEST VALEURS DE RETOUR");
    ret1 = printf("Test");
    printf(" -> retour: %d\n", ret1);
    ret2 = ft_printf("Test");
    printf(" -> retour: %d\n", ret2);
    
    return 0;
}