# JALA Student Skills App

A Django web application for managing student skills, built with Python and Django.

## Features

- Admin dashboard with live stats (total students, upcoming events, notifications, holidays)
- Student search and student list with photo, roll number, skills, and qualification
- Add/register new students with personal and parent/guardian information
- Public student registration form (self-service, pending admin approval)
- Parent portal to look up a child's report by name or roll number
- Feedback & complaints form for students, parents, and staff
- Admin-only login system
- Attendance, Events, Notifications, Holidays, Subjects, and Best Student modules
- Django admin panel for backend management
- Custom styling via CSS

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS
- **Image handling:** Pillow

## Project Structure

```
studentskills/
├── static/
│   └── css/
│       └── style.css
├── students/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── studentskills/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd studentskills
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If there's no `requirements.txt` yet, at minimum install:
   ```bash
   pip install django pillow
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin (superuser) account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open the app**
   Visit `http://127.0.0.1:8000/` in your browser.
   Visit `http://127.0.0.1:8000/admin/` to access the admin panel.

## Notes

- No credentials are hardcoded in the codebase. Admin login credentials are created locally via `createsuperuser` and stored (hashed) in the database — they are **not** included in this repository.
- Remember to add a `.gitignore` file to exclude `venv/`, `db.sqlite3`, and `__pycache__/` from version control.
