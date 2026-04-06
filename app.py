from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ticketdb"
)
cursor = db.cursor(dictionary=True)

# ---------------- LOGIN REQUIRED DECORATOR ----------------
def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if 'role' not in session:
                flash("Please login first.", "danger")
                return redirect(url_for('login'))

            if role and session['role'] != role:
                flash("Unauthorized access.", "danger")
                return redirect(url_for('login'))

            return fn(*args, **kwargs)
        return decorated
    return wrapper

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ---------------- REGISTER USER ----------------
@app.route('/register_user', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register_user'))

        hashed_password = generate_password_hash(password)

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Username already exists!", "danger")
            return redirect(url_for('register_user'))

        cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)",
                       (username, hashed_password))
        db.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template('register_user.html')

# ---------------- REGISTER ADMIN ----------------
@app.route('/register_admin', methods=['GET','POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register_admin'))

        hashed_password = generate_password_hash(password)

        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Admin username already exists!", "danger")
            return redirect(url_for('register_admin'))

        cursor.execute("INSERT INTO admin (username, password) VALUES (%s,%s)",
                       (username, hashed_password))
        db.commit()

        flash("Admin registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template('register_admin.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        table = "users" if role == "user" else "admin"

        cursor.execute(f"SELECT * FROM {table} WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['role'] = role
            session['user_id'] = user['id']
            return redirect(url_for('user_dashboard' if role=="user" else 'admin_dashboard'))

        flash("Invalid credentials!", "danger")

    return render_template('login.html')

# ---------------- USER DASHBOARD ----------------
@app.route('/user_dashboard')
@login_required(role='user')
def user_dashboard():
    return render_template('user_dashboard.html')

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():

    cursor.execute("SELECT COUNT(*) AS total FROM tickets")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS open FROM tickets WHERE status='Open'")
    open_count = cursor.fetchone()['open']

    cursor.execute("SELECT COUNT(*) AS progress FROM tickets WHERE status='In Progress'")
    progress_count = cursor.fetchone()['progress']

    cursor.execute("SELECT COUNT(*) AS closed FROM tickets WHERE status='Closed'")
    closed_count = cursor.fetchone()['closed']

    return render_template(
        'admin_dashboard.html',
        total=total,
        open_count=open_count,
        progress_count=progress_count,
        closed_count=closed_count
    )

# ---------------- CREATE TICKET ----------------
@app.route('/create_ticket', methods=['GET','POST'])
@login_required(role='user')
def create_ticket():
    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO tickets (title,description,priority,due_date,user_id,status)
            VALUES (%s,%s,%s,%s,%s,'Open')
        """,(
            request.form['title'],
            request.form['description'],
            request.form['priority'],
            request.form['due_date'],
            session['user_id']
        ))
        db.commit()
        flash("Ticket created successfully!", "success")
        return redirect(url_for('view_tickets'))

    return render_template('create_ticket.html')

# ---------------- VIEW / SEARCH / SORT ----------------
@app.route('/view_tickets')
@login_required()
def view_tickets():
    search = request.args.get('search')
    sort = request.args.get('sort')

    query = "SELECT * FROM tickets"
    params = []

    if session['role'] == 'user':
        query += " WHERE user_id=%s"
        params.append(session['user_id'])

    if search:
        query += " AND title LIKE %s" if params else " WHERE title LIKE %s"
        params.append(f"%{search}%")

    if sort == "due_date":
        query += " ORDER BY due_date ASC"

    cursor.execute(query, tuple(params))
    tickets = cursor.fetchall()

    return render_template('view_tickets.html', tickets=tickets)

# ---------------- EDIT TICKET ----------------
@app.route('/edit_ticket/<int:ticket_id>', methods=['GET','POST'])
@login_required()
def edit_ticket(ticket_id):

    cursor.execute("SELECT * FROM tickets WHERE id=%s",(ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        flash("Ticket not found!", "danger")
        return redirect(url_for('view_tickets'))

    if session['role'] == 'user' and ticket['user_id'] != session['user_id']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('view_tickets'))

    if request.method == 'POST':
        cursor.execute("""
            UPDATE tickets
            SET title=%s, description=%s, priority=%s, due_date=%s
            WHERE id=%s
        """,(
            request.form['title'],
            request.form['description'],
            request.form['priority'],
            request.form['due_date'],
            ticket_id
        ))
        db.commit()
        flash("Ticket updated successfully!", "success")
        return redirect(url_for('view_tickets'))

    return render_template('edit_ticket.html', ticket=ticket)

# ---------------- DELETE TICKET ----------------
@app.route('/delete_ticket/<int:ticket_id>')
@login_required()
def delete_ticket(ticket_id):

    cursor.execute("SELECT * FROM tickets WHERE id=%s",(ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        flash("Ticket not found!", "danger")
        return redirect(url_for('view_tickets'))

    if session['role'] == 'user' and ticket['user_id'] != session['user_id']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('view_tickets'))

    cursor.execute("DELETE FROM tickets WHERE id=%s",(ticket_id,))
    db.commit()

    flash("Ticket deleted successfully!", "warning")
    return redirect(url_for('view_tickets'))

# ---------------- UPDATE STATUS (ADMIN ONLY) ----------------
@app.route('/update_status/<int:ticket_id>/<string:new_status>')
@login_required(role='admin')
def update_status(ticket_id,new_status):
    cursor.execute("UPDATE tickets SET status=%s WHERE id=%s",
                   (new_status,ticket_id))
    db.commit()
    flash("Status updated!", "success")
    return redirect(url_for('view_tickets'))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)