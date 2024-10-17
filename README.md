# To-Do List Application

A simple web-based To-Do application built using Flask, Python, and SQLite. The app allows users to register, log in, and manage their tasks by adding, removing, or marking tasks as done.

## Features
- User registration and authentication
- Create, delete, and manage to-do tasks
- Task completion tracking (mark tasks as done/undone)
- Session-based login with user-specific task lists

### Project Structure

```bash
todo_app/
|
├── static/
│   └── styles.css        # CSS styling
│
├── templates/
│   ├── layout.html       # Base layout for all pages
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── tasks.html        # To-do list page
│
├── app.py                # Main Flask application
├── forms.py              # Form definitions for login/registration
├── models.py             # Database models for users and tasks
├── requirements.txt      # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.x installed
- Flask and dependencies (install via `pip`)

### Installation

1. Clone this repository:
   ```bash
   git clone <todo_app-repo-link>
   cd todo_app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/` to access the app.


