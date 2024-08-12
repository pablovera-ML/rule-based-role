from db.models.schedule import Schedule 
from collections import defaultdict
from datetime import datetime

class Report:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def _group_employees(self):
        grouped_employees = defaultdict(list)
        for id, error in self.schedule.errors_log.items():
            employee_id = id[0]
            grouped_employees[employee_id].append((error["error"].message, error["sample"]))
        return grouped_employees
    
    def _capitalize_elements(self, samples):
        if isinstance(samples, list):
            return ', '.join([e.title() for e in samples])
        else:
            return samples.title()
    
    def write_report(self, destination: str="./") -> str:
        now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = f"report_{now_date}.txt"  

        with open(destination+file_name, 'w') as file:
            grouped_employees = self._group_employees()
            for employee_id, errors in grouped_employees.items():
                employee = self.schedule.employees[employee_id]
                header = f"* Employee ID {employee_id}. Name {employee.name.title()}"
                errors_detail = f"""{header}. \n Violated rules: \n"""
                for error in errors:
                    samples = self._capitalize_elements(error[1])
                    message = error[0]
                    errors_detail += f"""   - {message}\n"""
                    errors_detail += f"     - Examples: {samples}. \n"
                
                file.write(errors_detail)
        return destination+file_name