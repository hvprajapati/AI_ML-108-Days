from managers.expense_manager import (
    add_expense,
    view_expenses,
    delete_expense,
    search_expense
)

from storage.file_handler import (
    load_expenses,
    save_expenses
)

from reports.report_generator import (
    show_summary
)

from utils.validators import (
    validate_amount,
    validate_category
)

expenses = load_expenses()

while True:

    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Delete Expense")
    print("5. Summary Report")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":

        try:
            amount = float(input("Amount: "))
            category = input("Category: ")
            description = input("Description: ")

            if not validate_amount(amount):
                print("Error: Amount must be positive")
                continue

            if not validate_category(category):
                print("Error: Category cannot be empty")
                continue

            add_expense(
                expenses,
                amount,
                category,
                description
            )

            save_expenses(expenses)

        except ValueError:
            print("Error: Invalid amount entered")

    elif choice == "2":

        view_expenses(expenses)

    elif choice == "3":

        keyword = input("Search: ")

        search_expense(
            expenses,
            keyword
        )

    elif choice == "4":

        expense_id = int(
            input("Expense ID: ")
        )

        delete_expense(
            expenses,
            expense_id
        )

        save_expenses(expenses)

    elif choice == "5":

        show_summary(expenses)

    elif choice == "6":

        save_expenses(expenses)

        print("Goodbye!")
        break

    else:

        print("Invalid Choice")