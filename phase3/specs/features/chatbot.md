# Feature: AI-Powered Todo Chatbot

## User Stories
- As a user, I can add tasks through natural language
- As a user, I can view my tasks by asking "what's on my list?"
- As a user, I can mark tasks complete by saying "done with task 3"
- As a user, I can delete tasks by saying "remove the meeting task"
- As a user, I can update tasks by saying "change task 1 to call mom tonight"

## Acceptance Criteria

### Natural Language Understanding
- Agent interprets intent from user message
- Agent calls appropriate MCP tool(s)
- Agent confirms actions in friendly language

### Conversation Persistence
- All messages stored in database
- Conversation resumes across sessions
- No server memory required

### Tool Invocation
- add_task: Creates new task with title and description
- list_tasks: Returns tasks filtered by status
- complete_task: Marks task as done
- delete_task: Removes task from database
- update_task: Modifies task title/description

## Implementation Notes
- OpenAI GPT-4o-mini handles function calling
- MCP tools defined in `tools.py`
- Agent logic in `agent.py`
- Chat endpoint in `main.py` orchestrates flow

## Test Cases
1. ✅ Add task: "add task to buy milk" → creates task
2. ✅ List tasks: "show my tasks" → displays all tasks
3. ✅ Complete task: "mark task 1 as done" → updates status
4. ✅ Update task: "change task 1 to buy groceries" → updates title
5. ✅ Delete task: "remove task 1" → deletes from DB
