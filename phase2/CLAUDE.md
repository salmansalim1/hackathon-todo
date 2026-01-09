# Todo App - Phase II

## Project Overview
Full-stack web application using spec-driven development with Next.js and FastAPI.

## Spec-Kit Structure
Specifications are organized in `/specs`:
- `/specs/overview.md` - Project overview and tech stack
- `/specs/constitution.md` - Development principles and standards
- `/specs/features/` - Feature specifications (authentication, task-crud)
- `/specs/database/` - Database schema and models
- `/specs/api/` - API endpoint specifications
- `/specs/ui/` - UI component specifications

## Project Structure
```
phase2/
├── .spec-kit/          # Spec-Kit configuration
├── specs/              # All specifications
├── frontend/           # Next.js 16 application
├── backend/            # Python FastAPI server
├── CLAUDE.md           # This file
└── README.md           # Documentation
```

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth

### Backend
- Python FastAPI
- SQLModel ORM
- Neon PostgreSQL
- JWT Authentication

## Development Workflow
1. **Read Specification**: Review relevant spec files in `/specs`
2. **Implement Backend**: Create FastAPI endpoints, models, database
3. **Implement Frontend**: Create Next.js pages, components, API client
4. **Test**: Verify functionality works as specified
5. **Iterate**: Update specs if requirements change

## How to Use Specs

When implementing features, always reference:
- `@specs/overview.md` - Overall project context
- `@specs/constitution.md` - Code standards and principles
- `@specs/features/[feature].md` - Specific feature requirements
- `@specs/database/schema.md` - Database structure
- `@specs/api/[endpoint].md` - API specifications

## Commands

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Security Notes
- All API endpoints require JWT authentication
- User data is isolated (user_id verification)
- Secrets must match between frontend and backend
- BETTER_AUTH_SECRET must be 32+ characters
