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

La version minimale de Python pour pouvoir exécuter ce programme est la version 3.12 (cependant, il a été élaboré avec la version 3.14).

## Tâche 1

`prelude.py` contient les synonymes et les opérateurs de base (c’est le remplacement du fichier initial `syntax.py`).
`formula.py` contient les classes utiles pour tout le projet, et de leurs méthodes.  
Pour l'implémentation de Dual(), nous avons choisi de créer une fonction récursive `map_formula(formule, fonction)` qui va parcourir l'arbre de la formule en entrée, et y appliquer une fonction sur chaque nœud (parcours en profondeur). Cela sera plus simple pour les futures tâches. Ces fonctions se retrouvent pour l'instant dans le fichier `formules.py`.

### Opérateurs

L’entièreté des opérateurs est définie dans la référence.

Liste simplifiée des principaux opérateurs :

| Syntaxe                                                                                                                                          | Résultat                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `x + y`, `x - y`, `x * y`                                                                                                                        | Opération arithmétique entre deux expressions arithmétiques |
| `x < y`, `x == y`, (éventuellement `x <= y`, `x > y`, `x >= y`, `x != y`)                                                                        | Comparaison entre deux expressions arithmétiques            |
| <code>(f1) &#124 (f2)</code>, `(f1) & (f2)`, `(f1) >> (f2)`, `(f1) << (f2)`, `~(f)`, `disj(f1, f2)`, `conj(f1, f2)`, `impl(f1, f2)`, `Not(f)`, … | Opération logique sur formule(s) logique(s)                 |
| `forall.x(f)`, `exists.x.y.z.a.b.c(f)`                                                                                                           | Quantificateur de variable(s) appliqué à une formule        |
| `x`, `y`, `z`, `a`, … (les lettres de l’alphabet sont définies comme variables)                                                                  | Variable arithmétique                                       |
| `true`, `false`, `top`, `bot`                                                                                                                    | Constante booléenne                                         |

Attention aux parenthèses pour les opérations logiques entre formules arithmétiques, les opérateurs logiques sous la forme de symboles (`|`, `&`, `~`, `>>` et `<<`) ont plus de priorité que les opérateurs arithmétiques et les comparaisons.  
Par exemple, `x < y | z < a` n’est pas valide (`y | z` ne pouvant pas s’évaluer).

## Tâche 2

### Nouvelles fonctionnalités

1. Ajout du module `decision` et de `decision.elim` contenant la fonction `decide` (importée dans le prélude).
2. Ajout de fonctions utilitaires dans `functions` (importées dans le prélude) :
    - `close` pour clore une formule.
    - `free_variables` (ou `fv`) pour lister l’ensemble des variables libres d’une formule.
3. Ajout de la syntaxe `f[x]` pour obtenir les informations additionnelles qu’on peut connaître sur une `Variable` quand celle-ci est reliée à une formule (par exemple si elle est libre ou non).
    - Cette syntaxe construit une classe `VariableInfo`, et quelques méthodes sont définies dessus, par exemple `forall.x(x < y)[x].is_free()`.
    - Les informations ne sont calculées qu’au moment où on les demande, la construction de la classe `VariableInfo` ne fait rien.
4. Ajout de la syntaxe `f[x:expr]` qui remplace la variable `x` par l’expression arithmétique `expr` donnée.
    - On peut effectuer plusieurs remplacements **en même temps** (pas à la suite) : `f[x:expr1, y:expr2, z:expr3, ...]` ou `f[x:y, y:x]`.
    - Renommer une variable par une autre variable renomme également la variable dans les quantificateurs.
    - Remplacer une variable par une expression ne supprime pas les quantificateurs associés.
    - Pour faire plusieurs remplacements à la suite, on peut se servir du fait que la valeur renvoyée soit elle-même une formule : `f[x:y][y:expr1]` est donc le remplacement de `x` par `y` puis de `y` par `expr1`.
5. Remplacement de la fonction `__contains__` sur les formules par `__iter__` qui liste (dans l’ordre alphabétique) les variables d’une formule.
    - `x in f` fonctionne toujours grâce à l’implémentation par défaut de `__contains__` sur les itérateurs.
    - Pour obtenir la liste des variables d’une formule, on peut désormais faire `list(f)` (par exemple `list(forall.x(x < y))`).
    - Les variables inutilisées présentes dans les quantificateurs ne sont pas comptées (`list(forall.x(y < z))` renvoie `[y, z]`).
6. Ajout de la forme prénexe `PNF` pour représenter une formule sous forme prénexe.
    - Le constructeur vérifie seulement que la formule est en forme prénexe, sinon il lève une `AssertionError`.
