import json
import os

FILE_NAME = "data/expenses.json"


def save_expenses(expenses):

    # Create data directory if it doesn't exist
    os.makedirs(
        os.path.dirname(FILE_NAME),
        exist_ok=True
    )

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