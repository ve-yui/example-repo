import sqlite3


def connect_db():
    """Connect to the database."""
    return sqlite3.connect("ebookstore.db")


def create_tables():
    """Create tables and insert starter data."""

    with connect_db() as db:
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authorID INTEGER,
            qty INTEGER,
            FOREIGN KEY(authorID) REFERENCES author(id)
        )
        """)

        authors = [
            (1290, "Charles Dickens", "England"),
            (8937, "J.K. Rowling", "England"),
            (2356, "C.S. Lewis", "Ireland"),
            (6380, "J.R.R. Tolkien", "South Africa"),
            (5620, "Lewis Carroll", "England")
        ]

        books = [
            (3001, "A Tale of Two Cities", 1290, 30),
            (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
            (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
            (3004, "The Lord of the Rings", 6380, 37),
            (3005, "Alice's Adventures in Wonderland", 5620, 12)
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO author VALUES (?, ?, ?)",
            authors
        )

        cursor.executemany(
            "INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)",
            books
        )

        db.commit()


def enter_book():
    """Add a new book."""

    try:
        book_id = int(input("Enter Book ID: "))
        title = input("Enter Title: ")
        author_id = int(input("Enter Author ID: "))
        qty = int(input("Enter Quantity: "))

        with connect_db() as db:
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO book VALUES (?, ?, ?, ?)",
                (book_id, title, author_id, qty)
            )

            db.commit()

        print("Book added successfully.")

    except Exception as error:
        print("Error:", error)


def update_book():
    """Update book and author information."""

    try:
        book_id = input("Enter Book ID: ")

        if not (book_id.isdigit() and len(book_id) == 4):
            print("Book ID must be a 4-digit number.")
            return

        with connect_db() as db:
            cursor = db.cursor()

            cursor.execute("""
                SELECT book.id,
                        book.title,
                        book.authorID,
                        book.qty,
                        author.name,
                        author.country
                FROM book
                INNER JOIN author
                ON book.authorID = author.id
                WHERE book.id = ?
            """, (int(book_id),))

            result = cursor.fetchone()

            if not result:
                print("Book not found.")
                return

            print("\nCurrent Book Details")
            print(f"Title: {result[1]}")
            print(f"Author ID: {result[2]}")
            print(f"Quantity: {result[3]}")
            print(f"Author Name: {result[4]}")
            print(f"Author Country: {result[5]}")

            print("\nWhat would you like to update?")
            print("1. Quantity")
            print("2. Title")
            print("3. Author ID")
            print("4. Author Name")
            print("5. Author Country")

            choice = input("Enter option: ")

            if choice == "1":
                qty = int(input("Enter new quantity: "))

                cursor.execute(
                    "UPDATE book SET qty = ? WHERE id = ?",
                    (qty, int(book_id))
                )

            elif choice == "2":
                title = input("Enter new title: ")

                cursor.execute(
                    "UPDATE book SET title = ? WHERE id = ?",
                    (title, int(book_id))
                )

            elif choice == "3":
                author_id = input("Enter new Author ID: ")

                if not (author_id.isdigit() and len(author_id) == 4):
                    print("Author ID must be a 4-digit number.")
                    return

                cursor.execute(
                    "UPDATE book SET authorID = ? WHERE id = ?",
                    (int(author_id), int(book_id))
                )

            elif choice == "4":
                author_name = input("Enter new author name: ")

                cursor.execute(
                    "UPDATE author SET name = ? WHERE id = ?",
                    (author_name, result[2])
                )

            elif choice == "5":
                country = input("Enter new author country: ")

                cursor.execute(
                    "UPDATE author SET country = ? WHERE id = ?",
                    (country, result[2])
                )

            else:
                print("Invalid option.")
                return

            db.commit()

        print("Record updated successfully.")

    except Exception as error:
        print("Error:", error)


def delete_book():
    """Delete a book."""

    try:
        book_id = int(input("Enter Book ID: "))

        with connect_db() as db:
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM book WHERE id=?",
                (book_id,)
            )

            db.commit()

        print("Book deleted successfully.")

    except Exception as error:
        print("Error:", error)


def search_books():
    """Search for a book."""

    try:
        book_id = int(input("Enter Book ID: "))

        with connect_db() as db:
            cursor = db.cursor()

            cursor.execute(
                "SELECT * FROM book WHERE id=?",
                (book_id,)
            )

            result = cursor.fetchone()

            if result:
                print(result)
            else:
                print("Book not found.")

    except Exception as error:
        print("Error:", error)


def view_all_books():
    """Display book details using INNER JOIN,"""

    with connect_db() as db:
        cursor = db.cursor()

        cursor.execute("""
        SELECT book.title,
            author.name,
            author.country
        FROM book
        INNER JOIN author
        ON book.authorID = author.id
        """)

        results = cursor.fetchall()

        print("\nDetails")
        print("-" * 50)

        for title, name, country in results:
            print(f"\nTitle: {title}")
            print(f"Author Name: {name}")
            print(f"Author Country: {country}")
            print("-" * 50)


def main():
    """Main menu."""

    create_tables()

    while True:

        print("\nMenu")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            enter_book()

        elif choice == "2":
            update_book()

        elif choice == "3":
            delete_book()

        elif choice == "4":
            search_books()

        elif choice == "5":
            view_all_books()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
