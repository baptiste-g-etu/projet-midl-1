## Opérateurs

Les opérateurs listés ici ne sont que ceux explicitement définis dans `setup.py`, mais il est possible d’y accéder directement avec le module python `formula`, par exemple : `formula.ArithOpType.SUM`.

### Nullaires (constantes)

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

### Unaires

| Opérateur                   | Raccourci conseillé                                                         |                    Type de l’argument                    |                                           Type de retour |
| --------------------------- | --------------------------------------------------------------------------- | :------------------------------------------------------: | -------------------------------------------------------: |
| `ConstF(b)`, `BoolConst(b)` | `true`, `false`                                                             |                 Booléen Python (`bool`)                  |                        Constante booléenne (`BoolConst`) |
| `NotF(ilf)`, `Not(ilf)`     | `~(ilf)`                                                                    | Type convertible en formule logique (`IntoLogicFormula`) |                      Négation de formule logique (`Not`) |
| `Variable(v)`               | `a`, `b`, `c`, `d`, …                                                       |      Type convertible en variable (`IntoVariable`)       |                                    Variable (`Variable`) |
| `CompBuilder(ct)`           | `eqf`, `ltf`, `==`, `<`                                                     |             Type de comparaison (`CompType`)             |              Constructeur de comparaison (`CompBuilder`) |
| `BoolOpBuilder(bt)`         | `conj`, `disj`, `() & ()`, <code>() &#124 ()</code>, `() >> ()`, `() << ()` |        Type d’opération booléenne (`BoolOpType`)         |     Constructeur d’opération booléenne (`BoolOpBuilder`) |
| `QuantifierBuilder(qt)`     | `forall`, `exists`                                                          |        Type de quantificateur (`QuantifierType`)         |     Constructeur de quantificateur (`QuantifierBuilder`) |
| `ArithOpBuilder(qt)`        | `sum`, `sub`, `prod`, `+`, `-`, `*`                                         |     Type d’opération arithmétique (`QuantifierType`)     | Constructeur d’opération arithmétique (`ArithOpBuilder`) |

### Binaires

| Opérateur                                               | Raccourci                                                           |                                   Type des arguments                                    |                     Type de retour |
| ------------------------------------------------------- | ------------------------------------------------------------------- | :-------------------------------------------------------------------------------------: | ---------------------------------: |
| `eqf(l, r)`, `ltf(l, r)`                                | `l == r`, `l < r`                                                   |           Type convertible en expression arithmétique (`IntoArithExpression`)           |               Comparaison (`Comp`) |
| `conj(l, r)`, `disj(l, r)`, `impl(l, r)`                | `(l) & (r)`, <code>(l) &#124 (r)</code>, `(l) >> (r)`, `(l) << (r)` |                Type convertible en formule logique (`IntoLogicFormula`)                 |     Opération booléenne (`BoolOp`) |
| `allq(v, f)`, `exq(v, f)`, `forall.v(f)`, `exists.v(f)` | Enchaînable : `forall.x.y.z(v)`                                     | `v` : variable (ou nom), `f` : Type convertible en formule logique (`IntoLogicFormula`) |      Quantificateur (`Quantifier`) |
| `sum(l, r)`, `sub(l, r)`, `prod(l, r)`                  | `l + r`, `l - r`, `l * r`                                           |           Type convertible en expression arithmétique (`IntoArithExpression`)           | Opération arithmétique (`ArithOp`) |

### Ternaires

| Opérateur                                  | Raccourci                                                           |                                                            Type des arguments                                                            |                     Type de retour |
| ------------------------------------------ | ------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------: | ---------------------------------: |
| `ArithOp(l, t, r)`, `ArithOpF(l, t, r)`    | `l + r`, `l - r`, `l * r`                                           |   `l`, `r` : Type convertible en expression arithmétique (`IntoArithExpression`), `t` : type d’opération arithmétique (`ArithOpType`)    | Opération arithmétique (`ArithOp`) |
| `BoolOp(l, t, r)`, `BoolOpF(l, t, r)`      | `(l) & (r)`, <code>(l) &#124 (r)</code>, `(l) >> (r)`, `(l) << (r)` |           `l`, `r` : Type convertible en formule logique (`IntoLogicFormula`), `t` : type d’opération booléenne (`BoolOpType`)           |     Opération booléenne (`BoolOp`) |
| `Comp(l, t, r)`, `ComparF(l, t r)`         | `l < r`, `l == r`                                                   |          `l`, `r` : Type convertible en expression arithmétique (`IntoArithExpression`), `t` : type de comparaison (`CompType`)          |               Comparaison (`Comp`) |
| `Quantifier(q, v, f)`, `QuantifF(q, v, f)` | `forall.v(f)`, `exists.v(f)`                                        | `q` : Type de quantificateur (`QuantifierType`), `v` : variable (ou nom), `f` : Type convertible en formule logique (`IntoLogicFormula`) |      Quantificateur (`Quantifier`) |

## Constructeurs

Pour faire des « fonctions » et d’autres syntaxes plus pratiques qui créent des formules ou des expressions, des classes constructeurs (-`Builder`) sont crées.

Elles permettent, notamment dans les cas de `eqf`, `conj`, ou encore `allq` (qui sont donc des instances de constructeurs), de faire une classe appelable, limitant ainsi le nombre de fonctions nécessaires (car la classe contient l’opérateur et non la fonction).

Elles permettent aussi de créer d’autres syntaxes, par exemple `forall.x.y.z(x < y)`, `forall` étant une instance de `QuantifierBuilder` ayant pour quantificateur le quantificateur universel, qui s’enrichit de variables à chaque variable après un point, et qui va finalement quantifier une formule en créant des instances de `Quantifier` autour lorsqu’elle est appelée dessus.
