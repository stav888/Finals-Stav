import sqlite3
from typing import Optional, List, Dict


def initialize_database(db_path: str = "restaurant.db"):
    """Create tables and ensure the 'status' column exists."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS opening_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week TEXT NOT NULL UNIQUE,
                open_time TEXT NOT NULL,
                close_time TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
        """)

        conn.execute("""
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
        """)

        cursor = conn.execute("PRAGMA table_info(reservations)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'status' not in columns:
            conn.execute("ALTER TABLE reservations ADD COLUMN status TEXT NOT NULL DEFAULT 'confirmed'")
            print("✅ Added missing 'status' column to existing database.")


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
    """Get a specific reservation by ID."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
        ).fetchone()
        return dict(row) if row else None


def cancel_reservation(db_path: str, reservation_id: int) -> bool:
    """Cancel a reservation. Returns True if successfully updated."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ? AND status != 'cancelled'",
            (reservation_id,)
        )
        return cursor.rowcount > 0


def get_reservations(db_path: str, customer_name: str = None) -> List[Dict]:
    """Return confirmed reservations (optionally filtered by name)."""
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
