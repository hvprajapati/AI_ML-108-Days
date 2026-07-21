"""
Day 26 - Book Inheritance Hierarchy
Concepts: Inheritance, super(), Method Overriding, Polymorphism, isinstance()

Book (Base/Parent Class)
 |-- PhysicalBook   (adds: weight, shelf_location)
 |-- EBook           (adds: file_size_mb, format)
 |-- AudioBook       (adds: duration_minutes, narrator)

Key OOP Idea:
    All three subclasses ARE Books (IS-A relationship).
    Each subclass EXTENDS the base with its own unique attributes,
    but shares the common interface (borrow, return, get_info).
"""


# ==============================================================================
# BASE CLASS: Book
# ==============================================================================
class Book:
    """
    Base class for all book types in the library.

    Attributes common to ALL books:
        book_id, title, author, price, is_borrowed, borrowed_by
    """

    def __init__(self, book_id: int, title: str, author: str, price: float):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._price = None
        self.price = price           # uses setter for validation
        self._is_borrowed = False
        self._borrowed_by = None

    # ---- Properties (same as Day 25) -----------------------------------------
    @property
    def book_id(self): return self._book_id

    @property
    def title(self): return self._title

    @property
    def author(self): return self._author

    @property
    def price(self): return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError(f"Price cannot be negative! Got: Rs.{value}")
        self._price = value

    @property
    def is_borrowed(self): return self._is_borrowed

    @property
    def borrowed_by(self): return self._borrowed_by

    # ---- Instance Methods (shared by ALL subclasses) -------------------------
    def borrow(self, member_id: int):
        if self._is_borrowed:
            raise ValueError(
                f"'{self._title}' is already borrowed by member {self._borrowed_by}."
            )
        self._is_borrowed = True
        self._borrowed_by = member_id

    def return_book(self):
        if not self._is_borrowed:
            return
        self._is_borrowed = False
        self._borrowed_by = None

    def get_info(self) -> str:
        """
        Base get_info() -- meant to be OVERRIDDEN by subclasses.
        Subclasses call this via super() and add their own details.
        """
        status = "Borrowed" if self._is_borrowed else "Available"
        return (
            f"ID: {self._book_id} | '{self._title}' by {self._author} | "
            f"Rs.{self._price:.2f} | {status}"
        )

    def get_type(self) -> str:
        """Return the type of book. Override in subclasses."""
        return "Generic Book"

    def __str__(self):
        status = "Available" if not self._is_borrowed else "Borrowed"
        return f"[{self.get_type()}] '{self._title}' by {self._author} -- {status}"

    def __repr__(self):
        return (f"Book(id={self._book_id}, title='{self._title}', "
                f"author='{self._author}')")


# ==============================================================================
# SUBCLASS 1: PhysicalBook
# ==============================================================================
class PhysicalBook(Book):
    """
    A physical/printed book.

    Inherits everything from Book and adds:
        - weight (float): Weight in grams.
        - shelf_location (str): Where the book is kept in the library.

    super().__init__() calls the PARENT constructor to set up common attributes.
    """

    def __init__(self, book_id: int, title: str, author: str, price: float,
                 weight: float, shelf_location: str):
        # Call the PARENT constructor to initialize common attributes
        super().__init__(book_id, title, author, price)
        # Now initialize PhysicalBook-specific attributes
        self.weight = weight
        self.shelf_location = shelf_location

    def get_info(self) -> str:
        """
        OVERRIDE the parent's get_info() to add physical book details.
        Uses super().get_info() to reuse the parent's logic (DRY principle).
        """
        base_info = super().get_info()  # Reuse parent's code
        return f"{base_info} | Weight: {self.weight}g | Shelf: {self.shelf_location}"

    def get_type(self) -> str:
        return "Physical"

    def is_heavy(self) -> bool:
        """PhysicalBook-specific method: check if the book is heavy."""
        return self.weight > 500


