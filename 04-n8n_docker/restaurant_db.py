import sqlite3
from typing import List, Dict, Optional


def initialize_database(db_path: str = "restaurant.db") -> None:
    """Create tables including reservations if they don't exist."""
    with sqlite3.connect(db_path) as conn:
        # Customers table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT
            )
            """
        )

        # Opening hours table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS opening_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT,
                opens TEXT,
                closes TEXT
            )
            """
        )

        # Reservations table (as required in Assignment 4)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date          TEXT NOT NULL,
                time          TEXT NOT NULL,
                party_size    INTEGER NOT NULL,
                contact       TEXT,
                status        TEXT NOT NULL DEFAULT 'confirmed',
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def book_reservation(
    db_path: str, 
    customer_name: str, 
    date: str, 
    time: str, 
    party_size: int, 
    contact: Optional[str] = None
) -> int:
    """Insert a new reservation and return its ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO reservations 
            (customer_name, date, time, party_size, contact) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (customer_name, date, time, party_size, contact)
        )
        return cursor.lastrowid


def cancel_reservation(db_path: str, reservation_id: int) -> bool:
    """Mark a reservation as cancelled (soft delete)."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ? AND status = 'confirmed'",
            (reservation_id,)
        )
        return cursor.rowcount > 0


def get_reservation_by_id(db_path: str, reservation_id: int) -> Optional[Dict]:
    """Return a reservation by ID."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM reservations WHERE id = ?",
            (reservation_id,)
        ).fetchone()
        return dict(row) if row else None


def get_reservations(db_path: str, customer_name: str = None) -> List[Dict]:
    """Return confirmed reservations (optional filter by name)."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if customer_name:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status='confirmed' AND customer_name LIKE ?",
                (f"%{customer_name}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status='confirmed'"
            ).fetchall()
        return [dict(r) for r in rows]