# Database Schema

## Tables

### users
- `id`: string (primary key) - User identifier
- `email`: string (unique) - User email
- `password`: string - Password hash
- `name`: string - Display name
- `created_at`: timestamp - Account creation
- `updated_at`: timestamp - Last update

### tasks
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key → users.id)
- `title`: string - Task title
- `description`: text (nullable) - Task details
- `completed`: boolean (default: false)
- `created_at`: timestamp
- `updated_at`: timestamp

### conversations
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key → users.id)
- `created_at`: timestamp
- `updated_at`: timestamp

### messages
- `id`: integer (primary key, auto-increment)
- `conversation_id`: integer (foreign key → conversations.id)
- `user_id`: string (foreign key → users.id)
- `role`: string ("user" | "assistant")
- `content`: text - Message content
- `created_at`: timestamp

## Indexes
- `users.email` - Unique constraint for login
- `tasks.user_id` - For filtering user's tasks
- `tasks.completed` - For status filtering
- `messages.conversation_id` - For fetching history

## Foreign Key Constraints
- `tasks.user_id` → `users.id`
- `conversations.user_id` → `users.id`
- `messages.conversation_id` → `conversations.id`
- `messages.user_id` → `users.id`
