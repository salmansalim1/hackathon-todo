# Task T-004: Main Application Entry Point
# From: speckit.specify §4, speckit.plan §2.4
# Architecture: Model-View-Controller (MVC) Pattern

"""
main.py - Application entry point

Responsibilities:
- Application entry point
- Initialize and start the UI
- Handle top-level errors
"""

import sys
from ui import ConsoleUI


def main():
    """Main entry point for the Todo application."""
    try:
        # Initialize and run the UI
        app = ConsoleUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!\n")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please report this error if it persists.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
