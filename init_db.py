import sqlite3
import bcrypt


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS admin''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (admin_id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''INSERT INTO admin (username, password) VALUES (?, ?)''',   ('admin', bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())))

    c.execute('''DROP TABLE IF EXISTS employees''')
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (emp_id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, designation TEXT)''')

    c.execute('''DROP TABLE IF EXISTS passengers''')
    c.execute('''CREATE TABLE IF NOT EXISTS passengers
                 (p_id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, phone TEXT, email TEXT)''')
    
    c.execute('''DROP TABLE IF EXISTS flights''')
    c.execute('''CREATE TABLE IF NOT EXISTS flights
                 (f_id INTEGER PRIMARY KEY, flight_number TEXT, flight_name TEXT, source TEXT, destination TEXT, departure TEXT, arrival TEXT, price INTEGER)''')
    
    c.execute('''DROP TABLE IF EXISTS baggage''')
    c.execute('''CREATE TABLE IF NOT EXISTS baggage
                 (b_id INTEGER PRIMARY KEY, p_id INTEGER, f_id INTEGER, weight INTEGER, FOREIGN KEY(p_id) REFERENCES passengers(p_id), FOREIGN KEY(f_id) REFERENCES flights(f_id)) ''')
    
    c.execute('''DROP TABLE IF EXISTS tickets''')
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (t_id INTEGER PRIMARY KEY, p_id INTEGER, f_id INTEGER, price INTEGER, class TEXT, seat TEXT, FOREIGN KEY(p_id) REFERENCES passengers(p_id), FOREIGN KEY(f_id) REFERENCES flights(f_id))''')
    
    

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('Database initialized.')
