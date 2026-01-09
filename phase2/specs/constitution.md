# Project Constitution - Phase II

## Core Principles

### 1. Security First
- All API endpoints require JWT authentication
- User data must be isolated (no cross-user access)
- Passwords must be hashed (Better Auth handles this)
- Environment variables for sensitive data

### 2. Spec-Driven Development
- No code without a specification
- Every feature maps to a task
- Tasks reference specifications
- Use Claude Code for implementation

### 3. Code Quality Standards
- **Backend**: Type hints for all functions
- **Frontend**: TypeScript strict mode enabled
- **API**: Pydantic models for request/response validation
- **Database**: SQLModel for type-safe ORM operations

### 4. Architecture Patterns
- **Separation of Concerns**: Frontend and backend are separate services
- **RESTful API**: Standard HTTP methods and status codes
- **Stateless Backend**: JWT tokens, no server-side sessions
- **Database-First**: All state persists to PostgreSQL

### 5. Tech Stack Constraints
- **Frontend**: Next.js 16+ App Router only (no Pages Router)
- **Backend**: FastAPI with async/await
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (not raw SQL)
- **Auth**: Better Auth (JWT plugin enabled)
