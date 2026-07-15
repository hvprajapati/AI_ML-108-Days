# Day 30 - Final Capstone Project

## Student Management System

### What You Will Build
A complete Student Management System that uses everything you learned in the past 29 days.

### Requirements

Your program should:
1. **Load/Save** student data from a JSON file
2. **Add** new students with name, age, grade, and marks in 5 subjects
3. **View** all students in a formatted table
4. **Search** students by name or grade
5. **Update** student information
6. **Delete** students
7. **Generate** a report showing:
   - Total students
   - Average marks per subject
   - Top 3 students
   - Grade distribution (pie chart using matplotlib)
8. **Handle errors** gracefully (invalid input, missing files, etc.)

### Project Structure
```
day 30 - final project/
    student_system.py    # Main CLI application
    models/
        __init__.py
        student.py        # Student class with properties
    utils/
        __init__.py
        file_handler.py   # JSON save/load
        helpers.py        # Input validation, formatting
```

### OOP Requirements
- Use a `Student` class with:
  - Private attributes (name, age, grade, marks dict)
  - @property for controlled access
  - __str__ and __repr__
  - Method: calculate_average(), get_grade()
- Optional: Inherit from a `Person` base class

### What This Tests
| Skill | From Days |
|-------|-----------|
| Classes & Objects | Days 16-17 |
| Properties & Encapsulation | Day 17 |
| Inheritance (optional) | Day 19 |
| File I/O & JSON | Days 13, 22 |
| Exception Handling | Day 14 |
| List/Dict Comprehensions | Day 10 |
| Input Validation | Day 8 |
| Modules & Imports | Day 11 |
| Matplotlib | Day 27 |

### Starter Code (in student_system.py)
```python
"""
Day 30 - Final Project: Student Management System
This is YOUR project. The structure is provided — you fill in the code.
"""

import json
import os
import sys
from models.student import Student
from utils.file_handler import load_students, save_students
from utils.helpers import get_input, print_table


def main():
    """Main CLI loop."""
    students = load_students("students.json")
    
    while True:
        print("\n" + "=" * 50)
        print("  STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search Student")
        print("  4. Update Student")
        print("  5. Delete Student")
        print("  6. Generate Report")
        print("  0. Exit")
        print("-" * 50)
        
        choice = input("  Enter choice: ").strip()
        
        if choice == "0":
            save_students(students, "students.json")
            print("Goodbye!")
            break
        elif choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            generate_report(students)
        else:
            print("Invalid choice!")


# TODO: Implement these functions:
# def add_student(students): ...
# def view_students(students): ...
# def search_student(students): ...
# def update_student(students): ...
# def delete_student(students): ...
# def generate_report(students): ...


if __name__ == "__main__":
    main()
```

### Hints
- `Student` class goes in `models/student.py`
- Use `json.load()` and `json.dump()` for file operations
- Use a list comprehension to calculate averages
- Use `try/except` for file operations and input parsing
- The report should use `matplotlib.pyplot.pie()` for grade distribution

### Grading Rubric
| Feature | Points |
|---------|--------|
| Working CLI menu | 20 |
| Add/View/Search/Delete work | 25 |
| JSON save/load works | 15 |
| Student class with properties | 15 |
| Error handling | 10 |
| Report with chart | 10 |
| Clean code & comments | 5 |
| **Total** | **100** |

Good luck! This is what separates a Python student from a Python developer.
