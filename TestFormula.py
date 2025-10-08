from main import *

# Formula from the subjet pdf
allq(
    "x",
    allq(
        "y",
        allq(
            "z",
            exq(
                "u",
                impl(
                    conj(ltf("x", "y"), ltf("x", "z")),
                    conj(ltf("y", "u"), ltf("z", "u")),
                ),
            ),
        ),
    ),
)
