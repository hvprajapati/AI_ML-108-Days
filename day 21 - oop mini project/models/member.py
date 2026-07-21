"""
Day 26 - Member Inheritance Hierarchy
Concepts: Inheritance, super(), Method Overriding, Polymorphism, Class Variables

Member (Base/Parent Class)
 |-- StudentMember   (discounted fee, max 3 books, requires student_id)
 |-- PremiumMember   (higher fee, max 10 books, priority access)

Key OOP Idea:
    Both are Members, but with DIFFERENT borrowing rules and fees.
    Method overriding lets each subclass define its OWN behavior.
"""


# ==============================================================================
# BASE CLASS: Member
# ==============================================================================
class Member:
    """
    Base class for all library members.

    Attributes:
        member_id, name, email, phone, membership_fee, borrowed_books
    """

    MAX_BOOKS_ALLOWED = 3  # Default limit  --  subclasses can override

    def __init__(self, member_id: int, name: str, email: str, phone: str,
                 membership_fee: float = 500.0):
        self._member_id = member_id
        self._name = name
        self._email = email
        self._phone = None
        self.phone = phone              # uses setter for validation
        self._membership_fee = None
        self.membership_fee = membership_fee
        self._borrowed_books = []

    # ---- Properties -----------------------------------------------------------
    @property
    def member_id(self): return self._member_id

    @property
    def name(self): return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty!")
        self._name = value.strip()

    @property
    def email(self): return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError(f"Invalid email: '{value}' -- must contain '@'.")
        self._email = value

    @property
    def phone(self): return self._phone

    @phone.setter
    def phone(self, value):
        digits_only = value.replace("-", "").replace(" ", "")
        if not digits_only.isdigit() or len(digits_only) != 10:
            raise ValueError(f"Phone must be exactly 10 digits. Got: '{value}'")
        self._phone = digits_only

    @property
    def membership_fee(self): return self._membership_fee

    @membership_fee.setter
    def membership_fee(self, value):
        if value < 0:
            raise ValueError("Membership fee cannot be negative!")
        self._membership_fee = value

    @property
    def borrowed_books(self) -> list:
        """Return a COPY to protect the real list."""
        return self._borrowed_books.copy()

    @property
    def books_borrowed_count(self) -> int:
        return len(self._borrowed_books)

    # ---- Instance Methods (can be overridden) ---------------------------------
    def borrow_book(self, book_id: int):
        """
        Add a book. Subclasses can override to add their own rules.
        """
        if len(self._borrowed_books) >= self.MAX_BOOKS_ALLOWED:
            raise ValueError(
                f"{self._name} has reached the max limit "
                f"({self.MAX_BOOKS_ALLOWED} books)!"
            )
        self._borrowed_books.append(book_id)

    def return_book(self, book_id: int):
        if book_id not in self._borrowed_books:
            raise ValueError(f"Book ID {book_id} is not borrowed by {self._name}.")
        self._borrowed_books.remove(book_id)

    def can_borrow(self) -> bool:
        return len(self._borrowed_books) < self.MAX_BOOKS_ALLOWED

    def get_info(self) -> str:
        """Base get_info -- override in subclasses."""
        return (
            f"ID: {self._member_id} | {self._name} | "
            f"Email: {self._email} | Phone: {self._phone} | "
            f"Fee: Rs.{self._membership_fee:.2f} | "
            f"Books: {self.books_borrowed_count}/{self.MAX_BOOKS_ALLOWED}"
        )

    def get_membership_type(self) -> str:
        """Return the type of membership. Override in subclasses."""
        return "Regular"

    def __str__(self):
        return (f"[{self.get_membership_type()}] {self._name} "
                f"(ID: {self._member_id}) -- {self.books_borrowed_count} book(s)")

    def __repr__(self):
        return (f"Member(id={self._member_id}, name='{self._name}', "
                f"type='{self.get_membership_type()}')")


# ==============================================================================
# SUBCLASS 1: StudentMember
# ==============================================================================
class StudentMember(Member):
    """
    A student member with discounted fee and limited borrowing.

    Differences from Regular Member:
        - Lower fee (Rs.200 instead of Rs.500)
        - Must provide student_id for verification
        - Same MAX_BOOKS_ALLOWED = 3 (inherited)
    """

    MAX_BOOKS_ALLOWED = 3          # Same as parent, but explicit

    def __init__(self, member_id: int, name: str, email: str, phone: str,
                 student_id: str):
        """
        StudentMember constructor.

        Note: We do NOT pass membership_fee to super().
        Instead, we set a fixed discounted fee after calling super().
        """
        # Call parent with a default fee (will be overwritten)
        super().__init__(member_id, name, email, phone, membership_fee=200.0)
        self._student_id = student_id  # Student-specific attribute
        # Override the fee with student discount (using property to validate)
        self.membership_fee = 200.0

    @property
    def student_id(self) -> str:
        return self._student_id

    def get_info(self) -> str:
        """OVERRIDE: Add student ID to the info."""
        base_info = super().get_info()
        return f"{base_info} | Student ID: {self._student_id}"

    def get_membership_type(self) -> str:
        return "Student"

    def is_valid_student(self) -> bool:
        """
        Student-specific method: verify student ID format.
        Example: Student IDs must start with 'STU'.
        """
        return self._student_id.startswith("STU")


