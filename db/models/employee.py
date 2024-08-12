from db.models.shift import Shift
from typing import Union

class Employee:
    """Employee class define an employee through the ID, Name and Shifts."""
    def __init__(self, id: str, name: str, shifts: list[Shift]=[]) -> None:
        self.id = id
        self.name = name
        self.shifts = shifts
    
    def add_shift(self, shift: Union[Shift, list[Shift]]) -> None:
        if isinstance(shift, list):
            self.shifts.extend(shift)
        elif isinstance(shift, Shift):
            self.shifts.append(shift)
        else:
            raise ValueError("Input 'shift' should be a Shift or a list of Shift instances.")