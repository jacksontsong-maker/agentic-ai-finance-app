<<<<<<< HEAD
import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def add_expense_db(amount, category):
    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (?, ?)",
        (amount, category)
    )
    conn.commit()
    return f"Added ${amount} for {category}"

def get_total_spent():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    return total

def get_summary_db():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        GROUP BY category 
        ORDER BY SUM(amount) DESC
    """)
    breakdown = cursor.fetchall()

    summary = f"Total spent: ${total}\n"
    for cat, amt in breakdown:
        summary += f"- {cat}: ${amt}\n"

    return summary

def get_detailed_summary():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    breakdown = cursor.fetchall()

    result = {
        "total": total,
        "categories": []
    }

    for cat, amt in breakdown:
        result["categories"].append({
            "category": cat,
            "amount": amt,
            "percentage": (amt / total * 100) if total > 0 else 0
        })

    return result

def get_daily_spending():
    cursor.execute("""
        SELECT DATE(date), SUM(amount)
        FROM expenses
        GROUP BY DATE(date)
        ORDER BY DATE(date)
    """)
=======
import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def add_expense_db(amount, category):
    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (?, ?)",
        (amount, category)
    )
    conn.commit()
    return f"Added ${amount} for {category}"

def get_total_spent():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    return total

def get_summary_db():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        GROUP BY category 
        ORDER BY SUM(amount) DESC
    """)
    breakdown = cursor.fetchall()

    summary = f"Total spent: ${total}\n"
    for cat, amt in breakdown:
        summary += f"- {cat}: ${amt}\n"

    return summary

def get_detailed_summary():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    breakdown = cursor.fetchall()

    result = {
        "total": total,
        "categories": []
    }

    for cat, amt in breakdown:
        result["categories"].append({
            "category": cat,
            "amount": amt,
            "percentage": (amt / total * 100) if total > 0 else 0
        })

    return result

def get_daily_spending():
    cursor.execute("""
        SELECT DATE(date), SUM(amount)
        FROM expenses
        GROUP BY DATE(date)
        ORDER BY DATE(date)
    """)
>>>>>>> 607f0b4deaa6c389191f7aeefff0ad3c62548222
    return cursor.fetchall()