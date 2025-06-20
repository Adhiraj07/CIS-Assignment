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

## API Endpoints

| Endpoint        | Method | Description                | Access Level                              |
| --------------- | ------ | -------------------------- | ----------------------------------------- |
| `/auth/login/`  | POST   | Obtain JWT tokens          | Public                                    |
| `/auth/logout/` | POST   | Logout and blacklist token | Authenticated users                       |
| `/tasks/`       | GET    | List tasks                 | Admin/Manager: all<br>User: only assigned |
| `/tasks/`       | POST   | Create a new task          | Admin / Manager only                      |
| `/tasks/<id>/`  | PUT    | Update a task              | Assigned user or Admin                    |
| `/tasks/<id>/`  | DELETE | Delete a task              | Admin / Manager only                      |

## User Management
- Admins: Full access via `/admin`
- Managers: Can manage tasks/users
- Users: View/update assigned tasks