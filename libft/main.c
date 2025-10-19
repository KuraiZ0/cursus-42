/* *******	******************************************************************* */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_test.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 by iliasalmani              #+#    #+#             */
/*   Updated: 2025/10/19 by iliasalmani              ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdio.h>
#include <string.h>

char test_map(unsigned int i, char c)
{
	return c + i;
}

void test_iter(unsigned int i, char *c)
{
	*c = *c + i;
}

void print_content(void *content)
{
	printf("  -> %d\n", *(int*)content);
}

void *duplicate_int(void *content)
{
	int *new = malloc(sizeof(int));
	*new = *(int*)content * 2;
	return new;
}

void del_int(void *content)
{
	free(content);
}

#define SEP printf("\n" "========================================" "\n")

void test_part1_is_functions(void)
{
	printf("\n=== PARTIE 1: Fonctions is* ===\n");
	
	// ft_isalpha
	printf("\n--- ft_isalpha ---\n");
	printf("'a': %d\n", ft_isalpha('a'));
	printf("'Z': %d\n", ft_isalpha('Z'));
	printf("'5': %d\n", ft_isalpha('5'));
	printf("'!': %d\n", ft_isalpha('!'));
	
	// ft_isdigit
	printf("\n--- ft_isdigit ---\n");
	printf("'0': %d\n", ft_isdigit('0'));
	printf("'9': %d\n", ft_isdigit('9'));
	printf("'a': %d\n", ft_isdigit('a'));
	
	// ft_isalnum
	printf("\n--- ft_isalnum ---\n");
	printf("'a': %d\n", ft_isalnum('a'));
	printf("'5': %d\n", ft_isalnum('5'));
	printf("'!': %d\n", ft_isalnum('!'));
	
	// ft_isascii
	printf("\n--- ft_isascii ---\n");
	printf("0: %d\n", ft_isascii(0));
	printf("127: %d\n", ft_isascii(127));
	printf("128: %d\n", ft_isascii(128));
	printf("-1: %d\n", ft_isascii(-1));
	
	// ft_isprint
	printf("\n--- ft_isprint ---\n");
	printf("' ' (32): %d\n", ft_isprint(' '));
	printf("'~' (126): %d\n", ft_isprint('~'));
	printf("31: %d\n", ft_isprint(31));
	printf("127: %d\n", ft_isprint(127));
	printf("'A': %d\n", ft_isprint('A'));
}

void test_part1_str_functions(void)
{
	printf("\n=== PARTIE 1: Fonctions str* ===\n");
	
	// ft_strlen
	printf("\n--- ft_strlen ---\n");
	printf("\"Hello\": %zu\n", ft_strlen("Hello"));
	printf("\"\": %zu\n", ft_strlen(""));
	printf("\"42 Network\": %zu\n", ft_strlen("42 Network"));
	
	// ft_toupper
	printf("\n--- ft_toupper ---\n");
	printf("'a' -> '%c'\n", ft_toupper('a'));
	printf("'Z' -> '%c'\n", ft_toupper('Z'));
	printf("'5' -> '%c'\n", ft_toupper('5'));
	
	// ft_tolower
	printf("\n--- ft_tolower ---\n");
	printf("'A' -> '%c'\n", ft_tolower('A'));
	printf("'z' -> '%c'\n", ft_tolower('z'));
	printf("'5' -> '%c'\n", ft_tolower('5'));
	
	// ft_strchr
	printf("\n--- ft_strchr ---\n");
	char str1[] = "Hello World";
	char *result = ft_strchr(str1, 'W');
	printf("Cherche 'W' dans \"%s\": %s\n", str1, result);
	result = ft_strchr(str1, 'z');
	printf("Cherche 'z' dans \"%s\": %s\n", str1, result ? result : "(null)");
	result = ft_strchr(str1, '\0');
	printf("Cherche '\\0' dans \"%s\": trouvé=%d\n", str1, result != NULL);
	
	// ft_strrchr
	printf("\n--- ft_strrchr ---\n");
	result = ft_strrchr(str1, 'o');
	printf("Cherche dernier 'o' dans \"%s\": %s\n", str1, result);
	result = ft_strrchr(str1, 'H');
	printf("Cherche dernier 'H' dans \"%s\": %s\n", str1, result);
	
	// ft_strncmp
	printf("\n--- ft_strncmp ---\n");
	printf("\"Hello\" vs \"Hello\" (5): %d\n", ft_strncmp("Hello", "Hello", 5));
	printf("\"Hello\" vs \"Hella\" (5): %d\n", ft_strncmp("Hello", "Hella", 5));
	printf("\"Hello\" vs \"World\" (5): %d\n", ft_strncmp("Hello", "World", 5));
	printf("\"abc\" vs \"abcdef\" (3): %d\n", ft_strncmp("abc", "abcdef", 3));
	
	// ft_strnstr
	printf("\n--- ft_strnstr ---\n");
	result = ft_strnstr("Hello World", "World", 11);
	printf("Cherche \"World\" dans \"Hello World\" (11): %s\n", result);
	result = ft_strnstr("Hello World", "World", 5);
	printf("Cherche \"World\" dans \"Hello World\" (5): %s\n", result ? result : "(null)");
	result = ft_strnstr("lorem ipsum dolor sit amet", "dolor", 20);
	printf("Cherche \"dolor\" dans \"lorem ipsum dolor sit amet\" (20): %s\n", result);
}

void test_part1_mem_functions(void)
{
	printf("\n=== PARTIE 1: Fonctions mem* ===\n");
	
	// ft_memset
	printf("\n--- ft_memset ---\n");
	char buffer1[10];
	ft_memset(buffer1, 'A', 5);
	buffer1[5] = '\0';
	printf("memset 'A' x5: \"%s\"\n", buffer1);
	
	// ft_bzero
	printf("\n--- ft_bzero ---\n");
	char buffer2[10] = "Hello";
	printf("Avant bzero: \"%s\"\n", buffer2);
	ft_bzero(buffer2, 3);
	printf("Après bzero(3): premiers bytes = %d, %d, %d\n", 
		   buffer2[0], buffer2[1], buffer2[2]);
	
	// ft_memcpy
	printf("\n--- ft_memcpy ---\n");
	char src[] = "Hello";
	char dest[10];
	ft_memcpy(dest, src, 6);
	printf("memcpy \"%s\" -> \"%s\"\n", src, dest);
	
	// ft_memmove
	printf("\n--- ft_memmove ---\n");
	char str2[] = "HelloWorld";
	printf("Avant memmove: \"%s\"\n", str2);
	ft_memmove(str2 + 2, str2, 5);
	printf("Après memmove overlap: \"%s\"\n", str2);
	
	// ft_memchr
	printf("\n--- ft_memchr ---\n");
	char str3[] = "Hello World";
	char *ptr = ft_memchr(str3, 'W', strlen(str3));
	printf("memchr 'W' dans \"%s\": %s\n", str3, ptr);
	ptr = ft_memchr(str3, 'o', 5);
	printf("memchr 'o' dans 5 premiers bytes: %s\n", ptr);
	
	// ft_memcmp
	printf("\n--- ft_memcmp ---\n");
	printf("memcmp \"Hello\" vs \"Hello\" (5): %d\n", 
		   ft_memcmp("Hello", "Hello", 5));
	printf("memcmp \"Hello\" vs \"Hella\" (5): %d\n", 
		   ft_memcmp("Hello", "Hella", 5));
	printf("memcmp \"abc\" vs \"abd\" (3): %d\n", 
		   ft_memcmp("abc", "abd", 3));
}

void test_part1_convert_alloc(void)
{
	printf("\n=== PARTIE 1: Conversion et Allocation ===\n");
	
	// ft_atoi
	printf("\n--- ft_atoi ---\n");
	printf("\"42\": %d\n", ft_atoi("42"));
	printf("\"  -123\": %d\n", ft_atoi("  -123"));
	printf("\"  +456\": %d\n", ft_atoi("  +456"));
	printf("\"  \\t\\n\\r\\v\\f123\": %d\n", ft_atoi("  \t\n\r\v\f123"));
	printf("\"0\": %d\n", ft_atoi("0"));
	printf("\"2147483647\": %d\n", ft_atoi("2147483647"));
	printf("\"-2147483648\": %d\n", ft_atoi("-2147483648"));
	
	// ft_calloc
	printf("\n--- ft_calloc ---\n");
	int *arr = (int *)ft_calloc(5, sizeof(int));
	if (arr)
	{
		printf("calloc 5 ints: ");
		for (int i = 0; i < 5; i++)
			printf("%d ", arr[i]);
		printf("\n");
		free(arr);
	}
	
// ft_strdup
	printf("\n--- ft_strdup ---\n");
	char *dup = ft_strdup("Hello World");
	printf("strdup \"Hello World\": \"%s\"\n", dup);
	printf("Adresses différentes? %s\n",
		   strcmp(dup, "Hello World") != 0 ? "Oui" : "Non");
	free(dup);
	
	// ft_strlcpy
	printf("\n--- ft_strlcpy ---\n");
	char dst1[10];
	size_t ret = ft_strlcpy(dst1, "Hello World", 10);
	printf("strlcpy \"Hello World\" (size=10): \"%s\" (ret=%zu)\n", dst1, ret);
	ret = ft_strlcpy(dst1, "Hi", 10);
	printf("strlcpy \"Hi\" (size=10): \"%s\" (ret=%zu)\n", dst1, ret);
	
	// ft_strlcat
	printf("\n--- ft_strlcat ---\n");
	char dst2[20] = "Hello ";
	ret = ft_strlcat(dst2, "World", 20);
	printf("strlcat \"Hello \" + \"World\" (size=20): \"%s\" (ret=%zu)\n", 
		   dst2, ret);
}

void test_part2_functions(void)
{
	printf("\n=== PARTIE 2: Fonctions Supplémentaires ===\n");
	
	// ft_substr
	printf("\n--- ft_substr ---\n");
	char *sub = ft_substr("Hello World", 6, 5);
	printf("substr(\"Hello World\", 6, 5): \"%s\"\n", sub);
	free(sub);
	sub = ft_substr("Hello", 2, 10);
	printf("substr(\"Hello\", 2, 10): \"%s\"\n", sub);
	free(sub);
	
	// ft_strjoin
	printf("\n--- ft_strjoin ---\n");
	char *joined = ft_strjoin("Hello ", "World");
	printf("strjoin \"Hello \" + \"World\": \"%s\"\n", joined);
	free(joined);
	joined = ft_strjoin("", "test");
	printf("strjoin \"\" + \"test\": \"%s\"\n", joined);
	free(joined);
	
	// ft_strtrim
	printf("\n--- ft_strtrim ---\n");
	char *trimmed = ft_strtrim("   Hello   ", " ");
	printf("strtrim \"   Hello   \" (set=' '): \"%s\"\n", trimmed);
	free(trimmed);
	trimmed = ft_strtrim("xxHelloxx", "x");
	printf("strtrim \"xxHelloxx\" (set='x'): \"%s\"\n", trimmed);
	free(trimmed);
	trimmed = ft_strtrim("   \t\n", " \t\n");
	printf("strtrim \"   \\t\\n\" (set=' \\t\\n'): \"%s\"\n", trimmed);
	free(trimmed);
	
	// ft_split
	printf("\n--- ft_split ---\n");
	char **split = ft_split("Hello,World,42,School", ',');
	if (split)
	{
		printf("split \"Hello,World,42,School\" (','):\n");
		for (int i = 0; split[i]; i++)
		{
			printf("  [%d]: \"%s\"\n", i, split[i]);
			free(split[i]);
		}
		free(split);
	}
	
	split = ft_split("   Hello   World   ", ' ');
	if (split)
	{
		printf("split \"   Hello   World   \" (' '):\n");
		for (int i = 0; split[i]; i++)
		{
			printf("  [%d]: \"%s\"\n", i, split[i]);
			free(split[i]);
		}
		free(split);
	}
	
	// ft_itoa
	printf("\n--- ft_itoa ---\n");
	char *num;
	num = ft_itoa(0);
	printf("itoa(0): \"%s\"\n", num);
	free(num);
	num = ft_itoa(42);
	printf("itoa(42): \"%s\"\n", num);
	free(num);
	num = ft_itoa(-42);
	printf("itoa(-42): \"%s\"\n", num);
	free(num);
	num = ft_itoa(2147483647);
	printf("itoa(2147483647): \"%s\"\n", num);
	free(num);
	num = ft_itoa(-2147483648);
	printf("itoa(-2147483648): \"%s\"\n", num);
	free(num);
	
	// ft_strmapi
	printf("\n--- ft_strmapi ---\n");
	char *mapped = ft_strmapi("abc", test_map);
	printf("strmapi \"abc\" (c+i): \"%s\"\n", mapped);
	free(mapped);
	
	// ft_striteri
	printf("\n--- ft_striteri ---\n");
	char str_iter[] = "abc";
	printf("Avant striteri: \"%s\"\n", str_iter);
	ft_striteri(str_iter, test_iter);
	printf("Après striteri (c+i): \"%s\"\n", str_iter);
}

void test_part2_fd_functions(void)
{
	printf("\n=== PARTIE 2: Fonctions fd ===\n");
	
	// ft_putchar_fd
	printf("\n--- ft_putchar_fd ---\n");
	printf("Affiche 'A': ");
	ft_putchar_fd('A', 1);
	printf("\n");
	
	// ft_putstr_fd
	printf("\n--- ft_putstr_fd ---\n");
	printf("Affiche \"Hello World\": ");
	ft_putstr_fd("Hello World", 1);
	printf("\n");
	
	// ft_putendl_fd
	printf("\n--- ft_putendl_fd ---\n");
	printf("Affiche \"Hello\" + newline:\n");
	ft_putendl_fd("Hello", 1);
	
	// ft_putnbr_fd
	printf("\n--- ft_putnbr_fd ---\n");
	printf("Affiche 42: ");
	ft_putnbr_fd(42, 1);
	printf("\nAffiche -42: ");
	ft_putnbr_fd(-42, 1);
	printf("\nAffiche 0: ");
	ft_putnbr_fd(0, 1);
	printf("\nAffiche 2147483647: ");
	ft_putnbr_fd(2147483647, 1);
	printf("\nAffiche -2147483648: ");
	ft_putnbr_fd(-2147483648, 1);
	printf("\n");
}

void test_bonus_functions(void)
{
	printf("\n=== BONUS: Fonctions Listes ===\n");
	
	// ft_lstnew
	printf("\n--- ft_lstnew ---\n");
	int *data1 = malloc(sizeof(int));
	*data1 = 42;
	t_list *node1 = ft_lstnew(data1);
	printf("lstnew avec data=42: content=%d, next=%s\n", 
		   *(int*)node1->content, node1->next ? "non-NULL" : "NULL");
	
	// ft_lstadd_front
	printf("\n--- ft_lstadd_front ---\n");
	t_list *list = NULL;
	ft_lstadd_front(&list, node1);
	printf("Liste après add_front: content=%d\n", *(int*)list->content);
	
	int *data2 = malloc(sizeof(int));
	*data2 = 21;
	t_list *node2 = ft_lstnew(data2);
	ft_lstadd_front(&list, node2);
	printf("Liste après 2ème add_front: content=%d\n", *(int*)list->content);
	
	// ft_lstsize
	printf("\n--- ft_lstsize ---\n");
	printf("Taille de la liste: %d\n", ft_lstsize(list));
	
	// ft_lstlast
	printf("\n--- ft_lstlast ---\n");
	t_list *last = ft_lstlast(list);
	printf("Dernier élément: content=%d\n", *(int*)last->content);
	
	// ft_lstadd_back
	printf("\n--- ft_lstadd_back ---\n");
	int *data3 = malloc(sizeof(int));
	*data3 = 84;
	t_list *node3 = ft_lstnew(data3);
	ft_lstadd_back(&list, node3);
	printf("Taille après add_back: %d\n", ft_lstsize(list));
	last = ft_lstlast(list);
	printf("Nouveau dernier élément: content=%d\n", *(int*)last->content);
	
	// Afficher toute la liste
	printf("\n--- Contenu de la liste ---\n");
	t_list *current = list;
	int index = 0;
	while (current)
	{
		printf("Node[%d]: %d\n", index++, *(int*)current->content);
		current = current->next;
	}
	
	// ft_lstiter
	printf("\n--- ft_lstiter ---\n");
	printf("Itération sur la liste:\n");
	ft_lstiter(list, print_content);
	
	// ft_lstmap
	printf("\n--- ft_lstmap ---\n");
	t_list *new_list = ft_lstmap(list, duplicate_int, del_int);
	printf("Nouvelle liste (valeurs x2):\n");
	current = new_list;
	index = 0;
	while (current)
	{
		printf("Node[%d]: %d\n", index++, *(int*)current->content);
		current = current->next;
	}
	
	// ft_lstdelone
	printf("\n--- ft_lstdelone ---\n");
	t_list *to_delete = new_list;
	new_list = new_list->next;
	ft_lstdelone(to_delete, del_int);
	printf("Supprimé premier élément de new_list\n");
	printf("Nouvelle taille: %d\n", ft_lstsize(new_list));
	
	// ft_lstclear
	printf("\n--- ft_lstclear ---\n");
	printf("Taille avant clear: %d\n", ft_lstsize(new_list));
	ft_lstclear(&new_list, del_int);
	printf("Taille après clear: %d\n", ft_lstsize(new_list));
	printf("Liste est NULL? %s\n", new_list == NULL ? "Oui" : "Non");
	
	// Nettoyer la liste originale
	ft_lstclear(&list, del_int);
}

int main(void)
{
	printf("\n");
	printf("╔════════════════════════════════════════╗\n");
	printf("║     TEST COMPLET DE TOUTES LES        ║\n");
	printf("║         FONCTIONS LIBFT                ║\n");
	printf("╚════════════════════════════════════════╝\n");
	
	SEP;
	test_part1_is_functions();
	
	SEP;
	test_part1_str_functions();
	
	SEP;
	test_part1_mem_functions();
	
	SEP;
	test_part1_convert_alloc();
	
	SEP;
	test_part2_functions();
	
	SEP;
	test_part2_fd_functions();
	
	SEP;
	test_bonus_functions();
	
	SEP;
	printf("\n✅ TOUS LES TESTS TERMINÉS !\n\n");
	
	return (0);
}