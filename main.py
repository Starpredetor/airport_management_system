from flask import Flask, render_template, request, url_for, session, redirect, jsonify
import bcrypt
from flask_session import Session
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from datetime import datetime, timedelta
import logging
import json


app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

app.logger.setLevel(logging.ERROR)

@app.route('/')
def index():
    if 'loggedin' in session:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM flights''')
            flights = c.fetchall()
            
            
            if session['role'] == 'PASSENGER':
                c.execute('''SELECT COUNT(*) FROM tickets WHERE p_id = ?''', (session['username'],))
                ticket_count = c.fetchone()[0]
                return render_template('passenger_dashboard/index.html', flights=flights, ticket_count=ticket_count)
            elif session['role'] == 'STAFF':
                return render_template('employee_dashboard/index.html', flights=flights)
            elif session['role'] == 'ADMIN':
                c.execute('''SELECT COUNT(*) FROM passengers''')
                total_users = c.fetchone()[0]
                c.execute('''SELECT COUNT(*) FROM flights''')
                active_flights = c.fetchone()[0]
                c.execute('''SELECT COUNT(*) FROM tickets''')
                total_bookings = c.fetchone()[0]
                c.execute('''SELECT SUM(price) FROM tickets''')
                total_revenue = c.fetchone()[0] or 0

                return render_template('admin_dashboard/index.html', 
                                    flights=flights,
                                    total_users=total_users,
                                    active_flights=active_flights,
                                    total_bookings=total_bookings,
                                    total_revenue=total_revenue)
            c.close()
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM passengers WHERE username = ?''', (username,))
            user = c.fetchone()
            c.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            session['loggedin'] = True
            session['username'] = user[1]
            session['role'] = 'PASSENGER'
            return redirect(url_for('index'))
        else:
            return render_template('passenger/login.html', error_message='Invalid username or password')
    if request.method == 'GET':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        else:
            return render_template('passenger/login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO passengers (username, password, name, phone, email) VALUES (?, ?, ?, ?, ?)''', 
                     (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), name, phone, email))
            conn.commit()
            c.close()
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('passenger/register.html')

@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM admin WHERE username = ?''', (username,))
            user = c.fetchone()
            c.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            session['loggedin'] = True
            session['username'] = user[1]
            session['role'] = 'ADMIN'
            return redirect(url_for('index'))
        else:
            return render_template('admin/login.html', message='Invalid username or password')
    if request.method == 'GET':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        else:
            return render_template('admin/login.html')

@app.route('/employee_login', methods=['GET','POST'])
def employee_login():
    if request.method == 'POST':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM employees WHERE username = ?''', (username,))
            user = c.fetchone()
            c.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            session['loggedin'] = True
            session['username'] = user[1]
            session['role'] = 'STAFF'
            return redirect(url_for('index'))
        else:
            return render_template('employee/login.html', message='Invalid username or password')
    if request.method == 'GET':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        else:
            return render_template('employee/login.html')

@app.route('/tickets')
def tickets():
    if 'loggedin' in session:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM tickets WHERE p_id = ?''', (session['username'],))
            tickets = c.fetchall()
            c.close()
        return render_template('passenger_dashboard/tickets.html', tickets=tickets)
    else:
        return redirect(url_for('login'))

@app.route('/flights')
def flights():
    if 'loggedin' in session:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM flights''')
            flights = c.fetchall()
            c.close()
        return render_template('passenger_dashboard/flights.html', flights=flights)
    else:
        return redirect(url_for('login'))

