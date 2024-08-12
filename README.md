# rule-based-role
Rule-based system for managing and validating a simplified employee scheduling system.

## Introduction
This project is a Rule-Based Role Management System developed as part of a coding challenge. The system allows for managing and validating employee schedules based on predefined rules and constraints. The project is implemented in Python, using Docker for containerization. I intended to keep it simple while using pure Python as far as I could instead of use Pandas methods and functions.

In my solution you'll find that I use multiple classes in order to conceptually abstract each component of the challenge. The classes that you'll find are:

1. **`Employee`**: Each employee is defined through a `name`, `id` and a list of `shifts`.
2. **`Shift`**: Each shift is defined with a `day_of_week`, `shift_type` (`morning`, `afternoon`, `night`).
3. **`Schedule`**: The Class in this challenge. Its attributes are: 
    - A dictionary of `employees`
    - A set of `Rules` that validates the business logic.
    - A summary of all the violated rules with the evidence needed to dump the information into a `Report`.
4. **`RuleError`**: Class used to define the message to show when a given Rule is not satisfied.
5. **`Report`**: The report itself. It contains a `schedule` as attribute and a `write_report` method in order to write the report in a `txt`file.

The main reason about my decision of writing this code in a OOP fashion is to make it easy to read and follow, and also to keep it close to a code state in which is easy to turn this solution into a micro-service itself. In that case we would have to replace the data feeding process in order to read the data from a DB and also to store the Report in a DB schema. Having elements defined with Classes is easier to migrate the code.

## Features
- Rule-based scheduling and role management.
- Validation of employee schedules.
- Containerized using Docker for easy deployment.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pablovera-ML/rule-based-role.git
   cd rule-based-role
   ```

## Requirements
- Docker
- Python 3.11
- Required Python packages listed in `requirements.txt`

## Usage

In order to get a report right after installing Docker is by running:
```
$> make full-rebuild
```

This should print out in the console something like:

```
* Employee ID 106. Name Adam Back. 
 Violated rules: 
   - Inconsistent names for the same Employee ID.
     - Examples: Susan Lindström. 
* Employee ID 101. Name John Doe. 
 Violated rules: 
   - Employee worked two consecutive night shifts.
     - Examples: Friday, Saturday. 
   - Employee worked more than 5 days in a week.
     - Examples: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday. 
   - Employee worked more than 1 shift per day.
     - Examples: Monday. 
* Employee ID 102. Name Jane Smith. 
 Violated rules: 
   - Employee worked two consecutive night shifts.
     - Examples: Monday, Tuesday. 
* Employee ID 103. Name Pablo Vera. 
 Violated rules: 
   - Employee worked more than 5 days in a week.
     - Examples: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday. 
   - Employee worked more than 1 shift per day.
     - Examples: Thursday. 
* Employee ID 104. Name Susan Lindström. 
 Violated rules: 
   - Employee worked more than 1 shift per day.
     - Examples: Friday. 
```

Otherwise, if you want to run the code locally by creating a new Python environment you can run:
```
$> make run-locally
```
The output should be the same as before, but this time you'll see a `txt` file generated in your machine.

