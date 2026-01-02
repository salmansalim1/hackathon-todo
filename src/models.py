# Task T-001: Implement Task Data Model
# From: speckit.specify §1, speckit.plan §2.1
# Architecture: Model-View-Controller (MVC) Pattern

"""
models.py - Task data structure and storage

Responsibilities:
- Define task data structure
- Provide type safety
- Support CRUD operations on in-memory storage
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task.
    
    Attributes:
        id: Unique task identifier
        title: Task title (required, 1-200 chars)
        description: Optional task description
        completed: Task completion status
        created_at: Timestamp when task was created
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.completed = False
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task details.
        
        Args:
            title: New title (if provided)
            description: New description (if provided)
        """
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Task title cannot be empty")
            if len(title) > 200:
                raise ValueError("Task title cannot exceed 200 characters")
            self.title = title
        
        if description is not None:
            if len(description) > 1000:
                raise ValueError("Task description cannot exceed 1000 characters")
            self.description = description
    
    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        desc = f" - {self.description}" if self.description else ""
        return f"[{status}] {self.id}. {self.title}{desc}"


class TaskManager:
    """Manages in-memory task storage and operations.
    
    Responsibilities:
    - Store tasks in memory (list)
    - Generate unique task IDs
    - Provide CRUD operations
    """
    
    def __init__(self):
        """Initialize empty task storage."""
        self._tasks: list[Task] = []
        self._next_id: int = 1
    
    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and add a new task.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            
        Returns:
            The created Task object
            
        Raises:
            ValueError: If title is invalid
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.
        
        Args:
            task_id: The task ID to find
            
        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.
        
        Returns:
            List of all tasks
        """
        return self._tasks.copy()
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task.
        
        Args:
            task_id: The task ID to update
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            Updated task if found, None otherwise
            
        Raises:
            ValueError: If validation fails
        """
        task = self.get_task(task_id)
        if task:
            task.update(title=title, description=description)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            task_id: The task ID to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False
    
    def mark_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as complete.
        
        Args:
            task_id: The task ID to mark complete
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
        return task
    
    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete.
        
        Args:
            task_id: The task ID to mark incomplete
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
        return task
    
    def get_count(self) -> dict[str, int]:
        """Get task count statistics.
        
        Returns:
            Dictionary with total, completed, and pending counts
        """
        total = len(self._tasks)
        completed = sum(1 for task in self._tasks if task.completed)
        pending = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize task manager
    manager = TaskManager()
    
    # Create tasks
    task1 = manager.add_task("Buy groceries", "Milk, eggs, bread")
    task2 = manager.add_task("Call mom")
    task3 = manager.add_task("Complete hackathon Phase I")
    
    # Display all tasks
    print("All Tasks:")
    for task in manager.get_all_tasks():
        print(f"  {task}")
    
    # Mark task as complete
    manager.mark_complete(1)
    print("\nAfter marking task 1 complete:")
    print(f"  {manager.get_task(1)}")
    
    # Update task
    manager.update_task(2, description="Call mom about weekend plans")
    print("\nAfter updating task 2:")
    print(f"  {manager.get_task(2)}")
    
    # Statistics
    stats = manager.get_count()
    print(f"\nStatistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Pending: {stats['pending']}")
    
    # Delete task
    manager.delete_task(3)
    print("\nAfter deleting task 3:")
    for task in manager.get_all_tasks():
        print(f"  {task}")
