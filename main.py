
import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database_functions import make_new_user, get_all_todos_user, add_todo_user, complete_todo_user, delete_todo_user
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

def load_db():
    if not os.path.exists('database.json'):
        return {}
    with open('database.json', 'r') as f:
        try:
            return json.load(f)
        except:
            return {}

def save_db(data):
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=2)



@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = load_db()
    todos = get_all_todos_user(username, db)
    # Add id to each todo for template
    todos = [dict(id=i, **todo) for i, todo in enumerate(todos)]
    return render_template('home.html', todos=todos, username=username)
    


@app.route('/add_todo', methods=['POST'])
def add_todo_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    task = request.form.get('task')
    db = load_db()
    if task:
        _, db = add_todo_user(username, task, db)
        save_db(db)
    return redirect(url_for('home'))



@app.route('/complete_todo/<int:todo_id>', methods=['POST'])
def complete_todo_route(todo_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = load_db()
    _, db = complete_todo_user(username, todo_id, db)
    save_db(db)
    return redirect(url_for('home'))


@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo_route(todo_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = load_db()
    _, db = delete_todo_user(username, todo_id, db)
    save_db(db)
    return redirect(url_for('home'))


# --- Auth routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = load_db()
        if username in db and db[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        db = load_db()
        if not username or not password:
            flash('Please fill all fields', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif username in db:
            flash('Username already exists', 'danger')
        else:
            _, db = make_new_user(username, password, db)
            save_db(db)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__=="__main__":
    app.run(debug=True)