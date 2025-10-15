# Projet MIDL 1 - Procédure d'élimlination des quantificateurs de la théorie DO

## Table des matières
0. [Généralités](#T0)
1.1. [Tâche 1](#Tache-1)
1.2. [Tâche 2](#Tache-2)
1.3. [Tâche 3](#Tache-3)

## Généralités

Dans ce projet, nous avons ajouté quelques fonctionnalités pour faciliter l'expérience utilisateur, notamment avec : 
- Un parenthésage intelligent des formules
- L'utilisation de couleurs pour faciliter la lecture des formules (en se basant surle terminal utilisateur)
- Déclaration de variables logiques sans utiliser des guillemets, pour les lettres classiques ("x" = x), nous y reviendrons avec des exemples.
- Ajout d'une syntaxe supplémentaire plus proche du LATEX

| Syntaxe d'origine  | Syntaxe d'origine simplifiée | Notre syntaxe |
| ------------------ |:----------------------------:| -------------:|
|QuantifF (All(), "x",QuantifF (Ex(), "y", ComparF("x", Lt(), "y")))| allq("x",exq("y",ltf("x","y"))) | TO ADD (il est 0h45 je suis trop fatigué pour retrouver la syntaxe) |
| Lorem | ipsum | dolor |


## Tâche 1

```setup.py``` contient les synonymes et les opérateurs de base. Il est le remplacement du fuchier initial ```syntax.py```

```formula.py``` contient les classes utiles pour tout le projet, et de leurs méthodes.

Pour l'implémentation de Dual(), nous avons choisi de créer une fonction récursive ```map_formula(formule, fonction)``` qui va parcourir l'arbre de la formule en entrée, et y appliquer une fonction. Cela sera plus simple pour les futures tâches. Ces fonctions se retouvent pour l'instant dans le fichier ```formules.py```.
### Opérateurs
Les opérateurs listés ici ne sont que ceux explicitement définis dans `setup.py`, mais il est possible d’y accéder directement avec le module python `formula`, par exemple : `formula.ArithOpType.SUM`.
#### Nullaires (constantes)

| Opérateur                                  |                Type de retour                 |                                       Retour |
| ------------------------------------------ | :-------------------------------------------: | -------------------------------------------: |
| `true`, `top`                              |       Constante booléenne (`BoolConst`)       |                                         Vrai |
| `false`, `bot`                             |       Constante booléenne (`BoolConst`)       |                                         Faux |
| `Eq`, `Eq()`, `EQUAL`, `EQUAL()`           |       Type de comparaison (`CompType`)        |                                      Égalité |
| `Lt`, `Lt()`, `LOWER_THAN`, `LOWER_THAN()` |       Type de comparaison (`CompType`)        | Inférieur <!-- « infériorité stricte » ? --> |
| `All`, `All()`, `FORALL`, `FORALL()`       |   Type de quantificateur (`QuantifierType`)   |                                    Universel |
| `Ex`, `Ex()`, `EXISTS`, `EXISTS()`         |   Type de quantificateur (`QuantifierType`)   |                                  Existentiel |
| `Conj`, `Conj()`, `CONJ`, `CONJ()`         |   Type d’opération booléenne (`BoolOpType`)   |                                  Conjonction |
| `Disj`, `Disj()`, `DISJ`, `DISJ()`         |   Type d’opération booléenne (`BoolOpType`)   |                                  Disjonction |
| `Sum`, `Sum()`                             | Type d’opération arithmétique (`ArithOpType`) |                                        Somme |
| `Sub`, `Sub()`                             | Type d’opération arithmétique (`ArithOpType`) |                                 Soustraction |
| `Prod`, `Prod()`                           | Type d’opération arithmétique (`ArithOpType`) |                                      Produit |
| `a`, `b`, `c`, `d`, …                      |             Variable (`Variable`)             |                                     Variable |
#### Unaires
| Opérateur                   | Raccourci conseillé                   |                    Type de l’argument                    |                                           Type de retour |
| --------------------------- | ------------------------------------- | :------------------------------------------------------: | -------------------------------------------------------: |
| `ConstF(b)`, `BoolConst(b)` | `true`, `false`                       |                 Booléen Python (`bool`)                  |                        Constante booléenne (`BoolConst`) |
| `NotF(ilf)`, `Not(ilf)`     | `~ilf`                                | Type convertible en formule logique (`IntoLogicFormula`) |                      Négation de formule logique (`Not`) |
| `Variable(v)`               | `a`, `b`, `c`, `d`, …                 |      Type convertible en variable (`IntoVariable`)       |                                    Variable (`Variable`) |
| `CompBuilder(ct)`           | `eqf`, `ltf`, `==`, `<`               |             Type de comparaison (`CompType`)             |              Constructeur de comparaison (`CompBuilder`) |
| `BoolOpBuilder(bt)`         | `conj`, `disj`, `&`, `\|`, `>>`, `<<` |        Type d’opération booléenne (`BoolOpType`)         |     Constructeur d’opération booléenne (`BoolOpBuilder`) |
| `QuantifierBuilder(qt)`     | `forall`, `exists`                    |        Type de quantificateur (`QuantifierType`)         |     Constructeur de quantificateur (`QuantifierBuilder`) |
| `ArithOpBuilder(qt)`        | `sum`, `sub`, `prod`, `+`, `-`, `*`   |     Type d’opération arithmétique (`QuantifierType`)     | Constructeur d’opération arithmétique (`ArithOpBuilder`) |
#### Binaires
| Opérateur                                               | Raccourci                             |                                   Type des arguments                                    |                     Type de retour |
| ------------------------------------------------------- | ------------------------------------- | :-------------------------------------------------------------------------------------: | ---------------------------------: |
| `eqf(l, r)`, `ltf(l, r)`                                | `l == r`, `l < r`                     |           Type convertible en expression arithmétique (`IntoArithExpression`)           |               Comparaison (`Comp`) |
| `conj(l, r)`, `disj(l, r)`, `impl(l, r)`                | `l & r`, `l \| r`, `l >> r`, `l << r` |                Type convertible en formule logique (`IntoLogicFormula`)                 |     Opération booléenne (`BoolOp`) |
| `allq(v, f)`, `exq(v, f)`, `forall.v(f)`, `exists.v(f)` | Enchaînable : `forall.x.y.z(v)`       | `v` : variable (ou nom), `f` : Type convertible en formule logique (`IntoLogicFormula`) |      Quantificateur (`Quantifier`) |
| `sum(l, r)`, `sub(l, r)`, `prod(l, r)`                  | `l + r`, `l - r`, `l * r`             |           Type convertible en expression arithmétique (`IntoArithExpression`)           | Opération arithmétique (`ArithOp`) |
#### Ternaires
| Opérateur                             | Raccourci                 |                                                 Type des arguments                                                  |                     Type de retour |
| ------------------------------------- | ------------------------- | :-----------------------------------------------------------------------------------------------------------------: | ---------------------------------: |
| `ArithOp(l, t, r), ArithOpF(l, t, r)` | `l + r`, `l - r`, `l * r` | `l`, `r` : Type convertible en expression arithmétique (`IntoArithExpression`), `t` : type d’opération arithmétique | Opération arithmétique (`ArithOp`) |
