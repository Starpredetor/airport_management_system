import sqlite3
import bcrypt
import sys
from datetime import datetime, timedelta

DB_PATH = '../database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
                 travel_date DATE,
                 passenger_name TEXT,
                 passenger_age NUMBER,
                 passenger_gender TEXT,
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

    print("Database initialized successfully!")
    conn.commit()
    conn.close()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing flights
    c.execute("DELETE FROM flights")
    
    # Get current date
    current_date = datetime.now()
    
    # List of flights with realistic data
    flights = [
        # Domestic Flights - Morning
        ("AI-802", "Air India Express", "Mumbai", "Delhi", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 06:00"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 08:15"), 5200),
        
        ("6E-186", "IndiGo", "Bangalore", "Mumbai", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 07:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 09:15"), 4800),
        
        ("SG-401", "SpiceJet", "Delhi", "Chennai", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 08:45"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 11:30"), 6100),
        
        # Domestic Flights - Afternoon
        ("UK-835", "Vistara", "Hyderabad", "Kolkata", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 13:15"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 15:30"), 5500),
        
        ("AI-542", "Air India", "Chennai", "Mumbai", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 14:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 16:45"), 4900),
        
        # Domestic Flights - Evening
        ("6E-789", "IndiGo", "Delhi", "Bangalore", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 18:00"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 20:45"), 6300),
        
        ("SG-308", "SpiceJet", "Mumbai", "Kolkata", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 19:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 22:00"), 5800),
        
        # International Flights - Long Haul
        ("EK-501", "Emirates", "Mumbai", "Dubai", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 01:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 03:45"), 24500),
        
        ("QR-677", "Qatar Airways", "Delhi", "Doha", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 03:15"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 05:30"), 28900),
        
        ("SQ-423", "Singapore Airlines", "Bangalore", "Singapore", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 23:45"),
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 06:45"), 32100),
        
        ("BA-138", "British Airways", "Mumbai", "London", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 02:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 08:45"), 45600),
        
        ("LH-761", "Lufthansa", "Delhi", "Frankfurt", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 03:45"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 09:15"), 42300),
        
        # Return International Flights
        ("EK-502", "Emirates", "Dubai", "Mumbai", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 09:30"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 14:45"), 26800),
        
        ("QR-678", "Qatar Airways", "Doha", "Delhi", 
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 10:15"),
         (current_date + timedelta(days=1)).strftime("%Y-%m-%d 16:30"), 29200),
        
        # Next Day Domestic Flights
        ("AI-803", "Air India Express", "Delhi", "Mumbai", 
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 07:00"),
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 09:15"), 5400),
        
        ("6E-187", "IndiGo", "Mumbai", "Bangalore", 
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 08:30"),
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 10:15"), 4900),
        
        ("UK-836", "Vistara", "Kolkata", "Hyderabad", 
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 11:15"),
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 13:30"), 5600),
        
        ("SG-402", "SpiceJet", "Chennai", "Delhi", 
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 12:45"),
         (current_date + timedelta(days=2)).strftime("%Y-%m-%d 15:30"), 6200)
    ]
    
    # Insert flights
    c.executemany("""
        INSERT INTO flights 
        (flight_number, flight_name, source, destination, departure, arrival, price) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, flights)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f"Successfully inserted {len(flights)} flights!")

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Drop all tables
    c.execute("DROP TABLE IF EXISTS tickets")
    c.execute("DROP TABLE IF EXISTS flights")
    c.execute("DROP TABLE IF EXISTS employees")
    c.execute("DROP TABLE IF EXISTS admin")
    c.execute("DROP TABLE IF EXISTS passengers")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database reset successfully!")

def view_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get all table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    # Print contents of each table
    for table in tables:
        table_name = table[0]
        print(f"\n=== {table_name.upper()} TABLE ===")
        
        # Get column names
        c.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in c.fetchall()]
        print("Columns:", columns)
        
        # Get all rows
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        print("\nRows:")
        for row in rows:
            print(row)
            
    conn.close()

def main():
    commands = {
        'reset': reset_db,
        'init': init_db,
        'view': view_database
    }
    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command in commands:
            commands[command]()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: reset, init, view")
            sys.exit(1)

if __name__ == '__main__':
    main()
