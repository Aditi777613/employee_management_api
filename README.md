# HabotConnect Employee Management API

A RESTful API for managing employees, built with Django and Django Rest Framework (DRF).

## Features
- **CRUD Operations**: Create, Read, Update, Delete employees.
- **Authentication**: Secure endpoints using JWT Authentication.
- **Filtering**: Filter employees by department and role.
- **Pagination**: Results paginated (10 per page).
- **Validation**: Data integrity checks (unique email, etc.).

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-filter
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### Authentication
Obtain a token to access protected endpoints.
- **POST** `/api/token/`
  - Body: `{"username": "your_user", "password": "your_password"}`
  - Response: `{"access": "...", "refresh": "..."}`
  - Note: You must create a user first (`python manage.py createsuperuser`).

### API Endpoints
All employee endpoints require `Authorization: Bearer <access_token>` header.

- **List Information**: `GET /api/employees/`
  - Filters: `?department=Engineering`, `?role=Manager`
  - Pagination: `?page=2`
- **Create Employee**: `POST /api/employees/`
- **Retrieve Employee**: `GET /api/employees/{id}/`
- **Update Employee**: `PUT/PATCH /api/employees/{id}/`
- **Delete Employee**: `DELETE /api/employees/{id}/`

## Testing
Run the automated test suite:
```bash
python manage.py test employees
```
