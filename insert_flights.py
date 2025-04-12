import sqlite3
from datetime import datetime, timedelta

def insert_flights():
    conn = sqlite3.connect('database.db')
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

if __name__ == '__main__':
    insert_flights()
