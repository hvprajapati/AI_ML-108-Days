from datetime import datetime


def add_expense(
    expenses,
    amount,
    category,
    description
):

    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(datetime.now().date())
    }

    expenses.append(expense)

    print("Expense Added Successfully")


def view_expenses(expenses):

    if not expenses:

        print("No Expenses Found")
        return

    for expense in expenses:

        print("-" * 50)

        print(
            f"ID: {expense['id']}"
        )

        print(
            f"Amount: ₹{expense['amount']}"
        )

        print(
            f"Category: {expense['category']}"
        )

        print(
            f"Description: {expense['description']}"
        )

        print(
            f"Date: {expense['date']}"
        )


def search_expense(
    expenses,
    keyword
):

    found = False

    for expense in expenses:

        if keyword.lower() in expense[
            "description"
        ].lower():

            print(expense)

            found = True

    if not found:

        print("No Match Found")


def delete_expense(
    expenses,
    expense_id
):

    for expense in expenses:

        if expense["id"] == expense_id:

            expenses.remove(expense)

            print("Deleted Successfully")

            return

    print("Expense Not Found")