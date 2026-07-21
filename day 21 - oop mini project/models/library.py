"""
Day 27 - Complete Library Class
Concepts: Composition, Delegation, Search, Statistics, Dunder Methods

This is the FULL Library class  --  the central controller of our system.
It coordinates all operations between Books and Members.

New for Day 27: Search, Advanced Reports, Dunder Methods, Integration with FileHandler
"""

from models.book import Book, PhysicalBook, EBook, AudioBook
from models.member import Member, StudentMember, PremiumMember


class Library:
    """
    Complete Library Management System.

    Responsibilities:
        - Manage book inventory (add, remove, search)
        - Manage member registry (register, remove, find)
        - Coordinate borrow/return operations
        - Generate reports and statistics
    """

    def __init__(self, name: str = "My Library"):
        self.name = name
        self._books = []
        self._members = []

    # ---- Properties -----------------------------------------------------------
    @property
    def books(self) -> list:
        return self._books.copy()

    @property
    def members(self) -> list:
        return self._members.copy()

    @property
    def total_books(self) -> int:
        return len(self._books)

    @property
    def total_members(self) -> int:
        return len(self._members)

    @property
    def available_books_count(self) -> int:
        return sum(1 for b in self._books if not b.is_borrowed)

    @property
    def borrowed_books_count(self) -> int:
        return sum(1 for b in self._books if b.is_borrowed)

    # ---- Book Management ------------------------------------------------------
    def add_book(self, book: Book):
        """Add a book (any type) to the library."""
        if any(b.book_id == book.book_id for b in self._books):
            raise ValueError(f"Book with ID {book.book_id} already exists!")
        self._books.append(book)

    def find_book_by_id(self, book_id: int) -> Book:
        """Find a book by ID. Returns Book or None."""
        for book in self._books:
            if book.book_id == book_id:
                return book
        return None

    def remove_book(self, book_id: int):
        """Remove a book (only if not borrowed)."""
        book = self.find_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book ID {book_id} not found!")
        if book.is_borrowed:
            raise ValueError(f"Cannot remove '{book.title}'  --  it is currently borrowed!")
        self._books.remove(book)

    # New for Day 27: SEARCH functionality --------------------------------------

    def search_books_by_title(self, keyword: str) -> list:
        """
        Search books by title (case-insensitive substring match).

        Args:
            keyword: Search term to look for in titles.

        Returns:
            List of matching Book objects (empty if nothing matches).
        """
        keyword_lower = keyword.lower()
        return [b for b in self._books if keyword_lower in b.title.lower()]

    def search_books_by_author(self, keyword: str) -> list:
        """Search books by author name."""
        keyword_lower = keyword.lower()
        return [b for b in self._books if keyword_lower in b.author.lower()]

    def search_books(self, keyword: str) -> list:
        """Search in BOTH title and author."""
        keyword_lower = keyword.lower()
        return [
            b for b in self._books
            if keyword_lower in b.title.lower() or keyword_lower in b.author.lower()
        ]

    def filter_by_type(self, book_type: str) -> list:
        """
        Filter books by type.

        Args:
            book_type: "Physical", "EBook", or "AudioBook"

        Returns:
            List of matching Book objects.
        """
        type_map = {
            "physical": PhysicalBook,
            "ebook": EBook,
            "audiobook": AudioBook,
        }
        target_class = type_map.get(book_type.lower())
        if target_class is None:
            # Try matching by get_type() string
            return [b for b in self._books if b.get_type().lower() == book_type.lower()]
        return [b for b in self._books if isinstance(b, target_class)]

    def filter_by_status(self, status: str) -> list:
        """Filter by 'available' or 'borrowed'."""
        if status.lower() == "available":
            return [b for b in self._books if not b.is_borrowed]
        elif status.lower() == "borrowed":
            return [b for b in self._books if b.is_borrowed]
        return []

    # ---- Member Management ----------------------------------------------------
    def add_member(self, member: Member):
        """Register a new member."""
        if any(m.member_id == member.member_id for m in self._members):
            raise ValueError(f"Member with ID {member.member_id} already exists!")
        self._members.append(member)

    def find_member_by_id(self, member_id: int) -> Member:
        """Find a member by ID. Returns Member or None."""
        for member in self._members:
            if member.member_id == member_id:
                return member
        return None

    def search_members(self, keyword: str) -> list:
        """Search members by name or email."""
        keyword_lower = keyword.lower()
        return [
            m for m in self._members
            if keyword_lower in m.name.lower() or keyword_lower in m.email.lower()
        ]

    def remove_member(self, member_id: int):
        """Remove a member (only if no books borrowed)."""
        member = self.find_member_by_id(member_id)
        if member is None:
            raise ValueError(f"Member ID {member_id} not found!")
        if member.books_borrowed_count > 0:
            raise ValueError(
                f"Cannot remove {member.name}  --  they still have "
                f"{member.books_borrowed_count} borrowed book(s)!"
            )
        self._members.remove(member)

    def get_member_borrowed_books(self, member_id: int) -> list:
        """
        Get all books currently borrowed by a specific member.

        Returns:
            List of Book objects borrowed by the member.
        """
        member = self.find_member_by_id(member_id)
        if member is None:
            return []
        return [b for b in self._books if b.book_id in member.borrowed_books]

    # ---- Borrow & Return ------------------------------------------------------
    def borrow_book(self, book_id: int, member_id: int):
        """Member borrows a book  --  validates and coordinates."""
        book = self.find_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book ID {book_id} not found!")

        member = self.find_member_by_id(member_id)
        if member is None:
            raise ValueError(f"Member ID {member_id} not found!")

        if book.is_borrowed:
            raise ValueError(f"'{book.title}' is already borrowed!")

        if not member.can_borrow():
            raise ValueError(
                f"{member.name} has reached the max limit "
                f"({member.MAX_BOOKS_ALLOWED} books)!"
            )

        book.borrow(member_id)
        member.borrow_book(book_id)

    def return_book(self, book_id: int, member_id: int):
        """Member returns a book."""
        book = self.find_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book ID {book_id} not found!")

        member = self.find_member_by_id(member_id)
        if member is None:
            raise ValueError(f"Member ID {member_id} not found!")

        if not book.is_borrowed:
            raise ValueError(f"'{book.title}' is not currently borrowed!")

        if book.borrowed_by != member_id:
            raise ValueError(
                f"'{book.title}' was borrowed by member {book.borrowed_by}, "
                f"not member {member_id}!"
            )

        book.return_book()
        member.return_book(book_id)

    # ---- Statistics & Reports -------------------------------------------------
    def get_statistics(self) -> dict:
        """Return comprehensive library statistics."""
        return {
            "library_name": self.name,
            "total_books": self.total_books,
            "available": self.available_books_count,
            "borrowed": self.borrowed_books_count,
            "borrow_rate": round(
                (self.borrowed_books_count / self.total_books * 100)
                if self.total_books > 0 else 0, 1
            ),
            "physical_books": sum(1 for b in self._books if isinstance(b, PhysicalBook)),
            "ebooks": sum(1 for b in self._books if isinstance(b, EBook)),
            "audiobooks": sum(1 for b in self._books if isinstance(b, AudioBook)),
            "total_members": self.total_members,
            "students": sum(1 for m in self._members if isinstance(m, StudentMember)),
            "premium": sum(1 for m in self._members if isinstance(m, PremiumMember)),
            "regular": sum(1 for m in self._members
                          if not isinstance(m, StudentMember)
                          and not isinstance(m, PremiumMember)),
            "total_books_borrowed": sum(m.books_borrowed_count for m in self._members),
        }

    def show_statistics(self):
        """Display a formatted statistics report."""
        stats = self.get_statistics()
        print(f"\n   === [Library Statistics: {stats['library_name']}] ===")
        print(f"   Total Books:    {stats['total_books']} "
              f"({stats['available']} available, {stats['borrowed']} borrowed)")
        print(f"   Borrow Rate:    {stats['borrow_rate']}%")
        print(f"   Book Types:     Physical={stats['physical_books']}, "
              f"EBooks={stats['ebooks']}, AudioBooks={stats['audiobooks']}")
        print(f"   Total Members:  {stats['total_members']} "
              f"(Students={stats['students']}, Premium={stats['premium']}, "
              f"Regular={stats['regular']})")
        print(f"   Books in Hands: {stats['total_books_borrowed']}")

    def get_member_report(self, member_id: int) -> str:
        """Generate a detailed report for a specific member."""
        member = self.find_member_by_id(member_id)
        if member is None:
            return f"Member ID {member_id} not found."

        borrowed = self.get_member_borrowed_books(member_id)
        report = f"\n   === Member Report: {member.name} ===\n"
        report += f"   ID: {member.member_id} | Type: {member.get_membership_type()}\n"
        report += f"   Email: {member.email} | Phone: {member.phone}\n"
        report += f"   Fee Paid: Rs.{member.membership_fee:.2f}\n"
        report += f"   Books Currently Borrowed: {len(borrowed)}/{member.MAX_BOOKS_ALLOWED}\n"

        if borrowed:
            report += f"   --- Borrowed Books ---\n"
            for book in borrowed:
                report += f"     - [{book.get_type()}] '{book.title}' by {book.author}\n"

        return report

    # ---- DUNDER METHODS -------------------------------------------------------
    def __str__(self) -> str:
        return (f"Library '{self.name}'  --  "
                f"{self.total_books} books, {self.total_members} members")

    def __repr__(self) -> str:
        return (f"Library(name='{self.name}', books={self.total_books}, "
                f"members={self.total_members})")

    def __len__(self) -> int:
        """len(library) returns total number of books."""
        return self.total_books

    def __contains__(self, book_id: int) -> bool:
        """
        'book_id in library' checks if a book exists.

        Usage:
            if 5 in library:
                print("Book ID 5 exists!")
        """
        return self.find_book_by_id(book_id) is not None

    def __iter__(self):
        """Make Library iterable  --  'for book in library' loops through books."""
        return iter(self._books)

    # ---- Display Methods (used by CLI) ----------------------------------------
    def list_all_books(self):
        """Print all books."""
        if not self._books:
            print("   (No books in the library)")
            return
        for book in self._books:
            print(f"   {book.get_info()}")

    def list_all_members(self):
        """Print all members."""
        if not self._members:
            print("   (No members registered)")
            return
        for member in self._members:
            print(f"   {member.get_info()}")

    def list_available_books(self):
        """Print only available books."""
        available = [b for b in self._books if not b.is_borrowed]
        if not available:
            print("   (No books available)")
            return
        for book in available:
            print(f"   {book.get_info()}")

    def list_borrowed_books(self):
        """Print borrowed books with borrower info."""
        borrowed = [b for b in self._books if b.is_borrowed]
        if not borrowed:
            print("   (No books currently borrowed)")
            return
        for book in borrowed:
            member = self.find_member_by_id(book.borrowed_by)
            borrower_name = member.name if member else "Unknown"
            print(f"   {book.get_info()}")
            print(f"     Borrowed by: {borrower_name} (ID: {book.borrowed_by})")


