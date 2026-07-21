"""
DAY 21 -- OOP MINI PROJECT: Library Management System
================================================================
[GOAL] Build a complete Library Management System using OOP.

TODAY'S CONCEPTS (tying Days 16-20 together):
    [x] Full OOP design with classes, inheritance, polymorphism
    [x] File I/O with JSON serialization
    [x] Search and filter functionality
    [x] Dunder methods (__len__, __contains__, __iter__)
    [x] Input validation with helper functions
    [x] Complete interactive CLI menu system
    [x] Real-world project structure (models/, storage/, utils/)

THIS IS THE FINAL PRODUCT  --  a fully working Library Management System!

RUN IT:   python main.py
TEST IT:  python main.py --demo    (runs automatic demo)

INSTRUCTIONS:
    1. Run 'python main.py' for the interactive menu
    2. Run 'python main.py --demo' to see an automatic demo
    3. Explore the code structure  --  this is how real projects are organized!
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.book import Book, PhysicalBook, EBook, AudioBook
from models.member import Member, StudentMember, PremiumMember
from models.library import Library
from storage.file_handler import FileHandler
from utils.helpers import (
    get_valid_input, get_positive_float, get_positive_int,
    get_int_in_range, confirm_action,
    print_header, print_success, print_error, print_info, print_table
)

# ---- Configuration ------------------------------------------------------------
DATA_FILE = "library_data.json"


# ==============================================================================
# MENU HANDLERS
# ==============================================================================

def menu_books(library: Library):
    """Book management sub-menu."""
    while True:
        print_header("[MANAGE BOOKS]")
        print("   1. Add Physical Book")
        print("   2. Add EBook")
        print("   3. Add AudioBook")
        print("   4. View All Books")
        print("   5. View Available Books")
        print("   6. View Borrowed Books")
        print("   7. Search Books")
        print("   8. Filter by Type")
        print("   9. Remove a Book")
        print("   0. Back to Main Menu")

        choice = input("\n   Enter choice: ").strip()

        if choice == "0": break
        elif choice == "1": _add_physical_book(library)
        elif choice == "2": _add_ebook(library)
        elif choice == "3": _add_audiobook(library)
        elif choice == "4": print_header("[ALL BOOKS]"); library.list_all_books()
        elif choice == "5": print_header("[AVAILABLE BOOKS]"); library.list_available_books()
        elif choice == "6": print_header("[BORROWED BOOKS]"); library.list_borrowed_books()
        elif choice == "7": _search_books(library)
        elif choice == "8": _filter_books(library)
        elif choice == "9": _remove_book(library)
        else: print_error("Invalid choice!")

        if choice in ("4", "5", "6", "7", "8"):
            input("\n   Press Enter to continue...")


def menu_members(library: Library):
    """Member management sub-menu."""
    while True:
        print_header("[MANAGE MEMBERS]")
        print("   1. Register Regular Member")
        print("   2. Register Student Member")
        print("   3. Register Premium Member")
        print("   4. View All Members")
        print("   5. Search Members")
        print("   6. Member Report (detailed)")
        print("   7. Remove a Member")
        print("   0. Back to Main Menu")

        choice = input("\n   Enter choice: ").strip()

        if choice == "0": break
        elif choice == "1": _add_regular_member(library)
        elif choice == "2": _add_student_member(library)
        elif choice == "3": _add_premium_member(library)
        elif choice == "4": print_header("[ALL MEMBERS]"); library.list_all_members()
        elif choice == "5": _search_members(library)
        elif choice == "6": _member_report(library)
        elif choice == "7": _remove_member(library)
        else: print_error("Invalid choice!")

        if choice in ("4", "5", "6"):
            input("\n   Press Enter to continue...")


def menu_transactions(library: Library):
    """Borrow/Return sub-menu."""
    while True:
        print_header("[TRANSACTIONS]")
        print("   1. Borrow a Book")
        print("   2. Return a Book")
        print("   3. View Borrowed Books")
        print("   0. Back to Main Menu")

        choice = input("\n   Enter choice: ").strip()

        if choice == "0": break
        elif choice == "1": _borrow_book(library)
        elif choice == "2": _return_book(library)
        elif choice == "3": print_header("[BORROWED BOOKS]"); library.list_borrowed_books()

        if choice in ("3",):
            input("\n   Press Enter to continue...")


def menu_reports(library: Library):
    """Reports sub-menu."""
    while True:
        print_header("[REPORTS]")
        print("   1. Library Statistics")
        print("   2. Member Report")
        print("   3. All Books Summary")
        print("   0. Back to Main Menu")

        choice = input("\n   Enter choice: ").strip()

        if choice == "0": break
        elif choice == "1": library.show_statistics()
        elif choice == "2":
            member_id = get_positive_int("   Enter Member ID: ")
            print(library.get_member_report(member_id))
        elif choice == "3":
            print_header("[BOOKS SUMMARY]")
            print(f"   Total: {library.total_books} | "
                  f"Available: {library.available_books_count} | "
                  f"Borrowed: {library.borrowed_books_count}")
            library.list_all_books()
        else:
            print_error("Invalid choice!")

        if choice in ("1", "2", "3"):
            input("\n   Press Enter to continue...")


# ==============================================================================
# BOOK OPERATIONS
# ==============================================================================

def _get_next_book_id(library: Library) -> int:
    """Generate the next available book ID."""
    if not library.books:
        return 1
    return max(b.book_id for b in library.books) + 1


def _add_physical_book(library: Library):
    """Add a PhysicalBook to the library."""
    print_header("[Add Physical Book]")
    try:
        book_id = _get_next_book_id(library)
        print_info(f"Auto-generated Book ID: {book_id}")
        title = input("   Title: ").strip()
        if not title: print_error("Title cannot be empty!"); return
        author = input("   Author: ").strip()
        if not author: print_error("Author cannot be empty!"); return
        price = get_positive_float("   Price (Rs.): ")
        weight = get_positive_float("   Weight (grams): ")
        shelf = input("   Shelf Location: ").strip()
        if not shelf: shelf = "Unassigned"

        book = PhysicalBook(book_id, title, author, price, weight, shelf)
        library.add_book(book)
        print_success(f"Added: {book}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _add_ebook(library: Library):
    """Add an EBook to the library."""
    print_header("[Add EBook]")
    try:
        book_id = _get_next_book_id(library)
        print_info(f"Auto-generated Book ID: {book_id}")
        title = input("   Title: ").strip()
        if not title: print_error("Title cannot be empty!"); return
        author = input("   Author: ").strip()
        if not author: print_error("Author cannot be empty!"); return
        price = get_positive_float("   Price (Rs.): ")
        file_size = get_positive_float("   File Size (MB): ")

        print("   Format options: PDF, EPUB, MOBI, AZW3")
        format = get_valid_input(
            "   Format: ",
            validator=lambda v: v.upper() in ("PDF", "EPUB", "MOBI", "AZW3"),
            error_msg="Please enter a valid format (PDF, EPUB, MOBI, AZW3)!"
        )

        book = EBook(book_id, title, author, price, file_size, format.upper())
        library.add_book(book)
        print_success(f"Added: {book}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _add_audiobook(library: Library):
    """Add an AudioBook to the library."""
    print_header("[Add AudioBook]")
    try:
        book_id = _get_next_book_id(library)
        print_info(f"Auto-generated Book ID: {book_id}")
        title = input("   Title: ").strip()
        if not title: print_error("Title cannot be empty!"); return
        author = input("   Author: ").strip()
        if not author: print_error("Author cannot be empty!"); return
        price = get_positive_float("   Price (Rs.): ")
        duration = get_positive_int("   Duration (minutes): ")
        narrator = input("   Narrator: ").strip()
        if not narrator: narrator = "Unknown"

        book = AudioBook(book_id, title, author, price, duration, narrator)
        library.add_book(book)
        print_success(f"Added: {book}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _search_books(library: Library):
    """Search books by keyword."""
    print_header("[Search Books]")
    keyword = input("   Enter keyword (title or author): ").strip()
    if not keyword:
        print_error("Keyword cannot be empty!"); return

    results = library.search_books(keyword)
    if results:
        print_success(f"Found {len(results)} matching book(s):")
        for book in results:
            print(f"   {book.get_info()}")
    else:
        print_info(f"No books matching '{keyword}' found.")


def _filter_books(library: Library):
    """Filter books by type."""
    print_header("[Filter by Type]")
    print("   1. Physical Books")
    print("   2. EBooks")
    print("   3. AudioBooks")
    print("   4. Available Only")
    print("   5. Borrowed Only")
    choice = input("\n   Enter choice: ").strip()

    type_map = {"1": "physical", "2": "ebook", "3": "audiobook"}
    if choice in type_map:
        results = library.filter_by_type(type_map[choice])
        label = type_map[choice].capitalize()
    elif choice == "4":
        results = library.filter_by_status("available")
        label = "Available"
    elif choice == "5":
        results = library.filter_by_status("borrowed")
        label = "Borrowed"
    else:
        print_error("Invalid choice!"); return

    if results:
        print_success(f"{label} books ({len(results)}):")
        for book in results:
            print(f"   {book.get_info()}")
    else:
        print_info(f"No {label.lower()} books found.")


def _remove_book(library: Library):
    """Remove a book from the library."""
    print_header("[Remove Book]")
    book_id = get_positive_int("   Enter Book ID to remove: ")
    try:
        book = library.find_book_by_id(book_id)
        if book is None:
            print_error(f"Book ID {book_id} not found!"); return
        print(f"   Book: {book.get_info()}")
        if confirm_action("   Are you sure you want to remove this book?"):
            library.remove_book(book_id)
            print_success(f"Book '{book.title}' removed!")
            _auto_save(library)
    except ValueError as e:
        print_error(str(e))


# ==============================================================================
# MEMBER OPERATIONS
# ==============================================================================

def _get_next_member_id(library: Library) -> int:
    """Generate the next available member ID."""
    if not library.members:
        return 101  # Start member IDs from 101
    return max(m.member_id for m in library.members) + 1


def _add_regular_member(library: Library):
    """Register a regular member."""
    print_header("[Register Regular Member]")
    try:
        member_id = _get_next_member_id(library)
        print_info(f"Auto-generated Member ID: {member_id}")
        name = input("   Full Name: ").strip()
        if not name: print_error("Name cannot be empty!"); return
        email = get_valid_input(
            "   Email: ",
            validator=lambda v: "@" in v,
            error_msg="Email must contain '@'!"
        )
        phone = get_valid_input(
            "   Phone (10 digits): ",
            validator=lambda v: v.replace("-","").replace(" ","").isdigit()
                                and len(v.replace("-","").replace(" ","")) == 10,
            error_msg="Phone must be exactly 10 digits!"
        )

        member = Member(member_id, name, email, phone)
        library.add_member(member)
        print_success(f"Registered: {member}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _add_student_member(library: Library):
    """Register a student member."""
    print_header("[Register Student Member]")
    try:
        member_id = _get_next_member_id(library)
        print_info(f"Auto-generated Member ID: {member_id}")
        name = input("   Full Name: ").strip()
        if not name: print_error("Name cannot be empty!"); return
        email = get_valid_input(
            "   Email: ",
            validator=lambda v: "@" in v,
            error_msg="Email must contain '@'!"
        )
        phone = get_valid_input(
            "   Phone (10 digits): ",
            validator=lambda v: v.replace("-","").replace(" ","").isdigit()
                                and len(v.replace("-","").replace(" ","")) == 10,
            error_msg="Phone must be exactly 10 digits!"
        )
        student_id = get_valid_input(
            "   Student ID (starts with STU): ",
            validator=lambda v: v.startswith("STU"),
            error_msg="Student ID must start with 'STU' (e.g., STU2024001)!"
        )

        member = StudentMember(member_id, name, email, phone, student_id)
        library.add_member(member)
        print_success(f"Registered: {member}")
        print_info(f"   Fee: Rs.200 | Max Books: {member.MAX_BOOKS_ALLOWED}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _add_premium_member(library: Library):
    """Register a premium member."""
    print_header("[Register Premium Member]")
    try:
        member_id = _get_next_member_id(library)
        print_info(f"Auto-generated Member ID: {member_id}")
        name = input("   Full Name: ").strip()
        if not name: print_error("Name cannot be empty!"); return
        email = get_valid_input(
            "   Email: ",
            validator=lambda v: "@" in v,
            error_msg="Email must contain '@'!"
        )
        phone = get_valid_input(
            "   Phone (10 digits): ",
            validator=lambda v: v.replace("-","").replace(" ","").isdigit()
                                and len(v.replace("-","").replace(" ","")) == 10,
            error_msg="Phone must be exactly 10 digits!"
        )
        priority = confirm_action("   Enable priority service?")

        member = PremiumMember(member_id, name, email, phone, priority)
        library.add_member(member)
        print_success(f"Registered: {member}")
        print_info(f"   Fee: Rs.1500 | Max Books: {member.MAX_BOOKS_ALLOWED}")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _search_members(library: Library):
    """Search members by name or email."""
    print_header("[Search Members]")
    keyword = input("   Enter keyword (name or email): ").strip()
    if not keyword:
        print_error("Keyword cannot be empty!"); return

    results = library.search_members(keyword)
    if results:
        print_success(f"Found {len(results)} matching member(s):")
        for member in results:
            print(f"   {member.get_info()}")
    else:
        print_info(f"No members matching '{keyword}' found.")


def _member_report(library: Library):
    """Show detailed report for a member."""
    print_header("[Member Report]")
    member_id = get_positive_int("   Enter Member ID: ")
    report = library.get_member_report(member_id)
    print(report)


def _remove_member(library: Library):
    """Remove a member from the library."""
    print_header("[Remove Member]")
    member_id = get_positive_int("   Enter Member ID to remove: ")
    try:
        member = library.find_member_by_id(member_id)
        if member is None:
            print_error(f"Member ID {member_id} not found!"); return
        print(f"   Member: {member.get_info()}")
        if confirm_action("   Are you sure you want to remove this member?"):
            library.remove_member(member_id)
            print_success(f"Member '{member.name}' removed!")
            _auto_save(library)
    except ValueError as e:
        print_error(str(e))


# ==============================================================================
# TRANSACTION OPERATIONS
# ==============================================================================

def _borrow_book(library: Library):
    """Process a book borrow."""
    print_header("[Borrow a Book]")

    # Show available books
    available = [b for b in library.books if not b.is_borrowed]
    if not available:
        print_info("No books are currently available!"); return

    print("   Available books:")
    for book in available:
        print(f"     ID {book.book_id}: '{book.title}' by {book.author} [{book.get_type()}]")

    book_id = get_positive_int("\n   Enter Book ID to borrow: ")
    member_id = get_positive_int("   Enter Member ID: ")

    try:
        library.borrow_book(book_id, member_id)
        book = library.find_book_by_id(book_id)
        member = library.find_member_by_id(member_id)
        print_success(f"'{book.title}' borrowed by {member.name}!")
        print_info(f"   {member.name} now has {member.books_borrowed_count}/{member.MAX_BOOKS_ALLOWED} books")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


def _return_book(library: Library):
    """Process a book return."""
    print_header("[Return a Book]")

    # Show borrowed books
    borrowed = [b for b in library.books if b.is_borrowed]
    if not borrowed:
        print_info("No books are currently borrowed!"); return

    print("   Borrowed books:")
    for book in borrowed:
        member = library.find_member_by_id(book.borrowed_by)
        name = member.name if member else "Unknown"
        print(f"     ID {book.book_id}: '{book.title}'  --  with {name} (Member #{book.borrowed_by})")

    book_id = get_positive_int("\n   Enter Book ID to return: ")
    member_id = get_positive_int("   Enter Member ID returning it: ")

    try:
        library.return_book(book_id, member_id)
        book = library.find_book_by_id(book_id)
        member = library.find_member_by_id(member_id)
        print_success(f"'{book.title}' returned by {member.name}!")
        _auto_save(library)
    except ValueError as e:
        print_error(str(e))


# ==============================================================================
# DATA PERSISTENCE
# ==============================================================================

def _auto_save(library: Library):
    """Save library data to file (called after every modification)."""
    try:
        FileHandler.save_library(library, DATA_FILE)
    except Exception as e:
        print_error(f"Could not save data: {e}")


def load_data(library: Library) -> bool:
    """Load library data from file. Returns True if loaded, False if new."""
    if os.path.exists(DATA_FILE):
        success = FileHandler.load_library(library, DATA_FILE)
        if success:
            print_success(f"Data loaded from '{DATA_FILE}'")
            print_info(f"{library}")
            return True

    print_info("No existing data found  --  starting with an empty library.")
    print_info("Add some books and members to get started!")
    return False


# ==============================================================================
# SEED DATA (for demo / first-time use)
# ==============================================================================

def seed_sample_data(library: Library):
    """Populate the library with sample data for testing."""
    # Sample books
    books = [
        PhysicalBook(1, "The Alchemist", "Paulo Coelho", 299.0,
                     weight=350, shelf_location="A-12"),
        PhysicalBook(2, "1984", "George Orwell", 249.0,
                     weight=280, shelf_location="B-03"),
        PhysicalBook(3, "To Kill a Mockingbird", "Harper Lee", 399.0,
                     weight=420, shelf_location="A-01"),
        EBook(4, "Clean Code", "Robert C. Martin", 599.0,
              file_size_mb=8.5, format="PDF"),
        EBook(5, "Design Patterns", "Gang of Four", 799.0,
              file_size_mb=15.0, format="PDF"),
        EBook(6, "Sapiens", "Yuval Noah Harari", 499.0,
              file_size_mb=12.0, format="EPUB"),
        AudioBook(7, "Atomic Habits", "James Clear", 399.0,
                  duration_minutes=332, narrator="James Clear"),
        AudioBook(8, "Deep Work", "Cal Newport", 449.0,
                  duration_minutes=465, narrator="Mike Chamberlain"),
        AudioBook(9, "The Power of Habit", "Charles Duhigg", 349.0,
                  duration_minutes=562, narrator="Mike Chamberlain"),
    ]

    for book in books:
        library.add_book(book)

    # Sample members
    members = [
        Member(101, "Rahul Sharma", "rahul@email.com", "9876543210"),
        StudentMember(102, "Priya Patel", "priya@email.com", "9123456780",
                      student_id="STU2024001"),
        PremiumMember(103, "Amit Kumar", "amit@email.com", "9988776655",
                      priority_service=True),
        StudentMember(104, "Sneha Reddy", "sneha@email.com", "9876501234",
                      student_id="STU2024002"),
        PremiumMember(105, "Vikram Singh", "vikram@email.com", "9900112233",
                      priority_service=False),
    ]

    for member in members:
        library.add_member(member)

    # Borrow some books
    library.borrow_book(1, 101)
    library.borrow_book(4, 102)
    library.borrow_book(7, 103)
    library.borrow_book(2, 103)
    library.borrow_book(8, 104)

    print_success("Sample data loaded!")


# ==============================================================================
# MAIN
# ==============================================================================

def run_auto_demo(library: Library):
    """Run an automatic demo of the system."""
    print_header("[AUTO DEMO MODE]")
    seed_sample_data(library)

    print("\n   [ALL BOOKS]:")
    library.list_all_books()

    print(f"\n   [ALL MEMBERS]:")
    library.list_all_members()

    print(f"\n   [BORROWED]:")
    library.list_borrowed_books()

    print(f"\n   [SEARCH 'alchemist']:")
    for b in library.search_books("alchemist"):
        print(f"     {b.get_info()}")

    print(f"\n   [FILTER EBooks]:")
    for b in library.filter_by_type("ebook"):
        print(f"     {b.get_info()}")

    library.show_statistics()

    print(f"\n   [MEMBER REPORT for Priya]:")
    print(library.get_member_report(102))

    print(f"\n   [DUNDER TESTS]:")
    print(f"     len(library) = {len(library)}")
    print(f"     5 in library = {5 in library}")
    print(f"     99 in library = {99 in library}")

    print(f"\n   [ITERATION] for book in library:")
    for book in library:
        print(f"     {book}")


def run_interactive(library: Library):
    """Run the interactive CLI menu."""
    while True:
        print_header("[MAIN MENU]")
        print(f"   {library}")
        print(f"   Books: {library.total_books} ({library.available_books_count} available) | "
              f"Members: {library.total_members}")
        print("-" * 60)
        print("   1. Manage Books")
        print("   2. Manage Members")
        print("   3. Borrow / Return")
        print("   4. Reports")
        print("   5. Load Sample Data")
        print("   6. Save Data")
        print("   0. Exit")
        print("-" * 60)

        choice = input("   Enter choice: ").strip()

        if choice == "0":
            print_header("[Goodbye!]")
            _auto_save(library)
            print_success("Data saved. Thank you for using the Library System!")
            break
        elif choice == "1":
            menu_books(library)
        elif choice == "2":
            menu_members(library)
        elif choice == "3":
            menu_transactions(library)
        elif choice == "4":
            menu_reports(library)
        elif choice == "5":
            if confirm_action("   This will add sample data. Continue?"):
                seed_sample_data(library)
                _auto_save(library)
        elif choice == "6":
            _auto_save(library)
            print_success("Data saved manually!")
        else:
            print_error("Invalid choice! Please enter 0-6.")


def main():
    """Main entry point for Day 27."""
    print("=" * 60)
    print("  DAY 21: LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("  Complete OOP Project  --  CLI + File Storage + Reports")
    print("=" * 60)

    # Create the library
    library = Library("My Library")

    # Try to load existing data
    load_data(library)

    # Check for --demo flag
    if "--demo" in sys.argv:
        run_auto_demo(library)
        _auto_save(library)
    else:
        run_interactive(library)

    print("\n" + "=" * 60)
    print("  Thank you for using the Library Management System!")
    print("  Day 21 OOP Project Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
