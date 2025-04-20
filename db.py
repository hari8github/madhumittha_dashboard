import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# Drop and recreate for demo purposes (remove this line in production)
cursor.execute("DROP TABLE IF EXISTS tickets")

# Create table
cursor.execute('''
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY,
        date TEXT,
        day TEXT,
        resolved_by TEXT,
        issue_type TEXT,
        routed_to_other_team INTEGER
    )
''')

# Dummy data
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
resolvers = ["Bot", "Engineer"]
issues = ["Login Issue", "VPN", "System Crash", "Printer", "Network", "Software Install"]

# Insert sample data
start_date = datetime.now() - timedelta(days=7)
for i in range(100):
    day = (start_date + timedelta(days=i % 5)).strftime('%A')
    date = (start_date + timedelta(days=i % 5)).strftime('%Y-%m-%d')
    resolved_by = random.choice(resolvers)
    issue = random.choice(issues)
    routed = random.choice([0, 0, 0, 1])  # 25% routed to other teams
    cursor.execute("INSERT INTO tickets (date, day, resolved_by, issue_type, routed_to_other_team) VALUES (?, ?, ?, ?, ?)",
                   (date, day, resolved_by, issue, routed))

conn.commit()
conn.close()
