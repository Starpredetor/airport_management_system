# Flight Booking System

A web-based flight booking system built with Flask that allows passengers to book flights, staff to manage flights, and admins to manage users.

## Features

- User Management:
  - Admin can manage users (add, delete, reset passwords)
  - Staff can manage flights
  - Passengers can book flights and manage their profiles

- Flight Management:
  - Search and filter flights
  - Visual seat selection with different classes
  - Dynamic pricing based on seat class
  - Real-time seat availability

- Dashboard:
  - Admin: User management and statistics
  - Staff: Flight management
  - Passenger: Booking history and profile

## Setup Instructions

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the application:
   - Open http://localhost:5000 in your browser
   - Default accounts:
     - Admin: username=admin, password=admin123
     - Staff: username=staff, password=staff123
     - Passenger: username=alen, password=alen123

## Project Structure

- `main.py`: Main application file
- `templates/`: HTML templates
  - `admin_dashboard/`: Admin interface
  - `passenger_dashboard/`: Passenger interface
  - `employee_dashboard/`: Staff interface
- `static/`: Static files (CSS, JS, images)
- `database.db`: SQLite database
