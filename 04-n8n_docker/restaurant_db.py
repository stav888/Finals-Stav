import sqlite3
from typing import Optional, List, Dict


def initialize_database(db_path: str = "restaurant.db"):
    """Create all required tables if they don't exist."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS opening_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week TEXT NOT NULL UNIQUE,
                open_time TEXT NOT NULL,
                close_time TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                party_size INTEGER NOT NULL,
                contact TEXT,
                status TEXT NOT NULL DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def book_reservation(
    db_path: str, customer_name: str, date: str,
    time: str, party_size: int, contact: str = None
) -> int:
    """Insert a new reservation and return its ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO reservations (customer_name, date, time, party_size, contact) "
            "VALUES (?, ?, ?, ?, ?)",
            (customer_name, date, time, party_size, contact)
        )
        return cursor.lastrowid


def get_reservation_by_id(db_path: str, reservation_id: int) -> Optional[Dict]:
    """Get a specific reservation by ID (Efficient: doesn't fetch all rows)."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
        ).fetchone()
        return dict(row) if row else None


def cancel_reservation(db_path: str, reservation_id: int) -> bool:
    """Mark a reservation as cancelled. Returns True if successfully updated."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ? AND status != 'cancelled'",
            (reservation_id,)
        )
        # rowcount > 0 means a row was actually found and updated
        return cursor.rowcount > 0 


def get_reservations(db_path: str, customer_name: str = None) -> List[Dict]:
    """Return confirmed reservations, optionally filtered by customer name."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if customer_name:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status='confirmed' "
                "AND customer_name LIKE ?", (f"%{customer_name}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status='confirmed'"
            ).fetchall()
        return [dict(r) for r in rows]