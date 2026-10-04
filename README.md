# Expense Tracker API

A backend Expense Tracker application built using **FastAPI, SQLAlchemy, SQLite, JWT Authentication, and Pydantic**.

The application allows users to securely register, log in, manage their own expenses, and view expense analytics.

## Features

### Authentication

* User registration
* User login
* Password hashing using Argon2
* JWT access token authentication
* Protected APIs
* Current-user authentication

### User APIs

* View my profile
* Update my profile
* Delete my account
* JWT-based user access

### Expense APIs

* Create an expense
* Get all my expenses
* Get a particular expense
* Update an expense
* Delete an expense
* Filter expenses by amount
* Expense summary
* Monthly expense analytics

### Security

* Passwords are never stored as plain text
* JWT authentication is used for protected endpoints
* Users can access only their own expenses
* Users cannot access another user's expenses by changing an ID
* Protected APIs return `401 Not Authenticated` without a valid JWT

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* Argon2
* Uvicorn

## Project Structure

```text
expense_tracker/
│
├── main.py
│
├── core/
│   ├── db.py
│   ├── security.py
│   ├── jwt_helper.py
│   └── dependencies.py
│
├── models/
│   ├── user_model.py
│   └── expense_model.py
│
├── schemas/
│   ├── api.py
│   ├── user.py
│   └── expense.py
│
└── routers/
    ├── auth_api.py
    ├── users_api.py
    └── expense_api.py
```

## API Endpoints

### Authentication

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| POST   | `/auth/register` | Register a new user   |
| POST   | `/auth/login`    | Login and receive JWT |

### User

| Method | Endpoint   | Description                     |
| ------ | ---------- | ------------------------------- |
| GET    | `/user/me` | Get logged-in user's profile    |
| PATCH  | `/user/me` | Update logged-in user's profile |
| DELETE | `/user/me` | Delete logged-in user's account |

### Expenses

| Method | Endpoint                      | Description                   |
| ------ | ----------------------------- | ----------------------------- |
| POST   | `/expenses/create_expense`    | Create an expense             |
| GET    | `/expenses/all`               | Get logged-in user's expenses |
| GET    | `/expenses/{expense_id}`      | Get a particular expense      |
| PATCH  | `/expenses/{expense_id}`      | Update an expense             |
| DELETE | `/expenses/{expense_id}`      | Delete an expense             |
| GET    | `/expenses/filter`            | Filter expenses               |
| GET    | `/expenses/summary`           | Get expense summary           |
| GET    | `/expenses/analytics/monthly` | Get monthly expense analytics |

## Authentication Flow

```text
Register
   ↓
Password is hashed
   ↓
User stored in database
   ↓
Login
   ↓
Username + Password verified
   ↓
JWT Access Token generated
   ↓
Client sends Bearer Token
   ↓
get_current_user()
   ↓
Protected API
```

## User Data Ownership

Each expense belongs to a user through `user_id`.

```text
User
 │
 ├── Expense 1
 ├── Expense 2
 └── Expense 3
```

When an authenticated user accesses expenses, the API filters data using the logged-in user's ID.

This prevents one user from accessing another user's expenses.

## Running the Project

Clone the repository and create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn expense_tracker.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Environment Variables

Create a `.env` file for sensitive configuration such as the JWT secret.

Do not commit `.env` to GitHub.

## Future Improvements

* PostgreSQL database
* Alembic database migrations
* Admin role and RBAC
* Pagination
* Expense categories
* Date-range filtering
* Automated tests using Pytest
* Docker
* Deployment
* Frontend dashboard
* Production environment configuration

## Author

Shreya Gavali

Computer Science Engineering Graduate

Python Backend Developer | FastAPI | SQLAlchemy | SQL

