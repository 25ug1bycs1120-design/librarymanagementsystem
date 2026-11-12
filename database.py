from contextlib import closing
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional


DATABASE_PATH = Path(__file__).resolve().parent / "library.db"


def initialize_database() -> None:
    """Create the database and books table if they do not already exist."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_title TEXT NOT NULL,
                    author_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    available_copies INTEGER NOT NULL
                )
                """
            )


def add_book(
    book_title: str, author_name: str, category: str, available_copies: int
) -> None:
    """Validate and save one book."""
    title = book_title.strip()
    author = author_name.strip()
    book_category = category.strip()

    if not title or not author or not book_category:
        raise ValueError("Title, author, and category are required.")
    if isinstance(available_copies, bool) or not isinstance(available_copies, int):
        raise ValueError("Available copies must be a whole number.")
    if available_copies < 0:
        raise ValueError("Available copies cannot be negative.")

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO books (book_title, author_name, category, available_copies)
                VALUES (?, ?, ?, ?)
                """,
                (title, author, book_category, available_copies),
            )


def get_all_books() -> List[Dict[str, object]]:
    """Return all books ordered by their ID."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            ORDER BY book_id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_total_available_copies() -> int:
    """Return the sum of all available copies."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        result = connection.execute(
            "SELECT COALESCE(SUM(available_copies), 0) FROM books"
        ).fetchone()
    return int(result[0])


def get_most_available_book() -> Optional[Dict[str, object]]:
    """Return the book with the most copies, or None when the library is empty."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            ORDER BY available_copies DESC, book_id
            LIMIT 1
            """
        ).fetchone()
    return dict(row) if row is not None else None


def get_category_summary() -> List[Dict[str, object]]:
    """Return each category's book-title count and total available copies."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT
                category,
                COUNT(*) AS book_titles,
                SUM(available_copies) AS available_copies
            FROM books
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()
    return [dict(row) for row in rows]
