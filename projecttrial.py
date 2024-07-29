import sqlite3

conn = sqlite3.connect('expenses.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
''')

def add_expense(date, category, amount, description):
    c.execute('''
    INSERT INTO expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()

# Example usage
add_expense('2023-07-28', 'Food', 12.50, 'Lunch')
conn.close()


import pandas as pd

def upload_csv(file_path):
    data = pd.read_csv(file_path)
    data.to_sql('expenses', conn, if_exists='append', index=False)

# Example usage
upload_csv('bank_statement.csv')


def clean_data():
    df = pd.read_sql('SELECT * FROM expenses', conn)
    # Handle missing values, format dates, etc.
    df['date'] = pd.to_datetime(df['date'])
    # Further cleaning...
    df.to_sql('expenses_clean', conn, if_exists='replace', index=False)

# Example usage
clean_data()


import matplotlib.pyplot as plt

def plot_expenses():
    df = pd.read_sql('SELECT * FROM expenses_clean', conn)
    df.groupby('category')['amount'].sum().plot(kind='pie')
    plt.show()

# Example usage
plot_expenses()


import schedule
import time

def job():
    clean_data()
    plot_expenses()

schedule.every().month.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)