@app.route('/book_flight/<int:f_id>', methods=['GET','POST'])
def book_flight(f_id):
    if 'loggedin' in session:
        if request.method == 'POST':
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO tickets 
                         (p_id, f_id, price, class, seat, travel_date, passenger_name, passenger_age, passenger_gender) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (session['username'], f_id, request.form['price'], request.form['class'], 
                          request.form['seat'], request.form['travel_date'], request.form['passenger_name'],
                          request.form['passenger_age'], request.form['passenger_gender']))
                conn.commit()
                c.close()
            return redirect(url_for('tickets'))
        if request.method == 'GET':
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''SELECT * FROM flights WHERE f_id = ?''', (f_id,))
                flight = c.fetchone()
                c.close()
            today = datetime.now().strftime('%Y-%m-%d')
            max_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d') 
            return render_template('passenger_dashboard/book_flight.html', flight=flight, today=today, max_date=max_date)
    else:
        return redirect(url_for('login'))

@app.route('/add_flight', methods=['GET','POST'])
def add_flight():
    if 'loggedin' in session and session['role'] == 'STAFF':
        if request.method == 'POST':
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO flights (flight_number, flight_name, source, destination, departure, arrival, price) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                         (request.form['flight_number'], request.form['flight_name'], request.form['source'], 
                          request.form['destination'], request.form['departure'], request.form['arrival'], request.form['price']))
                conn.commit()
                c.close()
            return redirect(url_for('flights'))
        if request.method == 'GET':
            return render_template('employee_dashboard/add_flight.html')
    else:
        return redirect(url_for('login'))

@app.route('/delete_flight/<int:f_id>')
def delete_flight(f_id):
    if 'loggedin' in session and session['role'] == 'STAFF':
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''DELETE FROM flights WHERE f_id = ?''', (f_id,))
            conn.commit()
            c.close()
        return redirect(url_for('flights'))
    else:
        return redirect(url_for('login'))

