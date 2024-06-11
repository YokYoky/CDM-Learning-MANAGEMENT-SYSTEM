**This project involves developing a comprehensive Learning Management System (LMS) for Colegio de Montalban using Python Django and PostgreSQL.**

# Features
* Admin: Create and manage user roles (Student or Instructor), courses (DSA), and program (BS Computer Engineering)
* Instructors: Create, manage, and deliver assignments, materials, and assessment
* Students: Access to course materials, assignment submissions, discussions, and progress tracking.

# Installation
**Clone the git repo:** `git clone https://github.com/YokYoky/CDM-Learning-MANAGEMENT-SYSTEM.git`

**Create virtual environment:** `python -m venv env`

Change directory to where the requirements.txt is located then install the requirements package `pip install -r requirements.txt` 
If it doesn't work and your OS is windows try `py pip install -r requirements.txt`

Setup the PostgreSQL database:
the required module is already installed earlier
``` SQL
psql -U postgres
CREATE DATABASE cdmlmsdtb;
CREATE USER cdmadmin WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE cdmlmsdtb TO cdmadmin;
\q
```

go to the settings.py and modify the DATABASES based from the database you created.
``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cdmlmsdtb',
        'USER': 'cdmadmin',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',  # Or the IP address where PostgreSQL is running
        'PORT': '5432',        # Default PostgreSQL port
    }
}
```

Migrate the models
``` python
python manage.py makemigrations
python manage.py migrate
```
Create django superuser
``` python
python manage.py createsuperuser
```
use those admin credentials to login in /admin

Run the app
``` python
python manage.py runserver
```
