# Task Management API with JWT Authentication

## Features
- Secure JWT authentication (login/logout)
- Role-based access control (Admin/Manager/User)
- Full task CRUD operations
- Automated user deactivation after 5 missed deadlines
- Admin panel integration

## Setup Instructions
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
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/auth/login/` | POST | Get JWT tokens | Public |
| `/auth/logout/` | POST | Invalidate refresh token | Authenticated |
| `/tasks/` | GET | List tasks | Admin:all, User:assigned |
| `/tasks/` | POST | Create task | Admin/Manager only |

## User Management
- Admins: Full access via `/admin`
- Managers: Can manage tasks/users
- Users: View/update assigned tasks

See Postman collection for detailed API examples.
