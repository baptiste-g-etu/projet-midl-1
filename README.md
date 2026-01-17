# Projet MIDL 1 - Procédure d'élimlination des quantificateurs de la théorie DO

## Table des matières
0. [Généralités](#généralités)
1. [Tâche 1](#tâche-1)
2. [Tâche 2](#tâche-2)
3. [Tâche 3](#tâche-3)

## Généralités

Dans ce projet, nous avons ajouté quelques fonctionnalités pour faciliter l'expérience utilisateur, notamment avec : 
- Un parenthésage intelligent des formules
- L'utilisation de couleurs pour faciliter la lecture des formules (en se basant sur le terminal utilisateur)
- Déclaration de variables logiques sans utiliser des guillemets, pour les lettres classiques (`"x"` = `x`), nous y reviendrons avec des exemples.
- Ajout d'une syntaxe supplémentaire plus proche du $\LaTeX$

## Tâche 1
`prelude.py` contient les synonymes et les opérateurs de base (c’est le remplacement du fichier initial `syntax.py`).
`formula.py` contient les classes utiles pour tout le projet, et de leurs méthodes.  
Pour l'implémentation de Dual(), nous avons choisi de créer une fonction récursive ```map_formula(formule, fonction)``` qui va parcourir l'arbre de la formule en entrée, et y appliquer une fonction sur chaque nœud (parcours en profondeur). Cela sera plus simple pour les futures tâches. Ces fonctions se retrouvent pour l'instant dans le fichier ```formules.py```.

### Opérateurs
L’entièreté des opérateurs est définie dans la référence.

Liste simplifiée des principaux opérateurs :

| Syntaxe                                                                                                                            | Résultat                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `a + b`, `a - b`, `a * b`                                                                                                          | Opération arithmétique entre deux expressions arithmétiques |
| `a < b`, `a == b`, (éventuellement `a <= b`, `a > b`, `a >= b`, `a != b`)                                                          | Comparaison entre deux expressions arithmétiques            |
| <code>(a) &#124 (b)</code>, `(a) & (b)`, `(a) >> (b)`, `(a) << (b)`, `~(a)`, `disj(a, b)`, `conj(a, b)`, `impl(a, b)`, `Not(a)`, … | Opération logique sur formule(s) logique(s)                 |
| `forall.a(form)`, `exists.a.b.c.d.e.f(form)`                                                                                       | Quantificateur de variable(s) appliqué à une formule        |
| `a`, `b`, `c`, `d`, … (les lettres de l’alphabet sont définies comme variables)                                                    | Variable arithmétique                                       |
| `true`, `false`, `top`, `bot`                                                                                                      | Constante booléenne                                         |
Attention aux parenthèses pour les opérations logiques entre formules arithmétiques, les opérateurs logiques sous la forme de symboles (`|`, `&`, `~`, `>>` et `<<`) ont plus de priorité que les opérateurs arithmétiques et les comparaisons.  
Par exemple, `a < b | c < d` n’est pas valide (`b | c` ne pouvant pas s’évaluer).

## Tâche 2

### Nouvelles fonctionnalités
1. Ajout du module `decision` et de `decision.elim` contenant la fonction `decide` (importée dans le prélude).
2. Ajout de fonctions utilitaires dans `functions` (importées dans le prélude) :
	- `close` pour clore une formule.
	- `free_variables` (ou `fv`) pour lister l’ensemble des variables libres d’une formule.
3. Ajout de la syntaxe `f[v]` pour obtenir les informations additionnelles qu’on peut connaître sur une `Variable` quand celle-ci est reliée à une formule (par exemple si elle est libre ou non).
	- Cette syntaxe construit une classe `VariableInfo`, et quelques méthodes sont définies dessus, par exemple `forall.a(a < b)[a].is_free()`.
	- Les informations ne sont calculées qu’au moment où on les demande, la construction de la classe `VariableInfo` ne fait rien.
4. Ajout de la syntaxe `f[v:expr]` qui remplace la variable `v` par l’expression arithmétique `expr` donnée.
	- On peut effectuer plusieurs remplacements **en même temps** (pas à la suite) : `f[v:expr1, x:expr2, y:expr3, ...]` ou `f[x:y, y:x]`.
	- Renommer une variable par une autre variable renomme également la variable dans les quantificateurs.
	- Remplacer une variable par une expression ne supprime pas les quantificateurs associés.
	- Pour faire plusieurs remplacements à la suite, on peut se servir du fait que la valeur renvoyée soit elle-même une formule : `f[v:w][w:expr1]` est donc le remplacement de `v` par `w` puis de `w` par `expr1`.
5. Remplacement de la fonction `__contains__` sur les formules par `__iter__` qui liste (dans l’ordre alphabétique) les variables d’une formule.
	- `v in f` fonctionne toujours grâce à l’implémentation par défaut de `__contains__` sur les itérateurs.
	- Pour obtenir la liste des variables d’une formule, on peut désormais faire `list(f)` (par exemple `list(forall.a(a < b))`).
	- Les variables inutilisées présentes dans les quantificateurs ne sont pas comptées (`list(forall.a(b < c))` renvoie `[b, c]`).
6. Ajout de la forme prénexe `PNF` pour représenter une formule sous forme prénexe.
	- Le constructeur vérifie seulement que la formule est en forme prénexe, sinon il lève une `AssertionError`.
