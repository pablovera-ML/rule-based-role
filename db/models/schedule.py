from db.models.employee import Employee 
from db.models.shift import Shift
from db.models.rule_error import RuleError
from thefuzz import fuzz


class Schedule:
    def __init__(self, employees: dict[str, Employee]={}) -> None:

        self.employees = employees

        self.error_messages = {"multiple_shifts_per_day": RuleError(1, "Employee worked more than 1 shift per day."),
                                "more_than_5_days_worked": RuleError(2, "Employee worked more than 5 days in a week."),
                                "consecutive_night_shifts": RuleError(3, "Employee worked two consecutive night shifts."),
                                "inconsistent_names": RuleError(4, "Inconsistent names for the same Employee ID.")}
        
        # errors_log contains information about all eployees (IDs) violating rules and samples
        self.errors_log = {}

    
    def add_employee(self, new_employee: Employee) -> None:
        employees_id = list(self.employees.keys())

        #
        if new_employee.id not in employees_id:
            self.employees.update({new_employee.id: new_employee})
        else:
            self.validate_employee_name(new_employee)
            
    

    def validate_employee_name(self, new_employee: Employee) -> bool:
        """This rule validates that existing employees names are consistents."""

        existing_employee = self.employees[new_employee.id]
        if fuzz.token_sort_ratio(existing_employee.name, new_employee.name) >= 90:
            self.employees[new_employee.id].add_shift(new_employee.shifts)
            return True
        else:
            error = self.error_messages["inconsistent_names"]
            self.errors_log.update({(existing_employee.id, error.id): {"id": existing_employee.id, 
                                    "error": error, 
                                    "sample": new_employee.name}})
        return False

    
    def validate_multiple_shifts(self, employee_id: Employee, shifts_per_day: dict[str, int]) -> bool:
        """This rule validates if the employee worked more that 1 shift in a day."""
        error = self.error_messages["multiple_shifts_per_day"]
        samples = []
        log_error = False
        for day_of_week, shifts_worked in shifts_per_day.items():
            if shifts_worked>1:
                log_error = True 
                samples.append(day_of_week)
                
        if log_error:
            self.errors_log.update({(employee_id, error.id): {"id": employee_id, 
                                    "error": error, 
                                    "sample": samples}})
            return False
        return True
    
    def validate_days_worked_in_week(self, employee_id: str, shifts_per_day: dict[str, int]) -> bool:
        """This rule validates if the employee worked more that 5 days per week."""
        total = 0
        days_worked = []
        for day, shifts in shifts_per_day.items():
            if shifts>0:
                total+=1
                days_worked.append(day)
        if total>5:
            error = self.error_messages["more_than_5_days_worked"]
            self.errors_log.update({(employee_id, error.id): {"id": employee_id, 
                                    "error": error,
                                    "sample": days_worked}})
            return False
        return True

    def validate_consecutive_night_shifts(self, employee_id, previous_shift: Shift, current_shift: Shift):
        """This rule validates if the employee two consecutive nights in a week."""
        if previous_shift.shift_type=='night' and current_shift.shift_type=='night' and (current_shift.day_number-previous_shift.day_number)==1:
            error = self.error_messages["consecutive_night_shifts"]
            self.errors_log.update({(employee_id, error.id): {"id": employee_id, 
                                    "error": error, 
                                    "sample": [previous_shift.day_of_week, current_shift.day_of_week]}})
            return False
        else:
            return True
    

    def validate_rules(self) -> dict[str, any]:
        """This method validates 3 of the 4 rules."""
        for id, employee in self.employees.items():

            shifts_per_day = {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0}
            previous_shift = None
            for shift in employee.shifts:
                shifts_per_day[shift.day_of_week]+=1
                if previous_shift:
                    self.validate_consecutive_night_shifts(id, previous_shift, shift)
                previous_shift = shift
            
            self.validate_days_worked_in_week(id, shifts_per_day)
            self.validate_multiple_shifts(id, shifts_per_day)
        return self.errors_log

                
                



    
