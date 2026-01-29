"""
MCP-style tools for task management (without official MCP SDK)
"""
from sqlmodel import Session, select
from models import Task
from db import engine
import json


# Define tool schemas for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by task status"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Remove a task from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Modify task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]


def execute_tool(user_id: str, tool_name: str, arguments: dict) -> str:
    """Execute a tool and return JSON result."""
    
    if tool_name == "add_task":
        return add_task(user_id, arguments)
    elif tool_name == "list_tasks":
        return list_tasks(user_id, arguments)
    elif tool_name == "complete_task":
        return complete_task(user_id, arguments)
    elif tool_name == "delete_task":
        return delete_task(user_id, arguments)
    elif tool_name == "update_task":
        return update_task(user_id, arguments)
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def add_task(user_id: str, args: dict) -> str:
    """Add a new task."""
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=args["title"],
            description=args.get("description", "")
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        result = {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }
        return json.dumps(result)


def list_tasks(user_id: str, args: dict) -> str:
    """List tasks with optional status filter."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        
        status = args.get("status", "all")
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        tasks = session.exec(statement).all()
        
        result = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
        return json.dumps(result)


def complete_task(user_id: str, args: dict) -> str:
    """Mark a task as complete."""
    with Session(engine) as session:
        statement = select(Task).where(
            Task.id == args["task_id"],
            Task.user_id == user_id
        )
        task = session.exec(statement).first()
        
        if not task:
            return json.dumps({"error": "Task not found"})
        
        task.completed = True
        session.add(task)
        session.commit()
        
        result = {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }
        return json.dumps(result)


def delete_task(user_id: str, args: dict) -> str:
    """Delete a task."""
    with Session(engine) as session:
        statement = select(Task).where(
            Task.id == args["task_id"],
            Task.user_id == user_id
        )
        task = session.exec(statement).first()
        
        if not task:
            return json.dumps({"error": "Task not found"})
        
        title = task.title
        session.delete(task)
        session.commit()
        
        result = {
            "task_id": args["task_id"],
            "status": "deleted",
            "title": title
        }
        return json.dumps(result)


def update_task(user_id: str, args: dict) -> str:
    """Update a task."""
    with Session(engine) as session:
        statement = select(Task).where(
            Task.id == args["task_id"],
            Task.user_id == user_id
        )
        task = session.exec(statement).first()
        
        if not task:
            return json.dumps({"error": "Task not found"})
        
        if "title" in args:
            task.title = args["title"]
        if "description" in args:
            task.description = args["description"]
        
        session.add(task)
        session.commit()
        
        result = {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }
        return json.dumps(result)
