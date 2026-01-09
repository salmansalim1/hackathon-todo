# Hackathon II - Todo App (Phase II Complete)

A full-stack todo application built with Next.js, FastAPI, and PostgreSQL using Spec-Driven Development.

## 🏗️ Architecture

- **Frontend**: Next.js 15 (App Router) + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI + SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

## 📁 Project Structure
```
hackathon-todo/
├── phase1/              # Console app (Phase I)
├── phase2/
│   ├── backend/         # FastAPI server
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── requirements.txt
│   └── frontend/        # Next.js app
│       ├── app/
│       ├── components/
│       └── lib/
├── specs/               # Specifications
└── README.md
```

## 🚀 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon account)

### Backend Setup
```bash
cd phase2/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your Neon database credentials

# Run server
uvicorn main:app --reload --port 8000
```

Backend will run at: `http://localhost:8000`

### Frontend Setup
```bash
cd phase2/frontend

# Install dependencies
npm install

# Create .env.local file (copy from .env.example)
cp .env.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 🔑 Environment Variables

### Backend (.env)
- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (min 32 characters)
- `CORS_ORIGINS`: Allowed frontend URLs

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `BETTER_AUTH_SECRET`: Better Auth secret key
- `DATABASE_URL`: Database connection for Better Auth

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## ✅ Completed Features (Basic Level)

1. ✅ Add Task - Create new todo items
2. ✅ Delete Task - Remove tasks from the list
3. ✅ Update Task - Modify existing task details
4. ✅ View Task List - Display all tasks
5. ✅ Mark as Complete - Toggle task completion status
6. ✅ Authentication - User signup/signin with Better Auth

## 🌐 Deployment

### Backend (Render.com)
- Deployed at: `https://hackathon-todo.onrender.com`

### Frontend (Vercel)
- Deployed at: `https://your-app.vercel.app`

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## 📝 Specifications

All specifications are maintained in the `/specs` directory following Spec-Driven Development principles.

## 🛠️ Technologies Used

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, Pydantic
- **Database**: Neon PostgreSQL
- **Auth**: Better Auth, JWT
- **Deployment**: Vercel (Frontend), Render (Backend)

## 👤 Author

Salman Salim (@salmansalim1)

## 📄 License

This project is part of Panaversity Hackathon II.
