from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import db, User, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # SQLite database path
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route now redirects to the login page if the user is not authenticated
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))  # Redirect to tasks page if logged in
    return redirect(url_for('login'))  # Otherwise, go to login page

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('tasks'))  # Redirect to tasks page after login
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful, please login')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Task management route
@app.route('/tasks', methods=['GET', 'POST'])
@login_required  # This ensures only authenticated users can access this route
def tasks():
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        if task_name:
            new_task = Task(task_name=task_name, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

# Route for deleting a task
@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks'))

# Route for marking a task as done/undone
@app.route('/mark_done/<int:task_id>')
@login_required
def mark_done(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.is_done = not task.is_done
        db.session.commit()
    return redirect(url_for('tasks'))

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))  # Redirect to login page after logout

# Ensure the database tables are created when the app starts
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the tables when the app starts
    app.run(host='0.0.0.0', port=10000)

