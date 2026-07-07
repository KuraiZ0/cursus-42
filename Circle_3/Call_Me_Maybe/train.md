# Mini-cours : Constrained Decoding pour Function Calling

## 1. Le problème de base

Un petit LLM (0.6B params) ne produit pas du JSON valide de façon fiable juste en lui demandant gentiment dans le prompt. Il va halluciner des clés, oublier des guillemets, inventer des types.

**Solution : Constrained Decoding.**
Au lieu de laisser le modèle choisir librement le prochain token, on l'**empêche physiquement** de choisir un token qui casserait le JSON ou le schéma.

```
Prompt -> Tokenize -> Input IDs -> LLM -> Logits -> [MASQUE ICI] -> Token choisi -> répéter
```

## 2. Logits et masquage

À chaque étape, le modèle sort un score (logit) par token possible dans le vocabulaire. Plus le score est haut, plus le token est probable.

Pour interdire un token : on met son logit à `-infini`. Après softmax, sa probabilité devient 0. Il ne sera jamais choisi.

```python
masked_logits = np.full(len(logits), float('-inf'))  # tout interdit par défaut
for allowed_id in allowed_ids:
    masked_logits[allowed_id] = logits[allowed_id]    # on réautorise juste ce qu'il faut
```

C'est exactement ce qui se passe dans `generate_json()` de ton `llm_model.py`, et la version vectorisée PyTorch dans `JSONLogitsProcessor.__call__` (`mask[:, allowed_tkn] = scores[:, allowed_tkn]`).

## 3. La machine à états (FSA)

À chaque instant de la génération JSON, il n'y a qu'un **petit nombre de tokens valides**. Exemple :
- Après `{` → seul `"` est valide (début de clé)
- Après `"name"` → seul `: ` est valide
- Dans une valeur `number` → seuls les chiffres sont valides

Donc on modélise le JSON attendu comme une **machine à états finis** :

```
état 0: début          -> attend '{'
état 1: après '{'      -> attend '"'
état 2: après '"'      -> attend 'name'
état 3: après 'name'   -> attend ': '
...
état 7: dans parameters -> attend un nom de paramètre valide pour CETTE fonction
état 9: valeur attendue -> dépend du type (number/string/boolean)
```

Chaque état définit `get_allowed()` (quels tokens sont permis maintenant) et `update()` (comment on change d'état après avoir reçu un token).

## 4. Pourquoi une PILE et pas juste un entier ?

Un simple `self.state = 5` marche pour du JSON plat. Mais le JSON a des structures **imbriquées** :
- Une valeur string peut contenir n'importe quel caractère jusqu'au `"` fermant → c'est un "sous-état" libre, après lequel il faut **revenir** à l'état parent (continuer à lire les autres paramètres).

Une pile permet ça :
```python
self.stack.append(91)   # "j'entre dans un sous-état (texte libre de string)"
...
self.stack.pop()         # "je ressors, je reviens à l'état parent (ex: lire prochain paramètre)"
```

**Règle d'or à respecter dans TON code (et que tu as actuellement cassée) :**
- Pour changer d'état **au même niveau** → `self.stack[-1] = nouvel_état`
- Pour rentrer dans un sous-état → `self.stack.append(nouvel_état)`
- Pour ressortir → `self.stack.pop()`
- **JAMAIS** `self.stack = 5` → ça remplace toute la pile par un entier, et `self.stack.pop()` plus tard va crasher.

## 5. Le vocabulaire (voc)

`voc` = dictionnaire `{token_string: token_id}`. Le module charge ça via `llm_model.get_path_to_vocabulary_json()`.

Astuce du projet : au lieu de chercher token par token "est-ce que ça correspond", on précalcule directement les IDs autorisés via `voc[mot_attendu]`, ce qui est rapide.

Pour `id_to_txt` (l'inverse : id → texte), il faut le construire toi-même quelque part :
```python
id_to_txt = {token_id: token for token, token_id in voc.items()}
```
Ce dict n'existe pas encore dans ton code — il faut l'ajouter avant de pouvoir lancer `JSONLogitsProcessor`.

## 6. Le cycle complet à l'inférence

1. `is_first_call` → pas encore de token généré, on calcule juste les tokens permis à l'état initial.
2. Pour chaque appel suivant : on regarde le dernier token généré (`input_ids[0][-1]`), on le traduit en texte via `id_to_txt`, on appelle `state_machine.update(texte)` pour avancer la machine à états.
3. On recalcule `get_allowed()` pour le nouvel état.
4. On masque les logits, on laisse le modèle (ou un sampling) choisir parmi les survivants.

## 7. Pourquoi pas juste valider après coup (retry si invalide) ?

Le sujet l'interdit explicitement : il faut **garantir 100%** de JSON valide, pas espérer puis réessayer. Le retry est probabiliste, le constrained decoding est déterministe au niveau structure.

---

# Ce qu'il te reste à faire (priorités)

1. **Corriger le bug de pile** (`self.stack = X` → `self.stack[-1] = X` ou `.append`/`.pop`) partout dans `JSONStateMachine`.
2. **Unifier les imports** : choisir `src.model.schemas` OU `src.models.schemas`, pas les deux.
3. **Construire `id_to_txt`** et le passer à `JSONLogitsProcessor`.
4. **Câbler `JSONStateMachine` avec `fn_dict`**, pas `voc`, dans le `__main__`.
5. **Brancher tout dans le vrai pipeline `model.generate()`** avec `LogitsProcessorList` (actuellement c'est un faux generate, juste un draft).
6. **Gérer les types `number` correctement** : ton FSA actuel n'autorise que le chiffre `"0"` littéral pour `number` — il faut autoriser tous les chiffres, le point décimal, et un état libre similaire au `91` des strings, avec une condition d'arrêt sur un caractère non-numérique (genre `,` ou `}`).
7. **Construire la pipeline `main`** (cli_parser → charge functions + prompts → pour chaque prompt, generate_json contraint → écrit `function_calling_results.json`).
8. **Tests unitaires** sur des cas simples (number, string, boolean, plusieurs paramètres).

Conseil : fixe d'abord le bug de pile et teste la state machine **seule**, sans LLM (juste en appelant `.update()` à la main avec une séquence de textes), avant de la brancher sur le vrai modèle. Plus facile à débugger.