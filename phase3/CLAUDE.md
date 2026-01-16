# Phase 3: AI-Powered Todo Chatbot

## Project Overview
This phase transforms the todo app into a conversational AI chatbot using OpenAI Agents SDK and MCP tools.

## Spec-Kit Structure
Specifications are in `/specs`:
- `/specs/constitution.md` - Project principles
- `/specs/features/chatbot.md` - Feature requirements
- `/specs/api/chat-endpoint.md` - API specification
- `/specs/database/schema.md` - Database schema

## Project Structure
```
phase3/
├── backend/
│   ├── main.py          # FastAPI server + chat endpoint
│   ├── models.py        # SQLModel database models
│   ├── db.py            # Database connection
│   ├── tools.py         # MCP tools (add, list, complete, delete, update)
│   ├── agent.py         # OpenAI agent logic
│   ├── requirements.txt
│   └── .env             # DATABASE_URL, OPENAI_API_KEY
├── frontend/
│   ├── app/page.tsx     # Chat interface
│   ├── app/layout.tsx
│   └── app/globals.css
└── specs/               # Specifications
```

## Development Workflow
1. Read relevant spec before implementing
2. Reference specs: @specs/features/chatbot.md
3. Test locally before deployment

## Commands

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Architecture
- **Stateless Chat Endpoint**: POST /api/{user_id}/chat
- **Conversation Persistence**: All messages stored in Neon DB
- **AI Agent**: OpenAI GPT-4o-mini with function calling
- **MCP Tools**: Task CRUD operations exposed to agent

## MCP Tools
- `add_task` - Create new task
- `list_tasks` - View tasks (all/pending/completed)
- `complete_task` - Mark task as done
- `delete_task` - Remove task
- `update_task` - Modify task details

## Example Commands
- "add task to call mom"
- "show me all my tasks"
- "mark task 3 as complete"
- "delete the meeting task"
- "change task 1 to buy groceries"
