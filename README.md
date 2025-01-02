# User Authentication Project

This repository contains the **user_auth** project, a Django-based application designed to manage user authentication using custom user models. The project also includes support for login using either a username or email.

---

## Project Structure

### Key Files and Directories
- **user_auth/**: The root project directory containing global settings and configuration.
- **accounts/**: A Django app managing user-related functionalities, including custom authentication.
- **templates/**: HTML templates used for rendering frontend pages like login and signup.
- **db.sqlite3**: The SQLite database file used for development.

---

## Features
1. **Custom User Model**:
   - Defined using `AUTH_USER_MODEL` in `accounts.models.CustomUser`.
2. **Email or Username Authentication**:
   - Custom backend `accounts.authentication_backend.EmailOrUsernameBackend` allows users to log in using either their email or username.
3. **Secure Email Configuration**:
   - Configured with Gmail SMTP for sending emails.
4. **User-Friendly Login Errors**:
   - Displays contextual error messages for incorrect passwords, usernames, or email addresses.
5. **Responsive Templates**:
   - A modern login page styled with embedded CSS.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- Django 5.1.4

### Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd user_auth
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate   # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrate the database**:
   ```bash
   python manage.py migrate
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

---

## Configuration

### Email Settings
The project uses Gmail's SMTP server for sending emails. Update the following settings in `settings.py` with your credentials:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```


