# Task T-002: Implement Todo Manager Controller
# From: speckit.specify §2, speckit.plan §2.2
# Architecture: Model-View-Controller (MVC) Pattern

"""
todo_manager.py - Core business logic and operations

Responsibilities:
- Business logic and operations
- Coordinate between model and UI
- Validate user inputs
- Handle error cases
"""

from typing import Optional
from models import Task, TaskManager


class TodoController:
    """Controller for Todo application business logic.
    
    Coordinates operations between the UI and the data model,
    handles validation, and provides user-friendly error messages.
    """
    
    def __init__(self):
        """Initialize the controller with a TaskManager."""
        self._manager = TaskManager()
    
    def add_task(self, title: str, description: Optional[str] = None) -> tuple[bool, str, Optional[Task]]:
        """Add a new task.
        
        Args:
            title: Task title
            description: Optional task description
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            # Validate and clean input
            title = title.strip()
            if not title:
                return False, "Error: Task title cannot be empty.", None
            
            if description:
                description = description.strip()
                if not description:
                    description = None
            
            # Create task
            task = self._manager.add_task(title, description)
            return True, f"✓ Task added successfully: '{task.title}' (ID: {task.id})", task
            
        except ValueError as e:
            return False, f"Error: {str(e)}", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def view_all_tasks(self) -> tuple[bool, str, list[Task]]:
        """View all tasks.
        
        Returns:
            Tuple of (success: bool, message: str, tasks: list[Task])
        """
        try:
            tasks = self._manager.get_all_tasks()
            
            if not tasks:
                return True, "No tasks found. Add your first task!", []
            
            return True, f"Found {len(tasks)} task(s):", tasks
            
        except Exception as e:
            return False, f"Error retrieving tasks: {str(e)}", []
    
    def view_task(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """View a specific task by ID.
        
        Args:
            task_id: The task ID to view
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            task = self._manager.get_task(task_id)
            
            if not task:
                return False, f"Error: Task with ID {task_id} not found.", None
            
            return True, "Task found:", task
            
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None) -> tuple[bool, str, Optional[Task]]:
        """Update an existing task.
        
        Args:
            task_id: The task ID to update
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            # Check if task exists
            task = self._manager.get_task(task_id)
            if not task:
                return False, f"Error: Task with ID {task_id} not found.", None
            
            # Validate inputs if provided
            if title is not None:
                title = title.strip()
                if not title:
                    return False, "Error: Task title cannot be empty.", None
            
            if description is not None:
                description = description.strip()
                if not description:
                    description = None
            
            # Check if anything to update
            if title is None and description is None:
                return False, "Error: No updates provided. Specify title or description.", None
            
            # Update task
            updated_task = self._manager.update_task(task_id, title, description)
            return True, f"✓ Task updated successfully: '{updated_task.title}' (ID: {task_id})", updated_task
            
        except ValueError as e:
            return False, f"Error: {str(e)}", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task.
        
        Args:
            task_id: The task ID to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check if task exists first
            task = self._manager.get_task(task_id)
            if not task:
                return False, f"Error: Task with ID {task_id} not found."
            
            # Store title for confirmation message
            task_title = task.title
            
            # Delete task
            success = self._manager.delete_task(task_id)
            if success:
                return True, f"✓ Task deleted successfully: '{task_title}' (ID: {task_id})"
            else:
                return False, f"Error: Failed to delete task {task_id}."
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def toggle_complete(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """Toggle task completion status.
        
        Args:
            task_id: The task ID to toggle
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            # Check if task exists
            task = self._manager.get_task(task_id)
            if not task:
                return False, f"Error: Task with ID {task_id} not found.", None
            
            # Toggle based on current status
            if task.completed:
                updated_task = self._manager.mark_incomplete(task_id)
                return True, f"✓ Task marked as incomplete: '{updated_task.title}' (ID: {task_id})", updated_task
            else:
                updated_task = self._manager.mark_complete(task_id)
                return True, f"✓ Task marked as complete: '{updated_task.title}' (ID: {task_id})", updated_task
            
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def mark_complete(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """Mark a task as complete.
        
        Args:
            task_id: The task ID to mark complete
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            # Check if task exists
            task = self._manager.get_task(task_id)
            if not task:
                return False, f"Error: Task with ID {task_id} not found.", None
            
            # Check if already complete
            if task.completed:
                return False, f"Task '{task.title}' (ID: {task_id}) is already complete.", task
            
            # Mark complete
            updated_task = self._manager.mark_complete(task_id)
            return True, f"✓ Task marked as complete: '{updated_task.title}' (ID: {task_id})", updated_task
            
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def mark_incomplete(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """Mark a task as incomplete.
        
        Args:
            task_id: The task ID to mark incomplete
            
        Returns:
            Tuple of (success: bool, message: str, task: Optional[Task])
        """
        try:
            # Check if task exists
            task = self._manager.get_task(task_id)
            if not task:
                return False, f"Error: Task with ID {task_id} not found.", None
            
            # Check if already incomplete
            if not task.completed:
                return False, f"Task '{task.title}' (ID: {task_id}) is already incomplete.", task
            
            # Mark incomplete
            updated_task = self._manager.mark_incomplete(task_id)
            return True, f"✓ Task marked as incomplete: '{updated_task.title}' (ID: {task_id})", updated_task
            
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def get_statistics(self) -> tuple[bool, str, dict]:
        """Get task statistics.
        
        Returns:
            Tuple of (success: bool, message: str, stats: dict)
        """
        try:
            stats = self._manager.get_count()
            return True, "Statistics retrieved successfully.", stats
            
        except Exception as e:
            return False, f"Error: {str(e)}", {}
    
    def get_filtered_tasks(self, filter_type: str = "all") -> tuple[bool, str, list[Task]]:
        """Get filtered list of tasks.
        
        Args:
            filter_type: "all", "completed", or "pending"
            
        Returns:
            Tuple of (success: bool, message: str, tasks: list[Task])
        """
        try:
            all_tasks = self._manager.get_all_tasks()
            
            if filter_type == "completed":
                filtered = [t for t in all_tasks if t.completed]
                msg = f"Found {len(filtered)} completed task(s):"
            elif filter_type == "pending":
                filtered = [t for t in all_tasks if not t.completed]
                msg = f"Found {len(filtered)} pending task(s):"
            else:  # all
                filtered = all_tasks
                msg = f"Found {len(filtered)} task(s):"
            
            if not filtered:
                return True, f"No {filter_type} tasks found.", []
            
            return True, msg, filtered
            
        except Exception as e:
            return False, f"Error: {str(e)}", []


# Example usage and testing
if __name__ == "__main__":
    print("=== TodoController Test ===\n")
    
    controller = TodoController()
    
    # Test 1: Add tasks
    print("1. Adding tasks...")
    success, msg, task = controller.add_task("Buy groceries", "Milk, eggs, bread")
    print(f"   {msg}")
    
    success, msg, task = controller.add_task("Call mom")
    print(f"   {msg}")
    
    success, msg, task = controller.add_task("Complete hackathon Phase I", "Finish T-001 to T-004")
    print(f"   {msg}\n")
    
    # Test 2: View all tasks
    print("2. Viewing all tasks...")
    success, msg, tasks = controller.view_all_tasks()
    print(f"   {msg}")
    for task in tasks:
        print(f"   {task}")
    print()
    
    # Test 3: Mark complete
    print("3. Marking task 1 as complete...")
    success, msg, task = controller.mark_complete(1)
    print(f"   {msg}\n")
    
    # Test 4: Update task
    print("4. Updating task 2...")
    success, msg, task = controller.update_task(2, description="Call mom about weekend plans")
    print(f"   {msg}\n")
    
    # Test 5: View statistics
    print("5. Getting statistics...")
    success, msg, stats = controller.get_statistics()
    print(f"   {msg}")
    print(f"   Total: {stats['total']}, Completed: {stats['completed']}, Pending: {stats['pending']}\n")
    
    # Test 6: Filter tasks
    print("6. Viewing pending tasks...")
    success, msg, tasks = controller.get_filtered_tasks("pending")
    print(f"   {msg}")
    for task in tasks:
        print(f"   {task}")
    print()
    
    # Test 7: Delete task
    print("7. Deleting task 3...")
    success, msg = controller.delete_task(3)
    print(f"   {msg}\n")
    
    # Test 8: Error handling - invalid task ID
    print("8. Testing error handling (invalid ID)...")
    success, msg, task = controller.view_task(999)
    print(f"   {msg}\n")
    
    # Test 9: Final task list
    print("9. Final task list...")
    success, msg, tasks = controller.view_all_tasks()
    print(f"   {msg}")
    for task in tasks:
        print(f"   {task}")
