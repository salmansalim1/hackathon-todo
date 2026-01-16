# API Specification: Chat Endpoint

## POST /api/{user_id}/chat

### Purpose
Send a message to the AI chatbot and receive a response.

### Path Parameters
- `user_id` (string, required): Unique identifier for the user

### Request Body
```json
{
  "conversation_id": 123,  // optional: existing conversation
  "message": "add task to buy groceries"
}
```

### Response
```json
{
  "conversation_id": 123,
  "response": "I've added 'buy groceries' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {"user_id": "demo-user", "title": "buy groceries"},
      "result": {"task_id": 5, "status": "created"}
    }
  ]
}
```

### Status Codes
- 200: Success
- 404: Conversation not found
- 500: Server error

### Flow
1. Auto-create user if doesn't exist
2. Get or create conversation
3. Store user message
4. Fetch conversation history
5. Run OpenAI agent with MCP tools
6. Store assistant response
7. Return response to client

## GET /api/{user_id}/conversations

List all conversations for a user.

### Response
```json
{
  "conversations": [
    {
      "id": 1,
      "user_id": "demo-user",
      "created_at": "2026-01-16T09:38:27",
      "updated_at": "2026-01-16T09:38:27"
    }
  ]
}
```

## GET /api/{user_id}/conversations/{conversation_id}

Get full conversation with message history.

### Response
```json
{
  "conversation": {
    "id": 1,
    "user_id": "demo-user"
  },
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "add task to buy milk",
      "created_at": "2026-01-16T09:38:27"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I've added 'buy milk' to your list.",
      "created_at": "2026-01-16T09:38:28"
    }
  ]
}
```
