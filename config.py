import sqlite3
from datetime import datetime

def create_connection():
    connection = sqlite3.connect('db/face_recog.db')
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def initialize_tables():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Users

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
        )
    ''')

    # Attendance

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        time_of_entry TEXT,
        date TEXT,
        FOREIGN KEY (employee_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
    SELECT * FROM users
    ''')

    users = cursor.fetchall()

    if len(users) == 0:
        cursor.execute('''
    INSERT INTO users (id, name, age)
    VALUES (:id, :name, :age)
    ''', {'id': 1, 'name': 'Radee', 'age': 27})
    
    connection.commit()
    connection.close()

def attendance_exists(date: str):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT * FROM attendance a
    INNER JOIN users u
    ON u.id = a.employee_id
    WHERE date = :date
    ''', {'date': date})

    entry_exists = cursor.fetchall()

    connection.close()

    return len(entry_exists) > 1

def create_attendance(employee_id: int = 1):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    if not attendance_exists(current_date):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO attendance (employee_id, time_of_entry, date)
        VALUES (:employee, :time, :date)
        ''', {'employee': employee_id,'time': current_time, 'date': current_date})
        
        connection.commit()
        connection.close()

def get_attendance(filter: str = None):
    connection = create_connection()
    cursor = connection.cursor()

    if filter is None:
        cursor.execute('''
        SELECT u.name, a.time_of_entry, a.date FROM attendance a
        INNER JOIN users u
        ON u.id = a.employee_id
        ''')
    else:
        cursor.execute('''
        SELECT u.name, a.time_of_entry, a.date FROM attendance a
        INNER JOIN users u
        ON u.id = a.employee_id
        WHERE a.date LIKE :date
        ''', {'date': "%" + filter})

    attendance_entries = cursor.fetchall()

    connection.close()

    return attendance_entries