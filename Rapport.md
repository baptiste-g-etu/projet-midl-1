<p style="text-align: center">Étudiants : Nyl Vitry, Baptiste Goudet, Matthieu Staub</p>
## Introduction

Le but de projet est de transcrire l’algorithme d’élimination des quantificateurs de la théorie des ordres denses en python, tout en conservant une syntaxe naturelle.

Problèmes rencontrés : 
- Circular imports : plus de temps à régler ces problèmes Python que de coder (plus un rallongement inutiles des fichiers)
- Le typage de certaines classes (choisir entre le statique et le dynamique)
- Conflits avec Python vis à vis de certains opérateurs

## Manuel Utilisateur
Pour cette partie, nous avions déjà ajouté un fichier readme, contenant des indications pour utiliser le programme. Nous mettrons ici un tableau contenant les informations essentielles, mais vous pourrez retrouver le [manuel plus complet ici](https://github.com/baptiste-g-etu/projet-midl-1/tree/T2?tab=readme-ov-file#g%C3%A9n%C3%A9ralit%C3%A9s)

| Syntaxe                                                                                                                                          | Résultat                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| `x < y`, `x == y`, (éventuellement `x <= y`, `x > y`, `x >= y`, `x != y`)                                                                        | Comparaison entre deux expressions arithmétiques     |
| <code>(f1) &#124 (f2)</code>, `(f1) & (f2)`, `(f1) >> (f2)`, `(f1) << (f2)`, `~(f)`, `disj(f1, f2)`, `conj(f1, f2)`, `impl(f1, f2)`, `Not(f)`, … | Opération logique sur formule(s) logique(s)          |
| `forall.x(f)`, `exists.x.y.z.a.b.c(f)`                                                                                                           | Quantificateur de variable(s) appliqué à une formule |
| `x`, `y`, `z`, `a`, … (les lettres de l’alphabet sont définies comme variables)                                                                  | Variable arithmétique                                |
| `true`, `false`, `top`, `bot`                                                                                                                    | Constante booléenne                                  |
| `decide(f)`                                                                                                                                      | Fonction de décision (renvoie un booléen)            |

Il est possible de changer certains paramètres d'affichage, notamment la coloration. Pour se faire, il suffit de modifier les variables globales du module `display`.

## Implantation

On a fait deux classes principales :
1. `LogicFormula` (qui représente toutes les formules logiques) :
	- Sert à garantir que les opérations sur par exemple les quantificateurs et opérateurs logiques restent valides, de ne pas faire une procédure sur une formule invalide.
2.  `ArithExpression` (principalement en prévision du lot 2) :
	- Sert uniquement pour les variables seules pour le moment.

## Lots 2 et 3

