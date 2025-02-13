from flask import Flask, render_template, request, url_for, session, redirect
import bcrypt
from flask_sessions import Session

import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False






@app.route('/')
def index():
    if 'loggedin' in session:
        role = session['role'] 
        print(session)
        if role == 'ADMIN':
            return render_template('admin_dashboard/index.html')
        elif role == 'STAFF':
            return render_template('employee_dashboard/index.html')
        elif role == 'PASSENGER':
            return render_template('passenger_dashboard/index.html')
        else:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM passengers WHERE username = ?''', (username,))
        user = c.fetchone()
        conn.close()
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
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO passengers (username, password, name, phone, email) VALUES (?, ?, ?, ?, ?)''', (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), name, phone, email))
        conn.commit()
        conn.close()
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
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM admin WHERE username = ?''', (username,))
        user = c.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            session['loggedin'] = True
            session['username'] = user[1]
            session['role'] = 'ADMIN'
            return redirect(url_for('index'))
        else:
            return render_template('admin_login.html', message='Invalid username or password')
    if request.method == 'GET':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        else:
            return render_template('admin_login.html')

@app.route('/employee_login', methods=['GET','POST'])
def employee_login():
    if request.method == 'POST':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM employees WHERE username = ?''', (username,))
        user = c.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            session['loggedin'] = True
            session['username'] = user[1]
            session['role'] = 'STAFF'
            return redirect(url_for('index'))
        else:
            return render_template('employee_login.html', message='Invalid username or password')
    if request.method == 'GET':
        if 'loggedin' in session:
            return redirect(url_for('index'))
        else:
            return render_template('employee_login.html')

@app.route('/tickets')
def tickets():
    if 'loggedin' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets WHERE p_id = ?''', (session['username'],))
        tickets = c.fetchall()
        conn.close()
        return render_template('passenger_dashboard/tickets.html', tickets=tickets)
    else:
        return redirect(url_for('login'))

@app.route('/flights')
def flights():
    if 'loggedin' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM flights''')
        flights = c.fetchall()
        conn.close()
        return render_template('passenger_dashboard/flights.html', flights=flights)
    else:
        return redirect(url_for('login'))

@app.route('/book_flight/<int:f_id>', methods=['GET','POST'])
def book_flight(f_id):
    if 'loggedin' in session:
        if request.method == 'POST':
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO tickets (p_id, f_id, price, class, seat) VALUES (?, ?, ?, ?, ?)''', (session['username'], f_id, request.form['price'], request.form['class'], request.form['seat']))
            conn.commit()
            conn.close()
            return redirect(url_for('tickets'))
        if request.method == 'GET':
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM flights WHERE f_id = ?''', (f_id,))
            flight = c.fetchone()
            conn.close()
            return render_template('passenger_dashboard/book_flight.html', flight=flight)
    else:
        return redirect(url_for('login'))
    
@app.route('/add_flight', methods=['GET','POST'])
def add_flight():
    if 'loggedin' in session and session['role'] == 'STAFF':
        if request.method == 'POST':
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO flights (flight_number, flight_name, source, destination, departure, arrival, price) VALUES (?, ?, ?, ?, ?, ?, ?)''', (request.form['flight_number'], request.form['flight_name'], request.form['source'], request.form['destination'], request.form['departure'], request.form['arrival'], request.form['price']))
            conn.commit()
            conn.close()
            return redirect(url_for('flights'))
        if request.method == 'GET':
            return render_template('employee_dashboard/add_flight.html')
    else:
        return redirect(url_for('login'))

@app.route('/delete_flight/<int:f_id>')
def delete_flight(f_id):
    if 'loggedin' in session and session['role'] == 'STAFF':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''DELETE FROM flights WHERE f_id = ?''', (f_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('flights'))
    else:
        return redirect(url_for('login'))
    



if __name__ == '__main__':
    app.run(debug=True)
