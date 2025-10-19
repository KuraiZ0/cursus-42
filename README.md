# 🧩 Libft

Libft est une librairie en C développée dans le cadre du cursus de l’école 42.
Son but est de recréer les fonctions essentielles de la libc et d’y ajouter des **outils personnels réutilisables** pour les futurs projets.

---

## ⚙️ Compilation

make        # Compile la libft
make clean  # Supprime les fichiers objets (.o)
make fclean # Supprime les fichiers objets et la lib (.a)
make re     # Recompile entièrement la lib
make bonus  # Compile avec les bonus

La compilation crée le fichier "libft.a" que vous pourrez lier à vos futurs projets.

---

## 📚 Utilisation

Inclure le header dans vos fichiers :
```
#include "libft.h"
```

Compiler votre programme avec la librairie :

gcc -Wall -Wextra -Werror main.c -L. -lft -o prog


---

## 🧠 Contenu de la librairie

### 🔹 Fonctions de la libc recréées :
`ft_strlen`, `ft_strchr`, `ft_strncmp`, `ft_memcpy`, `ft_memset`, `ft_calloc`, `ft_strdup`, etc.

### 🔹 Fonctions supplémentaires :
`ft_substr`, `ft_strjoin`, `ft_strtrim`, `ft_split`, `ft_itoa`, `ft_strmapi`, etc.

### 🔹 Bonus (listes chaînées) :
`ft_lstnew`, `ft_lstadd_front`, `ft_lstadd_back`, `ft_lstclear`, `ft_lstdelone`, `ft_lstiter`, `ft_lstmap`, etc.

---

## 💡 Exemple d’utilisation

#include "libft.h"
#include <stdio.h>

int main(void)
{
    char *str = "Hello World";
    printf("Length: %zu\n", ft_strlen(str));
    return (0);
}
```

Compilation :
```
gcc -Wall -Wextra -Werror main.c -L. -lft -o test && ./test
```

---

## 🧰 Objectifs pédagogiques

- Comprendre le fonctionnement interne des fonctions de la **libc**.  
- Travailler la **gestion de la mémoire** et les **pointeurs**.  
- Créer une base de code solide pour les projets suivants :  
  `get_next_line`, `ft_printf`, `so_long`, `push_swap`, etc.

---

## 👨‍💻 Auteur

**Nom :** Yusuke
**École :** 42  
**Projet :** Libft  
**Langage :** C  
**OS testé :** macOS / Linux  

---

## 🏁 Statut du projet

✅ Terminé — prêt à être utilisé dans vos futurs projets 42.  
🧠 En constante amélioration (optimisations et corrections possibles).

---

## 🧷 Licence

Projet développé dans le cadre du cursus **42**.  
Libre d’utilisation à des fins pédagogiques.

---

⭐ *Si ce projet t’a aidé, n’hésite pas à lui mettre une étoile sur GitHub !*