# ===== QUICK TEST ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 27 -- TESTING COMPLETE LIBRARY")
    print("=" * 60)

    lib = Library("Central Library")

    # Add books
    lib.add_book(PhysicalBook(1, "The Alchemist", "Paulo Coelho", 299.0,
                              weight=350, shelf_location="A-12"))
    lib.add_book(EBook(2, "Clean Code", "Robert C. Martin", 499.0,
                       file_size_mb=8.5, format="PDF"))
    lib.add_book(AudioBook(3, "Atomic Habits", "James Clear", 399.0,
                           duration_minutes=332, narrator="James Clear"))
    lib.add_book(PhysicalBook(4, "1984", "George Orwell", 249.0,
                              weight=280, shelf_location="B-03"))
    lib.add_book(EBook(5, "Sapiens", "Yuval Noah Harari", 599.0,
                       file_size_mb=12.0, format="EPUB"))

    # Add members
    lib.add_member(Member(101, "Rahul Sharma", "rahul@email.com", "9876543210"))
    lib.add_member(StudentMember(102, "Priya Patel", "priya@email.com", "9123456780",
                                 student_id="STU2024001"))
    lib.add_member(PremiumMember(103, "Amit Kumar", "amit@email.com", "9988776655"))

    # Borrow
    lib.borrow_book(1, 101)
    lib.borrow_book(2, 102)
    lib.borrow_book(3, 103)

    # Test new features
    print(f"\n   {lib}")

    # Dunder methods
    print(f"\n   [Dunder] len(library) -> {len(lib)}")
    print(f"   [Dunder] 1 in library -> {1 in lib}")
    print(f"   [Dunder] 99 in library -> {99 in lib}")

    # Search
    print(f"\n   [Search] 'alchemist':")
    results = lib.search_books("alchemist")
    for b in results:
        print(f"     {b.get_info()}")

    print(f"\n   [Filter] EBooks only:")
    for b in lib.filter_by_type("ebook"):
        print(f"     {b.get_info()}")

    # Member report
    print(f"\n   [Member Report]:")
    print(lib.get_member_report(101))

    # Statistics
    lib.show_statistics()

    # Iteration
    print(f"\n   [Iteration] for book in library:")
    for book in lib:
        print(f"     {book}")

    print("\n[PASS] Complete library test finished!")
