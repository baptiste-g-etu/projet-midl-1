# Projet MIDL 1 - Procédure d'élimlination des quantificateurs de la théorie DO

## Table des matières
0. [Généralités](#T0)
1.1. [Tâche 1](#Tache-1)
1.2. [Tâche 2](#Tache-2)
1.3. [Tâche 3](#Tache-3)

## Généralités

Dans ce projet, nous avons ajouté quelques fonctionnalités pour faciliter l'expérience utilisateur, notamment avec : 
- Un parenthésage intelligent des formules
- L'utilisation de couleurs pour faciliter la lecture des formules (en se basant sur le terminal utilisateur)
- Déclaration de variables logiques sans utiliser des guillemets, pour les lettres classiques ("x" = x), nous y reviendrons avec des exemples.
- Ajout d'une syntaxe supplémentaire plus proche du LATEX

| Syntaxe d'origine                                                   |  Syntaxe d'origine simplifiée   |                                                       Notre syntaxe |
| ------------------------------------------------------------------- | :-----------------------------: | ------------------------------------------------------------------: |
| QuantifF (All(), "x",QuantifF (Ex(), "y", ComparF("x", Lt(), "y"))) | allq("x",exq("y",ltf("x","y"))) | TO ADD (il est 0h45 je suis trop fatigué pour retrouver la syntaxe) |
| Lorem                                                               |              ipsum              |                                                               dolor |


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
| `a < b`, `a == b`, (éventuellement `a <= b`, `a > b`, `a >= b`)                                                                    | Comparaison entre deux expressions arithmétiques            |
| <code>(a) &#124 (b)</code>, `(a) & (b)`, `(a) >> (b)`, `(a) << (b)`, `~(a)`, `disj(a, b)`, `conj(a, b)`, `impl(a, b)`, `Not(a)`, … | Opération logique sur formule(s) logique(s)                 |
| `forall.a(form)`, `exists.a.b.c.d.e.f(form)`                                                                                       | Quantificateur de variable(s) appliqué à une formule        |
| `a`, `b`, `c`, `d`, … (les lettres de l’alphabet sont définies comme variables)                                                    | Variable arithmétique                                       |
| `true`, `false`, `top`, `bot`                                                                                                      | Constante booléenne                                         |
Attention aux parenthèses pour les opérations logiques entre formules arithmétiques, les opérateurs logiques sous la forme de symboles (`|`, `&`, `~`, `>>` et `<<`) ont plus de priorité que les opérateurs arithmétiques et les comparaisons.