# ==============================================================================
# SUBCLASS 2: PremiumMember
# ==============================================================================
class PremiumMember(Member):
    """
    A premium member with higher fee but more benefits.

    Differences from Regular Member:
        - Higher fee (Rs.1500)
        - Higher book limit (MAX_BOOKS_ALLOWED = 10)
        - Has priority_service flag
    """

    MAX_BOOKS_ALLOWED = 10         # OVERRIDE: Premium members get 10 books!

    def __init__(self, member_id: int, name: str, email: str, phone: str,
                 priority_service: bool = True):
        super().__init__(member_id, name, email, phone, membership_fee=1500.0)
        self.priority_service = priority_service
        # Override fee
        self.membership_fee = 1500.0

    @property
    def priority_service(self):
        return self._priority_service

    @priority_service.setter
    def priority_service(self, value: bool):
        self._priority_service = value

    def get_info(self) -> str:
        """OVERRIDE: Add premium-specific details."""
        base_info = super().get_info()
        priority = "Yes" if self._priority_service else "No"
        return f"{base_info} | Priority: {priority}"

    def get_membership_type(self) -> str:
        return "Premium"

    def request_priority(self) -> str:
        """Premium-specific: request priority processing."""
        if self._priority_service:
            return f"[PRIORITY] {self._name} gets fast-tracked!"
        return f"[STANDARD] {self._name} is in the normal queue."


# ===== QUICK TEST ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 26 -- TESTING MEMBER INHERITANCE HIERARCHY")
    print("=" * 60)

    # Create one of each type
    regular = Member(101, "Rahul Sharma", "rahul@email.com", "9876543210")
    student = StudentMember(102, "Priya Patel", "priya@email.com", "9123456780",
                            student_id="STU2024001")
    premium = PremiumMember(103, "Amit Kumar", "amit@email.com", "9988776655",
                            priority_service=True)

    all_members = [regular, student, premium]

    # ---- POLYMORPHISM: same method, different output per type ----------------
    print("\n[POLYMORPHISM] One list, different get_info() outputs:")
    for member in all_members:
        print(f"   {member.get_info()}")

    # ---- Different MAX_BOOKS_ALLOWED ------------------------------------------
    print(f"\n[MAX BOOKS ALLOWED]:")
    print(f"   Regular member: {regular.MAX_BOOKS_ALLOWED}")
    print(f"   Student member: {student.MAX_BOOKS_ALLOWED}")
    print(f"   Premium member: {premium.MAX_BOOKS_ALLOWED}")   # OVERRIDDEN to 10!

    # ---- Test premium can borrow MORE books ----------------------------------
    print(f"\n[BORROWING] Premium member borrows 10 books:")
    for i in range(1, 11):
        premium.borrow_book(i)
    print(f"   {premium.get_info()}")

    try:
        premium.borrow_book(11)  # Should fail -- limit reached
    except ValueError as e:
        print(f"   [X] {e}")

    # ---- Premium-specific method ----------------------------------------------
    print(f"\n[PREMIUM-SPECIFIC]:")
    print(f"   {premium.request_priority()}")

    # ---- Student-specific method ----------------------------------------------
    print(f"\n[STUDENT-SPECIFIC]:")
    print(f"   is_valid_student() -> {student.is_valid_student()}")
    # Test with bad student ID
    bad_student = StudentMember(104, "Test User", "test@email.com", "9999999999",
                                student_id="XYZ001")
    print(f"   Bad student ID valid? -> {bad_student.is_valid_student()}")

    # ---- isinstance() ---------------------------------------------------------
    print(f"\n[isinstance() CHECKS]:")
    print(f"   student is StudentMember? {isinstance(student, StudentMember)}")
    print(f"   student is Member?       {isinstance(student, Member)}")        # True
    print(f"   premium is Member?       {isinstance(premium, Member)}")        # True
    print(f"   regular is PremiumMember? {isinstance(regular, PremiumMember)}") # False

    print("\n[PASS] Member inheritance test complete!")
