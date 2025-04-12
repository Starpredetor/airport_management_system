import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create passengers table
    c.execute('''CREATE TABLE IF NOT EXISTS passengers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 name TEXT NOT NULL,
                 phone TEXT NOT NULL,
                 email TEXT NOT NULL)''')

    # Create admin table
    c.execute('''CREATE TABLE IF NOT EXISTS admin
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')

    # Create employees table
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 name TEXT NOT NULL)''')

    # Create flights table
    c.execute('''CREATE TABLE IF NOT EXISTS flights
                (f_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 flight_number TEXT NOT NULL,
                 flight_name TEXT NOT NULL,
                 source TEXT NOT NULL,
                 destination TEXT NOT NULL,
                 departure TEXT NOT NULL,
                 arrival TEXT NOT NULL,
                 price REAL NOT NULL)''')

    # Create tickets table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                (t_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 p_id TEXT NOT NULL,
                 f_id INTEGER NOT NULL,
                 price REAL NOT NULL,
                 class TEXT NOT NULL,
                 seat TEXT NOT NULL,
                 FOREIGN KEY (p_id) REFERENCES passengers (username),
                 FOREIGN KEY (f_id) REFERENCES flights (f_id))''')

    # Create default admin account
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute('''INSERT INTO admin (username, password) VALUES (?, ?)''', 
                 ('admin', admin_password))
    except sqlite3.IntegrityError:
        print("Admin account already exists")

    # Create sample employee account
    employee_password = bcrypt.hashpw('staff123'.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute('''INSERT INTO employees (username, password, name) VALUES (?, ?, ?)''',
                 ('staff', employee_password, 'John Staff'))
    except sqlite3.IntegrityError:
        print("Staff account already exists")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