# ==============================================================================
# SUBCLASS 2: EBook
# ==============================================================================
class EBook(Book):
    """
    An electronic/digital book.

    Adds:
        - file_size_mb (float): File size in megabytes.
        - format (str): File format (pdf, epub, mobi, etc.).
    """

    def __init__(self, book_id: int, title: str, author: str, price: float,
                 file_size_mb: float, format: str = "PDF"):
        super().__init__(book_id, title, author, price)
        self.file_size_mb = file_size_mb
        self.format = format

    def get_info(self) -> str:
        """OVERRIDE: Add digital-specific details."""
        base_info = super().get_info()
        return f"{base_info} | Size: {self.file_size_mb}MB | Format: {self.format}"

    def get_type(self) -> str:
        return "EBook"

    def is_downloadable(self) -> bool:
        """EBook-specific method: check file size is reasonable."""
        return self.file_size_mb <= 50  # 50MB limit


# ==============================================================================
# SUBCLASS 3: AudioBook
# ==============================================================================
class AudioBook(Book):
    """
    An audiobook.

    Adds:
        - duration_minutes (int): Length in minutes.
        - narrator (str): Name of the voice narrator.
    """

    def __init__(self, book_id: int, title: str, author: str, price: float,
                 duration_minutes: int, narrator: str):
        super().__init__(book_id, title, author, price)
        self.duration_minutes = duration_minutes
        self.narrator = narrator

    def get_info(self) -> str:
        """OVERRIDE: Add audio-specific details."""
        base_info = super().get_info()
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        return (f"{base_info} | Duration: {hours}h {minutes}m | "
                f"Narrator: {self.narrator}")

    def get_type(self) -> str:
        return "AudioBook"

    def get_duration_hours(self) -> float:
        """AudioBook-specific: return duration in hours."""
        return self.duration_minutes / 60


# ===== QUICK TEST ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 26 -- TESTING BOOK INHERITANCE HIERARCHY")
    print("=" * 60)

    # Create one of each type
    physical = PhysicalBook(1, "The Alchemist", "Paulo Coelho", 299.0,
                            weight=350, shelf_location="A-12")
    ebook = EBook(2, "Clean Code", "Robert C. Martin", 499.0,
                  file_size_mb=8.5, format="PDF")
    audiobook = AudioBook(3, "Atomic Habits", "James Clear", 399.0,
                          duration_minutes=332, narrator="James Clear")

    # ---- POLYMORPHISM: Store different types in ONE list --------------------
    all_books = [physical, ebook, audiobook]

    print("\n[POLYMORPHISM] One list, different types:")
    for book in all_books:
        # Same method call (get_info) but DIFFERENT behavior per subclass!
        print(f"   {book.get_info()}")
        print(f"     -> type = {type(book).__name__}, get_type() = '{book.get_type()}'")

    # ---- isinstance() checks -------------------------------------------------
    print(f"\n[isinstance() CHECKS]:")
    print(f"   physical is PhysicalBook? {isinstance(physical, PhysicalBook)}")
    print(f"   physical is Book?         {isinstance(physical, Book)}")        # True! (inheritance)
    print(f"   physical is EBook?        {isinstance(physical, EBook)}")       # False
    print(f"   ebook is Book?            {isinstance(ebook, Book)}")           # True!
    print(f"   audiobook is object?      {isinstance(audiobook, object)}")     # Everything is an object!

    # ---- Subclass-specific methods -------------------------------------------
    print(f"\n[SUBCLASS-SPECIFIC METHODS]:")
    print(f"   PhysicalBook.is_heavy()        -> {physical.is_heavy()}")
    print(f"   EBook.is_downloadable()         -> {ebook.is_downloadable()}")
    print(f"   AudioBook.get_duration_hours()  -> {audiobook.get_duration_hours():.1f}h")

    # ---- Borrow/Return still works (inherited from Book) --------------------
    print(f"\n[INHERITED BEHAVIOR]:")
    physical.borrow(101)
    ebook.borrow(102)
    print(f"   {physical}")
    print(f"   {ebook}")

    print("\n[PASS] Book inheritance test complete!")
