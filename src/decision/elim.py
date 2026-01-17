from formula.forms import PNF
from formula.types import IntoLogicFormula
from functions import close


def decide(f: IntoLogicFormula) -> bool:
    closed = close(f)
    prenex = PNF(closed)
    print(prenex)
    return True
