def show_summary(expenses):

    if not expenses:

        print("No Expenses Found")
        return

    total = 0

    category_summary = {}

    for expense in expenses:

        total += expense["amount"]

        category = expense["category"]

        category_summary[
            category
        ] = category_summary.get(
            category,
            0
        ) + expense["amount"]

    print("\n===== SUMMARY =====")

    print(
        f"Total Expense: ₹{total}"
    )

    print("\nCategory Wise Spending")

    for category, amount in (
        category_summary.items()
    ):

        print(
            f"{category}: ₹{amount}"
        )