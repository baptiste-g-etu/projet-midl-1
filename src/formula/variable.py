from typing import Any, Iterator

from .coloring import COLORING, color_level
from .types import ArithExpression, IntoArithExpression, into_arith_expr

# Types that can be converted into a Variable
type IntoVariable = Variable | str


class Variable(ArithExpression):
    """
    Arithmetic variable.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def is_syntaxically_eq(self, rhs: "Variable") -> bool:
        return self.name == rhs.name

    def __repr_colored__(self, level: int):
        return color_level(level, self.name)

    def __iter__(self) -> Iterator["Variable"]:
        return iter([self])

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return self.name

    def replace(
        self, variable: IntoVariable, expr: IntoArithExpression
    ) -> ArithExpression:
        if self.is_syntaxically_eq(into_variable(variable)):
            return into_arith_expr(expr)
        else:
            return self


def into_variable(var: Any) -> Variable:
    """
    Converts a str into a Variable if needed. Also reject to cast a number as a variable
    """
    if isinstance(var, Variable):
        return var
    elif isinstance(var, str):
        if var.isdigit():
            # Should we keep that ?
            raise TypeError(f"You should not use the number : {var} as a variable name")
        return Variable(var)
    else:
        raise TypeError(f"Cannot convert value of type {type(var)} into Variable")
