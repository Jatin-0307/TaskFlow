# TaskFlow - Complete Jira Clone with Setup Guide

TaskFlow is a comprehensive Jira clone built with Python Flask backend, featuring:
- **Modern UI**: Clean white/blue theme with dark mode support
- **User Management**: Role-based access (Admin/User)
- **Task Management**: Create, assign, and track tasks
- **Email-based Assignment**: Assign tasks using email addresses
- **Admin Dashboard**: Complete oversight of all tasks and users
- **Status Tracking**: Real-time task status updates

## 🚀 Quick Start

### 1. Run the Application
Double-click `start_taskflow.bat` or run:
```bash
python app.py
```

### 2. Access the Application
Open your browser and go to: `http://localhost:5000`

### 3. Default Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@taskflow.com`

## 🔧 Installation (Manual)

If you need to set up from scratch:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 💡 Key Features

### User Features
- ✅ Create and manage personal tasks
- ✅ Assign tasks to team members via email
- ✅ Track task progress (To Do → In Progress → Done)
- ✅ Set task priorities (Low, Medium, High, Critical)
- ✅ View assigned tasks from other users
- ✅ Modern responsive interface

### Admin Features
- ✅ View all tasks in the system
- ✅ Monitor all users and their activity
- ✅ Comprehensive dashboard with statistics
- ✅ Task status overview across the organization
- ✅ User management capabilities

### Technical Features
- ✅ Clean, human-readable code structure
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Flask-Login for authentication
- ✅ Responsive design (mobile-friendly)
- ✅ Dark/Light theme toggle
- ✅ Form validation and error handling
- ✅ AJAX status updates

## 📱 User Interface

### Theme System
- **Light Theme**: Clean white background with blue accents
- **Dark Theme**: Dark background with blue highlights
- **Toggle**: Click the moon/sun icon in the navigation

### Dashboard Views
1. **User Dashboard**: Personal tasks and assignments
2. **Admin Dashboard**: System-wide overview
3. **Task Details**: Comprehensive task information
4. **Create/Edit**: User-friendly forms

## 🔐 User Management

### Registration
1. Go to the registration page
2. Fill in username, email, and password
3. Choose user type (Regular User or Administrator)
4. Submit to create account

### User Types
- **Regular User**: Create and manage own tasks, receive assignments
- **Administrator**: All user features + system-wide access

## 📋 Task Management

### Creating Tasks
1. Click "Create New Task" from any dashboard
2. Fill in required information:
   - **Title**: Clear, descriptive task name
   - **Description**: Detailed requirements
   - **Priority**: Low, Medium, High, or Critical
   - **Assignee**: Email of team member (optional)

### Task Workflow
```
To Do → In Progress → Done
```

### Task Assignment
- Assign tasks using team member's email address
- System validates that the email exists in the database
- Assigned users see tasks in their dashboard

## 🎯 Admin Features

### Admin Dashboard
- **Task Statistics**: Total, To Do, In Progress, Done
- **User Overview**: All registered users
- **Task Management**: View and edit all tasks
- **Search Functionality**: Find tasks and users quickly

### System Monitoring
- Track task distribution across users
- Monitor completion rates
- View user activity and task creation

## 📁 Project Structure

```
TaskFlow/
├── app.py                  # Main Flask application (includes models)
├── requirements.txt        # Python dependencies
├── start_taskflow.bat      # Windows startup script
├── install_dependencies.bat # Dependency installer
├── test_taskflow.py        # Compatibility test script
├── .env                   # Configuration file
├── static/
│   ├── css/
│   │   └── style.css      # Complete styling with themes
│   └── js/
│       └── main.js        # JavaScript functionality
└── templates/
    ├── base.html          # Base template with navigation
    ├── index.html         # Welcome page
    ├── login.html         # User login
    ├── register.html      # User registration
    ├── dashboard.html     # User dashboard
    ├── admin_dashboard.html # Admin overview
    ├── create_task.html   # Task creation form
    ├── edit_task.html     # Task editing form
    └── task_detail.html   # Task details view
```

## 🎨 Code Quality

### Design Principles
- **Clean Architecture**: Separation of concerns
- **Readable Code**: Well-commented and structured
- **Human-like**: Natural coding patterns
- **Best Practices**: Following Flask conventions

### Security Features
- Password hashing with Werkzeug
- Session management with Flask-Login
- Input validation and sanitization
- CSRF protection with Flask-WTF

## 🛠️ Customization

### Themes
- Modify CSS variables in `static/css/style.css`
- Add new color schemes
- Customize component styling

### Database
- SQLite by default (file-based)
- Easily switch to PostgreSQL or MySQL
- Models in `app.py` for easy customization

### Features
- Add new task fields in models
- Extend user roles and permissions
- Implement additional workflows

## 📱 Mobile Support

TaskFlow is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔍 Search and Filtering

### Admin Dashboard
- Search tasks by title, description, creator, or assignee
- Search users by username or email
- Real-time filtering as you type

### User Dashboard
- Filter tasks by status
- Sort by priority or creation date
- Quick status updates

## 📊 Statistics and Analytics

### Dashboard Metrics
- Total task count
- Status breakdown
- User activity
- Completion rates

### Progress Tracking
- Visual progress indicators
- Status change animations
- Time tracking (created/updated)

## 🔧 Troubleshooting

### Common Issues
1. **Database errors**: Delete `taskflow.db` and restart
2. **Port conflicts**: Change port in `app.py`
3. **Permission errors**: Run as administrator
4. **Package issues**: Reinstall requirements

### Development Mode
- Set `DEBUG=True` in `.env`
- Automatic reloading on code changes
- Detailed error messages

## 🎓 Educational Value

This project demonstrates:
- **Flask Web Development**: Routes, templates, forms
- **Database Design**: SQLAlchemy ORM, relationships
- **User Authentication**: Session management, security
- **Frontend Development**: HTML, CSS, JavaScript
- **Responsive Design**: Mobile-first approach
- **Project Architecture**: Clean code organization

## 📋 Assignment Presentation

When presenting to your teacher:

1. **Start with the welcome page** - show the clean design
2. **Register a new account** - demonstrate the process
3. **Create tasks** - show the form validation
4. **Assign tasks via email** - key requirement
5. **Switch to admin view** - show comprehensive dashboard
6. **Demonstrate theme toggle** - modern UI feature
7. **Explain the code structure** - clean, readable code

## 🎯 Key Requirements Met

✅ **Name**: TaskFlow  
✅ **Color Theme**: White and blue with night mode  
✅ **Readable Code**: Clean, well-commented Python  
✅ **Email Assignment**: Assign tasks by email address  
✅ **Admin Dashboard**: View all tasks and assignments  
✅ **Status Display**: Real-time task status tracking  

## Technology Stack

- **Backend**: Python Flask with SQLAlchemy 2.0
- **Database**: SQLite with modern ORM patterns
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Flask-Login with session management
- **Styling**: Custom CSS with CSS variables for theming
- **Icons**: FontAwesome for modern iconography

## 📞 Support

For any issues or questions:
1. Check this documentation
2. Review the code comments
3. Test with the default admin account
4. Verify all requirements are installed

---

**TaskFlow** - Modern Project Management Made Simple 🚀
