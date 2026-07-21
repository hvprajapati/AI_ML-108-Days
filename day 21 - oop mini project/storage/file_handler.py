"""
Day 27 - File Handler (Persistence Layer)
Concepts: File I/O, JSON Serialization, Static Methods, Error Handling

This module handles saving and loading library data to/from JSON files.
Objects are serialized to dictionaries and deserialized back.

Why JSON? It's human-readable, language-independent, and Python's
json module makes it easy. The trade-off: custom objects need
manual conversion (to_dict / from_dict).
"""

import json
import os
from models.book import Book, PhysicalBook, EBook, AudioBook
from models.member import Member, StudentMember, PremiumMember


class FileHandler:
    """
    Handles saving and loading library data.

    Uses CLASS METHODS because we don't need multiple instances  -- 
    the file path is all the state we need, and we pass it as a parameter.

    STATIC METHODS are used for conversion functions that don't need
    access to class or instance state.
    """

    @staticmethod
    def book_to_dict(book: Book) -> dict:
        """
        Convert a Book (any subclass) to a dictionary for JSON storage.

        Uses isinstance() to determine the exact type and save
        type-specific attributes. This is a common pattern for
        polymorphic serialization.
        """
        data = {
            "type": book.get_type(),       # "Physical", "EBook", "AudioBook"
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "price": book.price,
            "is_borrowed": book.is_borrowed,
            "borrowed_by": book.borrowed_by,
        }

        # Add subclass-specific fields
        if isinstance(book, PhysicalBook):
            data["weight"] = book.weight
            data["shelf_location"] = book.shelf_location
        elif isinstance(book, EBook):
            data["file_size_mb"] = book.file_size_mb
            data["format"] = book.format
        elif isinstance(book, AudioBook):
            data["duration_minutes"] = book.duration_minutes
            data["narrator"] = book.narrator

        return data

    @staticmethod
    def dict_to_book(data: dict) -> Book:
        """
        Reconstruct a Book object from a dictionary.

        Reads the "type" field to determine which constructor to call.
        This is the DESERIALIZATION counterpart of book_to_dict().
        """
        book_type = data.get("type", "Generic Book")

        if book_type == "Physical":
            return PhysicalBook(
                book_id=data["book_id"],
                title=data["title"],
                author=data["author"],
                price=data["price"],
                weight=data.get("weight", 0),
                shelf_location=data.get("shelf_location", "Unknown"),
            )
        elif book_type == "EBook":
            return EBook(
                book_id=data["book_id"],
                title=data["title"],
                author=data["author"],
                price=data["price"],
                file_size_mb=data.get("file_size_mb", 0),
                format=data.get("format", "PDF"),
            )
        elif book_type == "AudioBook":
            return AudioBook(
                book_id=data["book_id"],
                title=data["title"],
                author=data["author"],
                price=data["price"],
                duration_minutes=data.get("duration_minutes", 0),
                narrator=data.get("narrator", "Unknown"),
            )
        else:
            # Fallback: create a generic Book (shouldn't happen normally)
            return Book(
                book_id=data["book_id"],
                title=data["title"],
                author=data["author"],
                price=data["price"],
            )

    @staticmethod
    def member_to_dict(member: Member) -> dict:
        """Convert a Member (any subclass) to a dictionary."""
        data = {
            "type": member.get_membership_type(),  # "Regular", "Student", "Premium"
            "member_id": member.member_id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "membership_fee": member.membership_fee,
            "borrowed_books": member.borrowed_books,  # already a list of ints
        }

        if isinstance(member, StudentMember):
            data["student_id"] = member.student_id
        elif isinstance(member, PremiumMember):
            data["priority_service"] = member.priority_service

        return data

    @staticmethod
    def dict_to_member(data: dict) -> Member:
        """Reconstruct a Member object from a dictionary."""
        member_type = data.get("type", "Regular")

        if member_type == "Student":
            member = StudentMember(
                member_id=data["member_id"],
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                student_id=data.get("student_id", "UNKNOWN"),
            )
        elif member_type == "Premium":
            member = PremiumMember(
                member_id=data["member_id"],
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                priority_service=data.get("priority_service", True),
            )
        else:
            member = Member(
                member_id=data["member_id"],
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                membership_fee=data.get("membership_fee", 500.0),
            )

        # Restore borrowed books
        for book_id in data.get("borrowed_books", []):
            member._borrowed_books.append(book_id)

        return member

    @classmethod
    def save_library(cls, library, filepath: str):
        """
        Save the entire library to a JSON file.

        Args:
            library:  The Library object to save.
            filepath: Path to the JSON file.

        The JSON structure:
        {
            "name": "Library Name",
            "books": [ {...}, {...}, ... ],
            "members": [ {...}, {...}, ... ]
        }
        """
        data = {
            "name": library.name,
            "books": [cls.book_to_dict(b) for b in library.books],
            "members": [cls.member_to_dict(m) for m in library.members],
        }

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_library(cls, library, filepath: str) -> bool:
        """
        Load library data from a JSON file.

        Args:
            library:  An EMPTY Library object to populate.
            filepath: Path to the JSON file.

        Returns:
            True if successful, False if file not found.
        """
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Set library name
            library.name = data.get("name", "My Library")

            # Reconstruct books
            for book_data in data.get("books", []):
                book = cls.dict_to_book(book_data)
                # Restore borrow state
                if book_data.get("is_borrowed"):
                    book._is_borrowed = True
                    book._borrowed_by = book_data.get("borrowed_by")
                library._books.append(book)

            # Reconstruct members
            for member_data in data.get("members", []):
                member = cls.dict_to_member(member_data)
                library._members.append(member)

            return True

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"  [X] Error loading data: {e}")
            return False


# ===== QUICK TEST ===============================================================
if __name__ == "__main__":
    from models.library import Library

    print("=" * 60)
    print("DAY 27 -- TESTING FILE HANDLER")
    print("=" * 60)

    # Create a test library
    lib = Library("Test Library")

    lib.add_book(PhysicalBook(1, "Test Book", "Author", 299.0,
                              weight=300, shelf_location="A-01"))
    lib.add_book(EBook(2, "Digital Book", "Author", 199.0,
                       file_size_mb=5.0, format="EPUB"))
    lib.add_book(AudioBook(3, "Audio Book", "Author", 399.0,
                           duration_minutes=180, narrator="Voice"))

    lib.add_member(Member(1, "User One", "one@email.com", "1111111111"))
    lib.add_member(StudentMember(2, "User Two", "two@email.com", "2222222222",
                                 student_id="STU001"))
    lib.add_member(PremiumMember(3, "User Three", "three@email.com", "3333333333"))

    # Borrow a book
    lib.borrow_book(1, 1)

    # Save
    print("\n[Saving library to test_library.json]")
    FileHandler.save_library(lib, "test_library.json")
    print("   Saved!")

    # Load into a NEW library
    print("\n[Loading into a NEW library object]")
    lib2 = Library("Empty")
    success = FileHandler.load_library(lib2, "test_library.json")

    if success:
        print(f"   Loaded: {lib2}")
        print(f"\n   Books:")
        lib2.list_all_books()
        print(f"\n   Members:")
        lib2.list_all_members()
        print(f"\n   Borrowed:")
        lib2.list_borrowed_books()

    # Cleanup
    if os.path.exists("test_library.json"):
        os.remove("test_library.json")
        print("\n[Cleaned up test file]")

    print("\n[PASS] File handler test complete!")
