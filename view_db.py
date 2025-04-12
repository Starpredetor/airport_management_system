import sqlite3

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

if __name__ == '__main__':
    view_database()
