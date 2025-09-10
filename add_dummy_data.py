import sqlite3

# Connect to the database
conn = sqlite3.connect('transactions.db')
c = conn.cursor()

# Insert some "Not Fraud" records manually
dummy_data = [
    (10, 5, 4, 2025, 1200.0, 'user111', 'Not Fraud'),
    (14, 12, 3, 2024, 850.0, 'user112', 'Not Fraud'),
    (18, 7, 2, 2025, 300.0, 'user113', 'Not Fraud'),
    (9, 23, 1, 2023, 1500.0, 'user114', 'Not Fraud'),
    (16, 19, 12, 2024, 500.0, 'user115', 'Not Fraud')
]

for row in dummy_data:
    c.execute("INSERT INTO transactions (trans_hour, trans_day, trans_month,"
              "trans_year, trans_amount, upi_number, prediction) VALUES (?, ?,"
              "?, ?, ?, ?, ?)", row)

conn.commit()
conn.close()

print("Dummy Not Fraud data added successfully.")