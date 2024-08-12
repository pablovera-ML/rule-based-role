from preprocess import load_schedules, lowercase, remove_accents
from db.models.employee import Employee
from db.models.shift import Shift
from db.models.schedule import Schedule
from report import Report


if __name__=="__main__":
    """ The input data is preprocessed in order to remove accents from names and
    lower case days' name. Then the program fill corresponding clasess reading 
    each row of the CSV file storing the weekly schedule. 
    A report is generated from that information and stored in a file with 
    name format `report_[today's timestamp].txt`."""

    schedules_df = load_schedules("schedules.csv")
    schedules_df["Day"] = schedules_df["Day"].apply(lambda x: lowercase(x))
    schedules_df["Shift"] = schedules_df["Shift"].apply(lambda x: lowercase(x))

    
    schedule = Schedule()

    # Populate objects from CSV file
    for index, row in schedules_df.iterrows():
        shift = Shift(day_of_week=row["Day"], shift_type=row["Shift"])
        employee = Employee(id=row["EmployeeID"], name=row["Name"], shifts=[shift])
        schedule.add_employee(employee)
        del employee, shift
    
    # Check business rules for the given weekly schedule.
    schedule.validate_rules()
    report = Report(schedule)

    # Write a txt file with the resulting output.
    report_file_name = report.write_report()

    # The report is printed n order to show it in console.
    with open(report_file_name, 'r') as file:
        report_content = file.read()

    print(report_content)


    
        