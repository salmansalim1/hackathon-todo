# Phase 3 Constitution: AI-Powered Todo Chatbot

## Project Principles

### Architecture Values
- **Stateless Server**: No in-memory state; all data persists in Neon DB
- **MCP-First**: All task operations exposed as MCP tools
- **Conversational AI**: Natural language interface using OpenAI GPT-4o-mini

### Technology Stack Constraints
- **Frontend**: Next.js 15+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **AI**: OpenAI GPT-4o-mini with function calling

### Security Rules
- Auto-create demo users for testing
- User-scoped data isolation (all queries filtered by `user_id`)
- Environment variables for secrets (DATABASE_URL, OPENAI_API_KEY)

### Performance Expectations
- Chat response < 3 seconds
- Database queries optimized with indexes
- Stateless design for horizontal scaling

### Code Quality Standards
- Type safety: Python type hints, TypeScript strict mode
- Error handling: Try-catch blocks, proper HTTP status codes
- Logging: Structured logs for debugging
