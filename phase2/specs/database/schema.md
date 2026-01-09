# Database Schema

## Connection
- **Provider**: Neon Serverless PostgreSQL
- **Connection String**: Set via `DATABASE_URL` environment variable
- **Connection Pooling**: Enabled by default in Neon

## Tables

### users (managed by Better Auth)
| Column      | Type      | Constraints           | Description          |
|-------------|-----------|-----------------------|----------------------|
| id          | TEXT      | PRIMARY KEY           | Unique user ID       |
| email       | TEXT      | UNIQUE, NOT NULL      | User email           |
| name        | TEXT      | NULL                  | User display name    |
| emailVerified | BOOLEAN | DEFAULT FALSE         | Email verification   |
| createdAt   | TIMESTAMP | DEFAULT CURRENT_TIME  | Account creation     |

### tasks
| Column      | Type      | Constraints           | Description          |
|-------------|-----------|-----------------------|----------------------|
| id          | INTEGER   | PRIMARY KEY, AUTO     | Task ID              |
| user_id     | TEXT      | FOREIGN KEY, NOT NULL | Owner of task        |
| title       | TEXT      | NOT NULL              | Task title (1-200)   |
| description | TEXT      | NULL                  | Task details         |
| completed   | BOOLEAN   | DEFAULT FALSE         | Completion status    |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TIME  | Creation timestamp   |
| updated_at  | TIMESTAMP | DEFAULT CURRENT_TIME  | Last update          |

## Indexes
- `idx_tasks_user_id` on `tasks.user_id` (for filtering by user)
- `idx_tasks_completed` on `tasks.completed` (for status filtering)
