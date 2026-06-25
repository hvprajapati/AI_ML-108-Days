import json

FILE_NAME = "data/expenses.json"


def save_expenses(expenses):

    with open(
        FILE_NAME,
        "w"
    ) as file:

        json.dump(
            expenses,
            file,
            indent=4
        )


def load_expenses():

    try:

        with open(
            FILE_NAME,
            "r"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []