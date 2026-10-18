import sqlite3

def create_connection():
    """Helper function to create a database connection."""
    return sqlite3.connect("receipts.db")

def init_db():
    """Initializes the SQLite database table for receipts."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            date TEXT,
            total_amount REAL,
            tax REAL,
            items TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_receipt(vendor, date, total_amount, tax, items):
    """Saves parsed receipt data into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO receipts (vendor, date, total_amount, tax, items)
        VALUES (?, ?, ?, ?, ?)
    ''', (vendor, date, total_amount, tax, items))
    conn.commit()
    conn.close()

def fetch_all_receipts():
    """Retrieves all receipts from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vendor, date, total_amount, tax, items FROM receipts ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_all_receipts():
    """Deletes all records from the receipts table."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receipts")
    conn.commit()
    conn.close()

def delete_expense_by_id(expense_id):
    """Deletes a specific receipt record by its ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receipts WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()