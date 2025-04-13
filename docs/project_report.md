# Flight Booking System - Technical Documentation

## Overview
The Flight Booking System is a web-based application built using Flask that provides a comprehensive platform for managing flight bookings, user accounts, and administrative tasks.

## Technical Stack
- **Backend Framework**: Flask 3.0.2
- **Database**: SQLite3
- **Authentication**: bcrypt 4.1.2
- **Session Management**: Flask-Session 0.7.0
- **Date Handling**: python-dateutil 2.9.0

## System Architecture

### User Roles
1. **Admin**
   - User management
   - System statistics
   - Database backup/restore
2. **Staff**
   - Flight management
   - Flight tracking
3. **Passengers**
   - Flight booking
   - Profile management
   - Ticket management

### Database Schema
1. **Passengers Table**
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - password
   - name
   - phone
   - email

2. **Admin Table**
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - password

3. **Employees Table**
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - password
   - name

## Key Features

### Authentication System
- Secure password hashing using bcrypt
- Session-based authentication
- Role-based access control

### Flight Management
- CRUD operations for flights
- Real-time seat tracking
- Dynamic pricing based on seat class

### Booking System
- Interactive seat selection
- Ticket generation
- Booking history

### Administration
- User management interface
- Database backup and restore
- Statistical analysis and reporting

## Security Features
- Password hashing
- Session management
- Input validation
- Error logging

## Project Structure
```
project/
├── try.py              # Main application file
├── init_db.py         # Database initialization
├── view_db.py         # Database viewer
├── templates/         # HTML templates
│   ├── admin_dashboard/
│   ├── employee_dashboard/
│   └── passenger_dashboard/
├── static/           # Static assets
└── database.db      # SQLite database
```

## Future Enhancements
1. Payment gateway integration
2. Email notifications
3. Mobile application
4. API documentation
5. Enhanced analytics
