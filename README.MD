# Project & Task Management API

A simple **Project and Task Management System** built with **Django REST Framework**.  
This application allows users to create projects, assign tasks, manage task statuses, and track ownership.

---

## Features

- User registration & authentication (JWT-based).
- Create and manage **projects**.
- Create and assign **tasks** within projects.
- Task filtering and ordering (by status, priority, due date).
- Email notification task stub (Celery + Redis ready).
- Permissions: 
  - Only project owners can manage their projects.
  - Tasks can only be viewed/modified if they belong to the user’s projects.
  - Tasks can be seen if assigned to the user.

---

## Tech Stack

- **Backend**: Django 5 + Django REST Framework
- **Database**: PostgreSQL (or SQLite for local testing)
- **Authentication**: JWT (via `djangorestframework-simplejwt`)
- **Task Queue (Optional)**: Celery + Redis
- **Testing**: Postman 

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/taskproject.git
cd taskproject

2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py migrate

5. Create superuser
python manage.py createsuperuser

6. Run the server
python manage.py runserver


The API will be available at:

http://localhost:8000/api/

API Endpoints
Auth

POST /api/token/ → Get JWT token (login)

POST /api/token/refresh/ → Refresh JWT token

POST /api/users/register/ → Register new user

Projects

GET /api/projects/ → List user’s projects (owner or assigned tasks)

POST /api/projects/ → Create a new project

GET /api/projects/{id}/ → Retrieve project details

PUT /api/projects/{id}/ → Update project

DELETE /api/projects/{id}/ → Delete project

Tasks

GET /api/tasks/ → List tasks in user’s projects

POST /api/tasks/ → Create a new task

GET /api/tasks/{id}/ → Retrieve task details

PUT /api/tasks/{id}/ → Update task

DELETE /api/tasks/{id}/ → Delete task