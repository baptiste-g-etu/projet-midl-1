from formula.types import IntoLogicFormula
from functions import close


def decide(f: IntoLogicFormula) -> bool:
    _closed = close(f)
    return True
