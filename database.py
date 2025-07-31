import sqlite3
import random

DB_NAME = "yash_private_bank.db"

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                address TEXT,
                welcome_kit TEXT,
                account_number TEXT UNIQUE
            )
        """)
        conn.commit()

def generate_account_number():
    return str(random.randint(10**9, 10**10 - 1))  # 10-digit account number

def save_account(name, phone, address, welcome_kit):
    account_number = generate_account_number()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO accounts (name, phone, address, welcome_kit, account_number)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, address, welcome_kit, account_number))
        conn.commit()
    return account_number

def create_user(user_id, name, phone):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO accounts (id, name, phone)
            VALUES (?, ?, ?)
        """, (user_id, name, phone))
        conn.commit()

def user_exists(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE id = ?", (user_id,))
        return cursor.fetchone() is not None