@app.route('/backup_database')
def backup_database():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        from datetime import datetime
        import shutil
        import os
        
        if not os.path.exists('backups'):
            os.makedirs('backups')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tstamp = datetime.now()
        backup_file = f'backups/database_backup_{timestamp}.db'
        with open('configs.json', 'w') as f:
            json.dump({"system_health": {"last_database_backup": tstamp}}, f)
        
        try:
            shutil.copy2('database.db', backup_file)
            return jsonify({'status': 'success', 'message': f'Backup created successfully: {backup_file}', 'file': backup_file})
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Backup failed: {str(e)}'})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/list_backups')
def list_backups():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        import os
        if os.path.exists('backups'):
            backups = []
            for file in os.listdir('backups'):
                if file.endswith('.db'):
                    file_path = os.path.join('backups', file)
                    file_stat = os.stat(file_path)
                    backups.append({
                        'file': file,
                        'size': file_stat.st_size,
                        'created': datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            return jsonify({'status': 'success', 'backups': backups})
        return jsonify({'status': 'success', 'backups': []})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/restore_backup/<filename>')
def restore_backup(filename):
    if 'loggedin' in session and session['role'] == 'ADMIN':
        import os
        import shutil
        
        backup_file = os.path.join('backups', filename)
        if os.path.exists(backup_file):
            try:
                import sqlite3
                sqlite3.connect('database.db').close()
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pre_restore_backup = f'backups/pre_restore_backup_{timestamp}.db'
                shutil.copy2('database.db', pre_restore_backup)
                
                shutil.copy2(backup_file, 'database.db')
                return jsonify({'status': 'success', 'message': f'Database restored from {filename}'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Restore failed: {str(e)}'})
        return jsonify({'status': 'error', 'message': 'Backup file not found'})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/admin/users')
def list_users():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT 'PASSENGER' as role, id, username, name, email, phone 
                        FROM passengers''')
            passengers = c.fetchall()
            
            c.execute('''SELECT 'STAFF' as role, id, username, name, NULL as email, NULL as phone 
                        FROM employees''')
            employees = c.fetchall()
            
            c.execute('''SELECT 'ADMIN' as role, id, username, NULL as name, NULL as email, NULL as phone 
                        FROM admin''')
            admins = c.fetchall()
            
            users = passengers + employees + admins
            c.close()
            
        return jsonify({'status': 'success', 'users': users})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/admin/add_user', methods=['POST'])
def add_user():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        data = request.get_json()
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        
        try:
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                if role == 'PASSENGER':
                    c.execute('''INSERT INTO passengers (username, password, name, email, phone) 
                                VALUES (?, ?, ?, ?, ?)''', 
                             (username, hashed_password, name, email, phone))
                elif role == 'STAFF':
                    c.execute('''INSERT INTO employees (username, password, name) 
                                VALUES (?, ?, ?)''', 
                             (username, hashed_password, name))
                elif role == 'ADMIN':
                    c.execute('''INSERT INTO admin (username, password) 
                                VALUES (?, ?)''', 
                             (username, hashed_password))
                conn.commit()
                c.close()
                
            return jsonify({'status': 'success', 'message': f'{role} user added successfully'})
        except sqlite3.IntegrityError:
            return jsonify({'status': 'error', 'message': 'Username already exists'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        data = request.get_json()
        role = data.get('role')
        user_id = data.get('id')
        
        try:
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                if role == 'PASSENGER':
                    c.execute('DELETE FROM passengers WHERE id = ?', (user_id,))
                elif role == 'STAFF':
                    c.execute('DELETE FROM employees WHERE id = ?', (user_id,))
                elif role == 'ADMIN':
                    c.execute('SELECT COUNT(*) FROM admin')
                    admin_count = c.fetchone()[0]
                    if admin_count <= 1:
                        return jsonify({'status': 'error', 'message': 'Cannot delete the last admin user'})
                    c.execute('DELETE FROM admin WHERE id = ?', (user_id,))
                conn.commit()
                c.close()
                
            return jsonify({'status': 'success', 'message': f'{role} user deleted successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/admin/reset_password', methods=['POST'])
def reset_password():
    if 'loggedin' in session and session['role'] == 'ADMIN':
        data = request.get_json()
        role = data.get('role')
        user_id = data.get('id')
        new_password = data.get('password')
        
        try:
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                
                if role == 'PASSENGER':
                    c.execute('UPDATE passengers SET password = ? WHERE id = ?', (hashed_password, user_id))
                elif role == 'STAFF':
                    c.execute('UPDATE employees SET password = ? WHERE id = ?', (hashed_password, user_id))
                elif role == 'ADMIN':
                    c.execute('UPDATE admin SET password = ? WHERE id = ?', (hashed_password, user_id))
                conn.commit()
                c.close()
                
            return jsonify({'status': 'success', 'message': 'Password reset successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'Unauthorized access'})

@app.route('/edit_flight/<int:f_id>', methods=['POST'])
def edit_flight(f_id):
    if 'loggedin' not in session or session['role'] != 'STAFF':
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'})
    
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''UPDATE flights 
                        SET flight_number=?, flight_name=?, source=?, destination=?, 
                            departure=?, arrival=?, price=? 
                        WHERE f_id=?''', 
                     (data['flight_number'], data['flight_name'], data['source'], 
                      data['destination'], data['departure'], data['arrival'], 
                      data['price'], f_id))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Flight updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'loggedin' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first'})
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'})
    
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            
            if session['role'] == 'PASSENGER':
                if data['password']:  
                    c.execute('''UPDATE passengers 
                                SET name=?, phone=?, email=?, password=?
                                WHERE username=?''',
                             (data['name'], data['phone'], data['email'],
                              bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()),
                              session['username']))
                else:  
                    c.execute('''UPDATE passengers 
                                SET name=?, phone=?, email=?
                                WHERE username=?''',
                             (data['name'], data['phone'], data['email'],
                              session['username']))
            elif session['role'] == 'STAFF':
                if data['password']:
                    c.execute('''UPDATE employees 
                                SET name=?, password=?
                                WHERE username=?''',
                             (data['name'],
                              bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()),
                              session['username']))
                else:
                    c.execute('''UPDATE employees 
                                SET name=?
                                WHERE username=?''',
                             (data['name'], session['username']))
            elif session['role'] == 'ADMIN':
                if data['password']:
                    c.execute('''UPDATE admin 
                                SET password=?
                                WHERE username=?''',
                             (bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()),
                              session['username']))
            
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/admin/stats/<period>')
def admin_stats(period):
    if 'loggedin' not in session or session['role'] != 'ADMIN':
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            
            today = datetime.now()
            labels = []
            bookings = []
            revenue = []
            
            if period == 'daily':
                for i in range(6, -1, -1):
                    date = today - timedelta(days=i)
                    labels.append(date.strftime('%Y-%m-%d'))
                    
                    c.execute('''SELECT COUNT(*), COALESCE(SUM(price), 0) 
                                FROM tickets 
                                WHERE date(created_at) = date(?)''', 
                             (date.strftime('%Y-%m-%d'),))
                    count, total = c.fetchone()
                    bookings.append(count or 0)
                    revenue.append(float(total or 0))
                    
            elif period == 'weekly':
                for i in range(3, -1, -1):
                    start_date = today - timedelta(weeks=i)
                    end_date = start_date + timedelta(days=6)
                    labels.append(f'{start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
                    
                    c.execute('''SELECT COUNT(*), COALESCE(SUM(price), 0) 
                                FROM tickets 
                                WHERE date(created_at) BETWEEN date(?) AND date(?)''',
                             (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                    count, total = c.fetchone()
                    bookings.append(count or 0)
                    revenue.append(float(total or 0))
                    
            elif period == 'monthly':
                for i in range(5, -1, -1):
                    date = today.replace(day=1) - relativedelta(months=i)
                    labels.append(date.strftime('%B %Y'))
                    
                    c.execute('''SELECT COUNT(*), COALESCE(SUM(price), 0) 
                                FROM tickets 
                                WHERE strftime('%Y-%m', created_at) = ?''',
                             (date.strftime('%Y-%m'),))
                    count, total = c.fetchone()
                    bookings.append(count or 0)
                    revenue.append(float(total or 0))
            
            return jsonify({
                'status': 'success',
                'labels': labels,
                'bookings': bookings,
                'revenue': revenue
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_occupied_seats/<int:f_id>')
def get_occupied_seats(f_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT seat FROM tickets WHERE f_id = ?''', (f_id,))
        seats = [row[0] for row in c.fetchall()]
        conn.close()
        return jsonify({'status': 'success', 'seats': seats})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/flight_tracker')
def flight_tracker():
    return render_template('flight_tracker.html')

@app.route('/get_active_flights')
def get_active_flights():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        current_time = datetime.now()
        
        c.execute('''
            SELECT f_id, flight_number, flight_name, source, destination, departure, arrival, price 
            FROM flights 
            WHERE datetime(departure) <= datetime(?) 
            AND datetime(arrival) >= datetime(?)
        ''', (
            (current_time + timedelta(hours=12)).strftime('%Y-%m-%d %H:%M'),
            (current_time - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M')
        ))
        
        flights = c.fetchall()
        active_flights = []
        
        for flight in flights:
            try:
                departure_time = datetime.strptime(flight[5], '%Y-%m-%d %H:%M')
                arrival_time = datetime.strptime(flight[6], '%Y-%m-%d %H:%M')
                flight_duration = (arrival_time - departure_time).total_seconds()
                
                if current_time < departure_time:
                    progress = 0
                    status = 'Scheduled'
                elif current_time > arrival_time:
                    progress = 1
                    status = 'Landed'
                else:
                    elapsed = (current_time - departure_time).total_seconds()
                    progress = min(elapsed / flight_duration, 1)
                    status = 'In Air'
                    
                        progress = max(0, progress - 0.1)
                        status = 'Delayed'
                
                active_flights.append({
                    'flight_number': flight[1],
                    'flight_name': flight[2],
                    'source': flight[3],
                    'destination': flight[4],
                    'departure': flight[5],
                    'arrival': flight[6],
                    'progress': progress,
                    'status': status
                })
            except (ValueError, TypeError) as e:
                app.logger.error(f"Error processing flight {flight[1]}: {str(e)}")
                continue
        
        conn.close()
        return jsonify(active_flights)
    except Exception as e:
        app.logger.error(f"Error in get_active_flights: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)