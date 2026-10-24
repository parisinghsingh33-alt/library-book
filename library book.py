import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("books.json")


class Book:
    def __init__(self, book_id, title, author, quantity=1, issued=0):
        self.book_id = str(book_id)
        self.title = title
        self.author = author
        self.quantity = int(quantity)
        self.issued = int(issued)

    @property
    def available(self):
        return self.quantity - self.issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "quantity": self.quantity,
            "issued": self.issued
        }


class Library:
    def __init__(self):
        self.books = {}
        self.load_data()

    def load_data(self):
        if not DATA_FILE.exists():
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                book = Book(**item)
                if (book.book_id in self.books
                        or book.quantity < 0
                        or book.issued < 0
                        or book.issued > book.quantity):
                    raise ValueError("Invalid book data")
                self.books[book.book_id] = book

        except (json.JSONDecodeError, TypeError, ValueError, KeyError):
            print("Warning: Could not load books.json. Starting empty.")

    def save_data(self):
        data = [book.to_dict() for book in self.books.values()]
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_book(self, book_id, title, author, quantity):
        book_id = str(book_id).strip()
        title = title.strip()
        author = author.strip()

        if not book_id or not title or not author:
            print("Book ID, title, and author are required.")
            return

        if book_id in self.books:
            print("Book ID already exists.")
            return

        if quantity < 1:
            print("Quantity must be at least 1.")
            return

        self.books[book_id] = Book(
            book_id, title, author, quantity
        )
        self.save_data()
        print("Book added successfully.")

    def search_books(self, keyword):
        keyword = keyword.strip().casefold()

        results = [
            book for book in self.books.values()
            if keyword in book.title.casefold()
            or keyword in book.author.casefold()
            or keyword in book.book_id.casefold()
        ]

        if not results:
            print("No matching books found.")
            return

        for book in results:
            self.display_book(book)

    @staticmethod
    def display_book(book):
        print(
            f"\nID: {book.book_id}\n"
            f"Title: {book.title}\n"
            f"Author: {book.author}\n"
            f"Total copies: {book.quantity}\n"
            f"Issued copies: {book.issued}\n"
            f"Available copies: {book.available}\n"
        )

    def issue_book(self, book_id):
        book = self.books.get(str(book_id).strip())

        if book is None:
            print("Book not found.")
        elif book.available <= 0:
            print("No copies available.")
        else:
            book.issued += 1
            self.save_data()
            print(f"Issued successfully: {book.title}")

    def return_book(self, book_id):
        book = self.books.get(str(book_id).strip())

        if book is None:
            print("Book not found.")
        elif book.issued <= 0:
            print("No copy of this book is currently issued.")
        else:
            book.issued -= 1
            self.save_data()
            print(f"Returned successfully: {book.title}")

    def show_all_books(self):
        if not self.books:
            print("Library is empty.")
            return

        for book in self.books.values():
            self.display_book(book)

    def show_report(self):
        total_titles = len(self.books)
        total_copies = sum(
            book.quantity for book in self.books.values()
        )
        issued_copies = sum(
            book.issued for book in self.books.values()
        )
        available_copies = total_copies - issued_copies

        print("\n--- Library Report ---")
        print("Different book titles:", total_titles)
        print("Total book copies:", total_copies)
        print("Issued copies:", issued_copies)
        print("Available copies:", available_copies)


def main():
    library = Library()

    while True:
        print("\n===== LIBRARY BOOK INVENTORY MANAGER =====")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display All Books")
        print("6. Inventory Report")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                book_id = input("Enter book ID: ")
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                quantity = int(input("Enter quantity: "))
                library.add_book(book_id, title, author, quantity)

            elif choice == "2":
                keyword = input("Enter title, author, or ID: ")
                library.search_books(keyword)

            elif choice == "3":
                book_id = input("Enter book ID to issue: ")
                library.issue_book(book_id)

            elif choice == "4":
                book_id = input("Enter book ID to return: ")
                library.return_book(book_id)

            elif choice == "5":
                library.show_all_books()

            elif choice == "6":
                library.show_report()

            elif choice == "7":
                print("Thank you for using the Library Manager!")
                break

            else:
                print("Invalid choice. Please enter 1 to 7.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

        except OSError as error:
            print("File operation failed:", error)


if __name__ == "__main__":
    main()