# 🔄 Push_swap

![Status](https://img.shields.io/badge/Status-Completed-success) ![Language](https://img.shields.io/badge/Language-C-blue) ![School](https://img.shields.io/badge/42-Project-black)

## 📝 Description

**Push_swap** est un projet d'algorithmique très complet de l'école 42. L'objectif est de trier une pile d'entiers (Stack A) en utilisant une pile auxiliaire (Stack B) et un ensemble d'instructions limité, le tout avec le **moins de coups possible**.

Ce projet m'a permis d'approfondir la complexité algorithmique, la manipulation de piles (Stacks) et les opérations bitwise.

## 🧠 Algorithme Utilisé : Radix Sort (Base Binaire)

Pour optimiser le tri des grandes listes, j'ai implémenté un **Radix Sort** (LSD - Least Significant Digit) adapté aux contraintes du projet.

### Fonctionnement technique :
1.  **Parsing & Validation :** Vérification stricte des arguments (entiers uniquement, pas de doublons, gestion des limites `INT_MAX`/`INT_MIN`).
2.  **Indexation (Simplification) :** Avant le tri, les valeurs réelles sont remplacées par leur **rang** (index de 0 à N-1). Cela permet de gérer facilement les nombres négatifs et de grands écarts.
3.  **Tri Bit-à-Bit :**
    * L'algorithme parcourt les nombres en base binaire.
    * À chaque itération (pour chaque bit), les nombres ayant un `0` à la position binaire actuelle sont poussés vers la pile B (`pb`).
    * Les nombres ayant un `1` restent dans la pile A et subissent une rotation (`ra`).
    * La pile B est ensuite reversée dans A (`pa`).

### Stratégies pour petites listes :
* **3 nombres :** Algorithme dédié ultra-rapide (< 3 coups).
* **5 nombres :** Algorithme hybride (push des 2 plus petits + tri de 3).

## 🛠️ Instructions

Les opérations autorisées pour manipuler les piles sont :

| Commande | Action |
| :--- | :--- |
| `sa`, `sb`, `ss` | **Swap** : Échange les deux premiers éléments d'une pile. |
| `pa`, `pb` | **Push** : Prend le premier élément d'une pile et le met sur l'autre. |
| `ra`, `rb`, `rr` | **Rotate** : Décale tous les éléments vers le haut (le premier devient dernier). |
| `rra`, `rrb`, `rrr` | **Reverse Rotate** : Décale tous les éléments vers le bas (le dernier devient premier). |

## 🚀 Installation et Utilisation

### Compilation
Utilisez le `Makefile` pour compiler le projet.
```bash
make
Exécution
Lancer le programme avec une liste d'entiers en arguments :

Bash

./push_swap 2 1 3 6 5 8
Vérification
Pour vérifier si le tri est correct et compter le nombre de coups :

Bash

ARG="4 67 3 80 12"; ./push_swap $ARG | wc -l
📊 Performance (Moyenne)
3 nombres : ~2 coups

5 nombres : ~10 coups

100 nombres : < 700 coups (Objectif 5 étoiles)

500 nombres : < 5500 coups (Objectif 5 étoiles)
