# Hackathon II - Phase II: Todo Full-Stack Web Application

## Project Overview
A multi-user todo application with authentication, built using spec-driven development.

## Tech Stack
- **Frontend:** Next.js 15+ (App Router), React, Tailwind CSS, Better Auth
- **Backend:** Python FastAPI, SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Development:** Claude Code, Spec-Kit Plus

## Project Structure
```
phase2/
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/          # Next.js frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── .env.example
├── specs/             # Specifications
│   ├── overview.md
│   ├── constitution.md
│   ├── features/
│   └── database/
└── README.md
```

## Features Implemented
✅ User Authentication (Better Auth)
✅ Add Task
✅ Delete Task
✅ Update Task
✅ View Task List
✅ Mark as Complete/Incomplete
✅ Multi-user support with user isolation

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon account)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your actual credentials

# Run backend
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your actual credentials

# Run frontend
npm run dev
```

Visit http://localhost:3000

## Deployment

### Backend: Render.com
See deployment instructions in DEPLOYMENT.md

### Frontend: Vercel
See deployment instructions in DEPLOYMENT.md

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Minimum 32 character secret
- `BETTER_AUTH_URL`: Frontend URL
- `CORS_ORIGINS`: Allowed origins (comma-separated)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `BETTER_AUTH_SECRET`: Same as backend
- `BETTER_AUTH_URL`: Frontend URL
- `DATABASE_URL`: Neon PostgreSQL connection string

## API Endpoints

### Authentication
- POST `/api/auth/signup` - Register new user
- POST `/api/auth/signin` - Login user
- POST `/api/auth/signout` - Logout user

### Tasks
- GET `/api/{user_id}/tasks` - List all tasks
- POST `/api/{user_id}/tasks` - Create task
- GET `/api/{user_id}/tasks/{id}` - Get task details
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

## Development Approach
This project was built using **Spec-Driven Development**:
1. Write specifications in `/specs`
2. Use Claude Code to generate implementation
3. Iterate on specs until correct output

## License
MIT

## Author
Salman Salim - Panaversity Hackathon II
