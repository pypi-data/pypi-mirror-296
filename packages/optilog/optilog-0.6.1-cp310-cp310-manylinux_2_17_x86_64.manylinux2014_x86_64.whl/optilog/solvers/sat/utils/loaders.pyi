from optilog.formulas import WCNF as WCNF
from optilog.internalutils import general_parser as general_parser
from typing import NamedTuple

class SatSolverOutput(NamedTuple):
    model: list[int] | None
    sat: str | None
    def verify_on(self, formula): ...

class MaxSatSolverOutput(NamedTuple):
    model: list[int] | None
    sat: str | None
    cost: int | None
    def verify_on(self, formula): ...

def load_sat_output(path, model_format): ...
def load_maxsat_output(path, model_format): ...
