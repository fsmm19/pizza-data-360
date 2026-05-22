import sqlite3

connection = sqlite3.connect("bronze/pos.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT,
  quantity INTEGER,
  unit_price REAL,
  date TEXT
)
""")

cursor.executemany(
    """
INSERT INTO ventas (sku, quantity, unit_price, date)
VALUES (?, ?, ?, ?)
""",
    [
        ("SKU-992-P", 5, 35000, "2026-05-13"),
        ("SKU-992-P", 3, 35000, "2026-05-13"),
        ("SKU-992-P", 2, 35000, "2026-05-14"),
    ],
)

connection.commit()
connection.close()
