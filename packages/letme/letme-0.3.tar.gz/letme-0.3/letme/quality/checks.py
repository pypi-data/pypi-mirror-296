from .basics import *
from ..helpers import save_checks


class check:
    def __init__(self, source ,auto_save: bool = False):
        self.auto_save = auto_save
        self.source = source

    def check_condition(self, condition: str):
        output = check_condition(source = self.source, condition = condition)
        if self.auto_save:
            save_checks(output[0])
        return output






