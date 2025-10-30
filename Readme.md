# Doctor Feedback System

A Django web application for doctors to document patient outcomes and product feedback.

## Features

- Doctor authentication (signup/login)
- Patient management dashboard
- Track product effectiveness on diseases
- Upload before/after images
- Add progress updates

## Quick Start

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 13+

### 2. Installation

```bash
# Clone repository
git clone <repository-url>
cd doctor-feedback-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```sql
-- Run in PostgreSQL
CREATE DATABASE doctor_feedback_db;
CREATE USER doctor_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE doctor_feedback_db TO doctor_user;
```

### 4. Configure Environment

Create `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=doctor_feedback_db
DB_USER=doctor_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## Usage

1. **Sign Up** - Create doctor account with mobile number
2. **Login** - Use mobile number and password
3. **Add Patient** - Document patient data and product usage
4. **View Dashboard** - See all patient records
5. **Add Updates** - Track patient progress over time

## Project Structure

```
doctor-feedback-system/
├── doctor_feedback/     # Project settings
├── core/               # Main app (models, views, forms)
├── media/              # Uploaded images
├── static/             # CSS, JS files
├── manage.py
└── requirements.txt
```

## Technologies

- Django 4.2
- PostgreSQL
- Bootstrap 5
- Python 3.9+

## License

MIT
