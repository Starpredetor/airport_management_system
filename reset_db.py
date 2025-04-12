import sqlite3
import bcrypt
import os

def reset_database():
    # Remove existing database
    if os.path.exists('database.db'):
        os.remove('database.db')
    
    # Create new database connection
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS passengers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 name TEXT NOT NULL,
                 phone TEXT NOT NULL,
                 email TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 name TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS flights
                (f_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 flight_number TEXT NOT NULL,
                 flight_name TEXT NOT NULL,
                 source TEXT NOT NULL,
                 destination TEXT NOT NULL,
                 departure TEXT NOT NULL,
                 arrival TEXT NOT NULL,
                 price REAL NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                (t_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 p_id INTEGER NOT NULL,
                 f_id INTEGER NOT NULL,
                 price REAL NOT NULL,
                 class TEXT NOT NULL,
                 seat TEXT NOT NULL,
                 FOREIGN KEY(p_id) REFERENCES passengers(id),
                 FOREIGN KEY(f_id) REFERENCES flights(f_id))''')

    # Add default admin account
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
              ('admin', admin_password))

    # Add default staff account
    staff_password = bcrypt.hashpw('staff123'.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO employees (username, password, name) VALUES (?, ?, ?)",
              ('staff', staff_password, 'John Staff'))

    # Add demo passenger account
    passenger_password = bcrypt.hashpw('alen123'.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO passengers (username, password, name, phone, email) VALUES (?, ?, ?, ?, ?)",
              ('alen', passenger_password, 'Alen Walker', '1234567890', 'alen@example.com'))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database has been reset successfully!")

if __name__ == '__main__':
    reset_database()
