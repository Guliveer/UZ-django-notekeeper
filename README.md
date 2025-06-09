![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Django Badge](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=fff&style=for-the-badge)
![SQLite Badge](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=fff&style=for-the-badge)

# NoteKeeper

NoteKeeper is a simple web application for managing personal notes. Users can create, edit, and delete their own notes after registering and logging in. An admin user can view and manage all users' notes, including searching by username or note title.

## Features

- User registration and authentication
- Add, edit, and delete personal notes
- Admin panel for managing all notes (had to make something quick for admin to manage, so here it is)
- Search notes by username or title (admin only)
- User management (admin only)

## Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Guliveer/UZ-django-notekeeper.git
   cd UZ-django-notekeeper
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the app:**
   - User interface: [http://localhost:8000/](http://localhost:8000/)
   - Admin interface: [http://localhost:8000/admin/](http://localhost:8000/admin/)
