# Todo Console Application - Phase I

A command-line todo application built using Spec-Driven Development with Claude Code.

## Features

- ✅ Add Task - Create new todo items
- ✅ Delete Task - Remove tasks from the list
- ✅ Update Task - Modify existing task details
- ✅ View Task List - Display all tasks
- ✅ Mark as Complete - Toggle task completion status

## Tech Stack

- Python 3.13+
- Spec-Driven Development (SDD)
- Claude Code
- Spec-Kit Plus

## Project Structure
```
hackathon-todo-phase1/
├── src/
│   ├── models.py          # Task data model and storage
│   ├── todo_manager.py    # Business logic controller
│   ├── ui.py              # Console UI interface
│   └── main.py            # Application entry point
├── specs/                 # Specification files
├── README.md
└── CLAUDE.md
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/salmansalim1/hackathon-todo.git
cd hackathon-todo
```

2. Run the application:
```bash
python3 src/main.py
```

## Usage

The application provides an interactive menu with the following options:

1. Add Task - Create a new task with title and optional description
2. View All Tasks - Display all tasks with their status
3. View Task by ID - View details of a specific task
4. Update Task - Modify task title or description
5. Delete Task - Remove a task from the list
6. Mark Task Complete - Mark a task as done
7. Mark Task Incomplete - Reopen a completed task
8. Toggle Task Status - Switch between complete/incomplete
9. View Statistics - See task completion statistics
10. View Pending Tasks - Show only incomplete tasks
11. View Completed Tasks - Show only completed tasks
0. Exit - Close the application

## Development Approach

This project was built using **Spec-Driven Development (SDD)**:
1. Write specifications in `speckit.specify`
2. Generate technical plan in `speckit.plan`
3. Break down into tasks in `speckit.tasks`
4. Implement using Claude Code

## Architecture

**Model-View-Controller (MVC) Pattern**:
- **Model** (`models.py`): Task data structure and in-memory storage
- **Controller** (`todo_manager.py`): Business logic and operations
- **View** (`ui.py`): Console interface and user interaction
- **Main** (`main.py`): Application entry point

## Phase I Completion

- [x] T-001: Implement Task Data Model
- [x] T-002: Implement Todo Manager Controller
- [x] T-003: Implement Console UI
- [x] T-004: Create Main Entry Point

## Author

Salman Salim (@salmansalim1)

## License

This project is part of the Panaversity Hackathon II.
