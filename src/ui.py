# Task T-003: Implement Console UI
# From: speckit.specify §3, speckit.plan §2.3
# Architecture: Model-View-Controller (MVC) Pattern

"""
ui.py - Console UI and formatting

Responsibilities:
- Console UI and formatting
- Display menu and handle user input
- Format task output for display
- Handle user interaction flow
"""

import os
import sys
from typing import Optional
from todo_manager import TodoController
from models import Task


class ConsoleUI:
    """Console-based user interface for Todo application.
    
    Provides an interactive menu system for managing tasks
    through the command line interface.
    """
    
    def __init__(self):
        """Initialize the UI with a TodoController."""
        self.controller = TodoController()
        self.running = True
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print application header."""
        print("\n" + "="*60)
        print(" "*20 + "📝 TODO APP" + " "*20)
        print("="*60)
    
    def print_menu(self):
        """Display the main menu."""
        print("\n" + "-"*60)
        print("MENU OPTIONS:")
        print("-"*60)
        print("  1. Add Task")
        print("  2. View All Tasks")
        print("  3. View Task by ID")
        print("  4. Update Task")
        print("  5. Delete Task")
        print("  6. Mark Task Complete")
        print("  7. Mark Task Incomplete")
        print("  8. Toggle Task Status")
        print("  9. View Statistics")
        print(" 10. View Pending Tasks")
        print(" 11. View Completed Tasks")
        print("  0. Exit")
        print("-"*60)
    
    def print_separator(self, char="-", length=60):
        """Print a separator line."""
        print(char * length)
    
    def display_task(self, task: Task, detailed: bool = False):
        """Display a single task.
        
        Args:
            task: The task to display
            detailed: If True, show full details
        """
        if detailed:
            status = "✓ Completed" if task.completed else "○ Pending"
            print(f"\nTask ID: {task.id}")
            print(f"Title: {task.title}")
            if task.description:
                print(f"Description: {task.description}")
            print(f"Status: {status}")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"  {task}")
    
    def display_tasks(self, tasks: list[Task], show_empty: bool = True):
        """Display a list of tasks.
        
        Args:
            tasks: List of tasks to display
            show_empty: Whether to show message if list is empty
        """
        if not tasks:
            if show_empty:
                print("\n  No tasks to display.")
        else:
            print()
            for task in tasks:
                self.display_task(task)
    
    def display_statistics(self, stats: dict):
        """Display task statistics.
        
        Args:
            stats: Dictionary containing task statistics
        """
        print("\n" + "-"*60)
        print("TASK STATISTICS:")
        print("-"*60)
        print(f"  Total Tasks:     {stats['total']}")
        print(f"  Completed:       {stats['completed']}")
        print(f"  Pending:         {stats['pending']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"  Completion Rate: {completion_rate:.1f}%")
        print("-"*60)
    
    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation.
        
        Args:
            prompt: The prompt to display
            required: If True, empty input is not allowed
            
        Returns:
            User input string or None if empty and not required
        """
        while True:
            try:
                value = input(prompt).strip()
                
                if not value and required:
                    print("  ⚠ Input cannot be empty. Please try again.")
                    continue
                
                if not value and not required:
                    return None
                
                return value
            except (EOFError, KeyboardInterrupt):
                print("\n  ⚠ Input cancelled.")
                return None
    
    def get_int_input(self, prompt: str) -> Optional[int]:
        """Get integer input from user.
        
        Args:
            prompt: The prompt to display
            
        Returns:
            Integer value or None if invalid
        """
        value = self.get_input(prompt, required=True)
        if value is None:
            return None
        
        try:
            return int(value)
        except ValueError:
            print(f"  ⚠ Invalid number: '{value}'. Please enter a valid integer.")
            return None
    
    def confirm_action(self, message: str) -> bool:
        """Ask user to confirm an action.
        
        Args:
            message: The confirmation message
            
        Returns:
            True if user confirms, False otherwise
        """
        response = self.get_input(f"{message} (y/n): ", required=True)
        return response and response.lower() in ['y', 'yes']
    
    def pause(self):
        """Pause and wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    def handle_add_task(self):
        """Handle adding a new task."""
        self.print_separator()
        print("ADD NEW TASK")
        self.print_separator()
        
        title = self.get_input("Enter task title: ")
        if title is None:
            return
        
        description = self.get_input("Enter task description (optional, press Enter to skip): ", required=False)
        
        success, message, task = self.controller.add_task(title, description)
        print(f"\n{message}")
        
        if success and task:
            self.display_task(task, detailed=True)
    
    def handle_view_all_tasks(self):
        """Handle viewing all tasks."""
        self.print_separator()
        print("ALL TASKS")
        self.print_separator()
        
        success, message, tasks = self.controller.view_all_tasks()
        print(f"\n{message}")
        self.display_tasks(tasks, show_empty=False)
    
    def handle_view_task(self):
        """Handle viewing a specific task."""
        self.print_separator()
        print("VIEW TASK BY ID")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID: ")
        if task_id is None:
            return
        
        success, message, task = self.controller.view_task(task_id)
        print(f"\n{message}")
        
        if success and task:
            self.display_task(task, detailed=True)
    
    def handle_update_task(self):
        """Handle updating a task."""
        self.print_separator()
        print("UPDATE TASK")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID to update: ")
        if task_id is None:
            return
        
        # First, show the current task
        success, message, task = self.controller.view_task(task_id)
        if not success:
            print(f"\n{message}")
            return
        
        print("\nCurrent task:")
        self.display_task(task, detailed=True)
        
        print("\nEnter new values (press Enter to keep current value):")
        new_title = self.get_input("New title: ", required=False)
        new_description = self.get_input("New description: ", required=False)
        
        if new_title is None and new_description is None:
            print("\n  ⚠ No updates provided.")
            return
        
        success, message, updated_task = self.controller.update_task(task_id, new_title, new_description)
        print(f"\n{message}")
        
        if success and updated_task:
            print("\nUpdated task:")
            self.display_task(updated_task, detailed=True)
    
    def handle_delete_task(self):
        """Handle deleting a task."""
        self.print_separator()
        print("DELETE TASK")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID to delete: ")
        if task_id is None:
            return
        
        # Show the task first
        success, message, task = self.controller.view_task(task_id)
        if not success:
            print(f"\n{message}")
            return
        
        print("\nTask to delete:")
        self.display_task(task, detailed=True)
        
        if not self.confirm_action("\nAre you sure you want to delete this task?"):
            print("\n  ℹ Deletion cancelled.")
            return
        
        success, message = self.controller.delete_task(task_id)
        print(f"\n{message}")
    
    def handle_mark_complete(self):
        """Handle marking a task as complete."""
        self.print_separator()
        print("MARK TASK COMPLETE")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID: ")
        if task_id is None:
            return
        
        success, message, task = self.controller.mark_complete(task_id)
        print(f"\n{message}")
        
        if success and task:
            self.display_task(task, detailed=True)
    
    def handle_mark_incomplete(self):
        """Handle marking a task as incomplete."""
        self.print_separator()
        print("MARK TASK INCOMPLETE")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID: ")
        if task_id is None:
            return
        
        success, message, task = self.controller.mark_incomplete(task_id)
        print(f"\n{message}")
        
        if success and task:
            self.display_task(task, detailed=True)
    
    def handle_toggle_status(self):
        """Handle toggling task completion status."""
        self.print_separator()
        print("TOGGLE TASK STATUS")
        self.print_separator()
        
        task_id = self.get_int_input("Enter task ID: ")
        if task_id is None:
            return
        
        success, message, task = self.controller.toggle_complete(task_id)
        print(f"\n{message}")
        
        if success and task:
            self.display_task(task, detailed=True)
    
    def handle_view_statistics(self):
        """Handle viewing task statistics."""
        self.print_separator()
        print("TASK STATISTICS")
        self.print_separator()
        
        success, message, stats = self.controller.get_statistics()
        
        if success:
            self.display_statistics(stats)
        else:
            print(f"\n{message}")
    
    def handle_view_pending_tasks(self):
        """Handle viewing pending tasks."""
        self.print_separator()
        print("PENDING TASKS")
        self.print_separator()
        
        success, message, tasks = self.controller.get_filtered_tasks("pending")
        print(f"\n{message}")
        self.display_tasks(tasks, show_empty=False)
    
    def handle_view_completed_tasks(self):
        """Handle viewing completed tasks."""
        self.print_separator()
        print("COMPLETED TASKS")
        self.print_separator()
        
        success, message, tasks = self.controller.get_filtered_tasks("completed")
        print(f"\n{message}")
        self.display_tasks(tasks, show_empty=False)
    
    def handle_exit(self):
        """Handle application exit."""
        if self.confirm_action("\nAre you sure you want to exit?"):
            print("\n👋 Thank you for using Todo App. Goodbye!\n")
            self.running = False
        else:
            print("\n  ℹ Exit cancelled.")
    
    def run(self):
        """Run the main application loop."""
        try:
            while self.running:
                self.clear_screen()
                self.print_header()
                self.print_menu()
                
                choice = self.get_input("\nEnter your choice (0-11): ")
                
                if choice is None:
                    continue
                
                # Route to appropriate handler
                handlers = {
                    '1': self.handle_add_task,
                    '2': self.handle_view_all_tasks,
                    '3': self.handle_view_task,
                    '4': self.handle_update_task,
                    '5': self.handle_delete_task,
                    '6': self.handle_mark_complete,
                    '7': self.handle_mark_incomplete,
                    '8': self.handle_toggle_status,
                    '9': self.handle_view_statistics,
                    '10': self.handle_view_pending_tasks,
                    '11': self.handle_view_completed_tasks,
                    '0': self.handle_exit
                }
                
                handler = handlers.get(choice)
                
                if handler:
                    handler()
                else:
                    print(f"\n  ⚠ Invalid choice: '{choice}'. Please select 0-11.")
                
                if self.running:
                    self.pause()
        
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            sys.exit(1)


# For testing the UI
if __name__ == "__main__":
    print("This is the UI module. Run main.py to start the application.")
