"""
Day 27 - Utility Helpers
Concepts: Static Methods, Input Validation, Formatting

Helper functions to keep the main code clean.
These are NOT classes  --  just regular utility functions.
Sometimes plain functions are BETTER than methods!
"""


def get_valid_input(prompt: str, validator=None, error_msg: str = "Invalid input!"):
    """
    Keep asking until the user enters valid input.

    Args:
        prompt:     The message to show the user.
        validator:  A function that returns True/False (e.g., str.isdigit).
        error_msg:  What to print when validation fails.

    Returns:
        The validated input string.
    """
    while True:
        value = input(prompt).strip()
        if not value:
            print("   Input cannot be empty!")
            continue
        if validator is None or validator(value):
            return value
        print(f"   {error_msg}")


def get_positive_float(prompt: str) -> float:
    """Get a positive float from the user."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("   Value cannot be negative!")
                continue
            return value
        except ValueError:
            print("   Please enter a valid number!")


def get_positive_int(prompt: str) -> int:
    """Get a positive integer from the user."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 0:
                print("   Value cannot be negative!")
                continue
            return value
        except ValueError:
            print("   Please enter a valid integer!")


def get_int_in_range(prompt: str, min_val: int, max_val: int) -> int:
    """Get an integer within a specific range."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"   Please enter a number between {min_val} and {max_val}!")
        except ValueError:
            print("   Please enter a valid integer!")


def confirm_action(prompt: str) -> bool:
    """Ask for yes/no confirmation. Returns True for 'y'."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("   Please enter 'y' or 'n'!")


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_success(message: str):
    """Print a success message."""
    print(f"  [OK] {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"  [X] {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"  [i] {message}")


def print_table(headers: list, rows: list):
    """
    Print a formatted table.

    Args:
        headers: List of column header strings.
        rows:    List of tuples, each tuple is one row.
    """
    if not rows:
        print("   (No data)")
        return

    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)

    # Print header
    header_line = ""
    for i, header in enumerate(headers):
        header_line += f"{header:<{col_widths[i]}}"
    print(f"   {header_line}")
    print(f"   {'-' * (sum(col_widths))}")

    # Print rows
    for row in rows:
        row_line = ""
        for i, cell in enumerate(row):
            row_line += f"{str(cell):<{col_widths[i]}}"
        print(f"   {row_line}")


# ===== QUICK TEST ===============================================================
if __name__ == "__main__":
    print("Testing helpers...")

    # Test print_table
    headers = ["ID", "Name", "Type"]
    rows = [
        (1, "The Alchemist", "Physical"),
        (2, "Clean Code", "EBook"),
        (3, "Atomic Habits", "AudioBook"),
    ]
    print_table(headers, rows)

    print("\nAll helpers working!")
