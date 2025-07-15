"""
TaskFlow - A Jira Clone Application
Main Flask application file with routes and configuration
Compatible with Python 3.13 and latest Flask/SQLAlchemy
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and login manager
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Database Models
class User(UserMixin, db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by', backref='creator', lazy='dynamic')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        return self.username
    
    def get_task_count(self):
        return self.created_tasks.count()
    
    def get_assigned_task_count(self):
        return self.assigned_tasks.count()

class Task(db.Model):
    """Task model for task management"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='To Do')
    priority = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    
    # Foreign keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def get_status_color(self):
        status_colors = {
            'To Do': 'status-todo',
            'In Progress': 'status-progress', 
            'Done': 'status-done'
        }
        return status_colors.get(self.status, 'status-todo')
    
    def get_priority_color(self):
        priority_colors = {
            'Low': 'priority-low',
            'Medium': 'priority-medium',
            'High': 'priority-high',
            'Critical': 'priority-critical'
        }
        return priority_colors.get(self.priority, 'priority-medium')
    
    def get_assignee_name(self):
        if self.assignee:
            return self.assignee.username
        return 'Unassigned'
    
    def get_creator_name(self):
        return self.creator.username if self.creator else 'Unknown'
    
    def is_overdue(self):
        if self.due_date and self.status != 'Done':
            return datetime.utcnow() > self.due_date
        return False
    
    def get_time_since_created(self):
        time_diff = datetime.utcnow() - self.created_at
        
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            return f"{hours} hours ago"
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def index():
    """Home page - redirect based on user status"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'
        
        # Check if user already exists
        if db.session.scalar(db.select(User).filter_by(username=username)):
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        if db.session.scalar(db.select(User).filter_by(email=email)):
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.session.scalar(db.select(User).filter_by(email=email))
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on user role
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - shows user's tasks"""
    user_tasks = db.session.scalars(db.select(Task).filter_by(created_by=current_user.id)).all()
    assigned_tasks = db.session.scalars(db.select(Task).filter_by(assigned_to=current_user.id)).all()
    
    return render_template('dashboard.html', 
                         user_tasks=user_tasks, 
                         assigned_tasks=assigned_tasks)

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard - shows all tasks and users"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    all_tasks = db.session.scalars(db.select(Task)).all()
    all_users = db.session.scalars(db.select(User)).all()
    
    # Task statistics
    task_stats = {
        'total': len(all_tasks),
        'todo': len([t for t in all_tasks if t.status == 'To Do']),
        'in_progress': len([t for t in all_tasks if t.status == 'In Progress']),
        'done': len([t for t in all_tasks if t.status == 'Done'])
    }
    
    return render_template('admin_dashboard.html', 
                         tasks=all_tasks, 
                         users=all_users,
                         task_stats=task_stats)

@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        assignee_email = request.form.get('assignee_email')
        
        # Find assignee by email if provided
        assigned_to = None
        if assignee_email:
            assignee = db.session.scalar(db.select(User).filter_by(email=assignee_email))
            if assignee:
                assigned_to = assignee.id
            else:
                flash(f'No user found with email: {assignee_email}', 'error')
                return render_template('create_task.html')
        
        # Create new task
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status='To Do',
            created_by=current_user.id,
            assigned_to=assigned_to
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_task.html')

@app.route('/task/<int:task_id>')
@login_required
def view_task(task_id):
    """View task details"""
    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if user has permission to view this task
    if not current_user.is_admin and task.created_by != current_user.id and task.assigned_to != current_user.id:
        flash('Access denied. You can only view your own tasks.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('task_detail.html', task=task)

@app.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    """Update task status via AJAX"""
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'})
    
    # Check permissions
    if not current_user.is_admin and task.created_by != current_user.id and task.assigned_to != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'})
    
    new_status = request.json.get('status')
    if new_status in ['To Do', 'In Progress', 'Done']:
        task.status = new_status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid status'})

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit task details"""
    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check permissions
    if not current_user.is_admin and task.created_by != current_user.id:
        flash('Access denied. You can only edit tasks you created.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.updated_at = datetime.utcnow()
        
        # Update assignee if provided
        assignee_email = request.form.get('assignee_email')
        if assignee_email:
            assignee = db.session.scalar(db.select(User).filter_by(email=assignee_email))
            if assignee:
                task.assigned_to = assignee.id
            else:
                flash(f'No user found with email: {assignee_email}', 'error')
                return render_template('edit_task.html', task=task)
        else:
            task.assigned_to = None
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('view_task', task_id=task.id))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check permissions
    if not current_user.is_admin and task.created_by != current_user.id:
        flash('Access denied. You can only delete tasks you created.', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = db.session.scalar(db.select(User).filter_by(username='admin'))
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@taskflow.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
    
    app.run(debug=True)
