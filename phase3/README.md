# Phase 3: AI-Powered Todo Chatbot

## Overview
A conversational AI chatbot for managing todos through natural language, built with OpenAI Agents SDK and MCP (Model Context Protocol).

## Features
- ✅ Natural language task management
- ✅ Conversation persistence across sessions
- ✅ Stateless architecture (scales horizontally)
- ✅ MCP tools for AI agent integration
- ✅ Auto-create demo users

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel, OpenAI Agents SDK
- **Database**: Neon Serverless PostgreSQL
- **AI Model**: GPT-4o-mini

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Neon PostgreSQL database
- OpenAI API key

### Backend Setup
```bash
cd phase3/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=your_neon_connection_string" > .env
echo "OPENAI_API_KEY=your_openai_key" >> .env

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd phase3/frontend
npm install
npm run dev
```

Open `http://localhost:3000`

## API Documentation

### POST /api/{user_id}/chat
Send a message to the chatbot.

**Request:**
```json
{
  "conversation_id": 123,  // optional
  "message": "add task to buy milk"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "I've added 'buy milk' to your task list.",
  "tool_calls": [...]
}
```

## MCP Tools
The AI agent can call these tools:
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
- "change task 1 to buy groceries and fruits"

## Architecture

### Stateless Chat Flow
1. User sends message
2. Backend auto-creates user if needed
3. Get/create conversation in DB
4. Store user message in DB
5. Fetch conversation history
6. Run OpenAI agent with MCP tools
7. Store assistant response in DB
8. Return response to client

### Database Schema
- **users**: User accounts
- **tasks**: Todo items
- **conversations**: Chat sessions
- **messages**: Chat history

## Deployment
- **Backend**: Render.com (https://hackathon-todo.onrender.com)
- **Frontend**: Vercel (https://hackathon-todo-lac.vercel.app)

## GitHub Repository
https://github.com/salmansalim1/hackathon-todo

## Demo Video
[Link to 90-second demo video]

## Author
Salman Salim (@salmansalim1)

## Phase 3 Completion
- [x] Backend with MCP tools
- [x] OpenAI agent integration
- [x] Chat endpoint with conversation persistence
- [x] Frontend chat interface
- [x] Database schema with auto-user creation
- [x] Documentation (README, CLAUDE.md, specs)
- [x] Local testing complete
- [ ] Deployed to Render.com
- [ ] Deployed to Vercel
- [ ] Demo video created
- [ ] Submitted to hackathon
