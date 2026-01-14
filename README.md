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

```setup.py``` contient les synonymes et les opérateurs de base. Il est le remplacement du fichier initial ```syntax.py```

```formula.py``` contient les classes utiles pour tout le projet, et de leurs méthodes.

Pour l'implémentation de Dual(), nous avons choisi de créer une fonction récursive ```map_formula(formule, fonction)``` qui va parcourir l'arbre de la formule en entrée, et y appliquer une fonction. Cela sera plus simple pour les futures tâches. Ces fonctions se retrouvent pour l'instant dans le fichier ```formules.py```.
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
## Tâche 2
Ajout du module `decision` et de `decision.elim` contenant la fonction `decide` (importée dans le prélude).

Ajout de fonctions utilitaires dans `functions` (importées dans le prélude) :
- `close` pour clore une formule.
- `free_variables` pour lister l’ensemble des variables libres d’une formule.

Ajout de la classe `VariableInfo`, qui représente les informations additionnelles qu’on peut obtenir sur une `Variable` quand celle-ci est reliée à une formule (par exemple si elle est libre ou non).
- Cette classe se construit à partir d’une formule `f` et d’une variable `v` de cette manière : `f[v]` (par exemple `forall.a(a < b)[a].is_free()`).
- Les informations ne sont calculées qu’au moment où on les demande, la construction de la classe ne fait rien.

Remplacement de la fonction `__contains__` sur les formules par `__iter__` qui liste (dans l’ordre alphabétique) les variables d’une formule.
- `v in f` fonctionne toujours grâce à l’implémentation par défaut de `__contains__` sur les itérateurs.
- Pour obtenir la liste des variables d’une formule, on peut désormais faire `list(f)` (par exemple `list(forall.a(a < b))`).
- Les variables inutilisées présentes dans les quantificateurs ne sont pas comptées (`list(forall.a(b < c))` renvoie `[b, c]`).

