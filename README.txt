# Task Management API with JWT Authentication

## Features
- JWT-based login/logout system
- Role-based access (Admin / Manager / User)
- Full CRUD operations
- Automated user deactivation after 5 missed deadlines
- Admin panel integration


##Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create admin user:
```bash
python manage.py createsuperuser
```

4. Start development server:
```bash
python manage.py runserver
```
This project includes a custom Django management command 
to deactivate users who have missed 5 or more tasks
python manage.py check_missed_deadlines

## API Endpoints

| Endpoint        | Method | Description                | Access Level                              |
| --------------- | ------ | -------------------------- | ----------------------------------------- |
| `/core/login/`  | POST   | Obtain JWT tokens          | Public                                    |
| `/core/logout/` | POST   | Logout and blacklist token | Authenticated users                       |
| `core/tasks/`       | GET    | List tasks                 | Admin/Manager: all<br>User: only assigned |
| `core/tasks/`       | POST   | Create a new task          | Admin / Manager only                      |
| `core/tasks/<id>/`  | PUT    | Update a task              | Assigned user or Admin                    |
| `core/tasks/<id>/`  | DELETE | Delete a task              | Admin / Manager only                      |



## User Management
- Admins: Full access via `/admin`
- Managers: Can manage tasks/users
- Users: View/update assigned tasks
