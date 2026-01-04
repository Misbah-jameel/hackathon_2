"""
main.py - Entry Point for Hackathon 2 Task Manager

This is the main entry point for the console application.
Provides menu-driven interface for task management with AI assistance.

Hackathon 2 - Phase 1: In-Memory Python Console Application
"""

from typing import Optional
from models import Task, Priority, Status
from store import task_store
from gemini_service import gemini_service
from ui import (
    clear_screen, print_header, print_subheader, print_success,
    print_error, print_warning, print_info, display_task,
    display_task_list, display_stats, get_input, get_int_input,
    get_choice, get_priority, get_status, get_due_date, confirm,
    press_enter_to_continue, display_menu
)


# ==================== APPLICATION INFO ====================

APP_NAME = "Task Manager Pro"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-Powered Task Management Console Application"


# ==================== CRUD OPERATIONS ====================

def add_task():
    """Add a new task to the store"""
    print_header("Add New Task")

    # Get required title
    title = get_input("Enter task title", required=True)
    if not title:
        print_warning("Task creation cancelled.")
        return

    # Get optional description
    description = get_input("Enter description (optional)", required=False)

    # Get priority
    print("\nSelect priority:")
    priority = get_priority()
    if priority is None:
        priority = Priority.MEDIUM  # Default if cancelled

    # Get optional due date
    due_date, _ = get_due_date()

    # Get optional tags
    tags_input = get_input("Enter tags (comma-separated, optional)", required=False)
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    # Create the task
    task = task_store.add_task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        tags=tags
    )

    print_success(f"Task #{task.id} created successfully!")
    display_task(task, detailed=True)


def view_all_tasks():
    """Display all tasks in the store"""
    tasks = task_store.get_all_tasks()
    display_task_list(tasks, "All Tasks")


def view_task_details():
    """View detailed information about a specific task"""
    print_header("View Task Details")

    task_id = get_int_input("Enter task ID")
    if task_id is None:
        return

    task = task_store.get_task(task_id)
    if task:
        display_task(task, detailed=True)
    else:
        print_error(f"Task #{task_id} not found.")


def update_task():
    """Update an existing task"""
    print_header("Update Task")

    task_id = get_int_input("Enter task ID to update")
    if task_id is None:
        return

    task = task_store.get_task(task_id)
    if not task:
        print_error(f"Task #{task_id} not found.")
        return

    print("\nCurrent task:")
    display_task(task, detailed=True)

    print("\nLeave blank to keep current value.")

    # Get updates (all optional)
    new_title = get_input(f"New title", required=False, default=task.title)
    new_description = get_input(f"New description", required=False, default=task.description)

    # Priority update
    print("\nUpdate priority?")
    if confirm("Change priority?", default=False):
        new_priority = get_priority()
    else:
        new_priority = None

    # Status update
    print("\nUpdate status?")
    if confirm("Change status?", default=False):
        new_status = get_status()
    else:
        new_status = None

    # Due date update
    print("\nUpdate due date?")
    if confirm("Change due date?", default=False):
        new_due_date, clear_due_date = get_due_date(allow_clear=True)
    else:
        new_due_date = None
        clear_due_date = False

    # Apply updates
    updated_task = task_store.update_task(
        task_id=task_id,
        title=new_title if new_title != task.title else None,
        description=new_description if new_description != task.description else None,
        priority=new_priority,
        status=new_status,
        due_date=new_due_date,
        clear_due_date=clear_due_date
    )

    if updated_task:
        print_success(f"Task #{task_id} updated successfully!")
        display_task(updated_task, detailed=True)


def delete_task():
    """Delete a task from the store"""
    print_header("Delete Task")

    task_id = get_int_input("Enter task ID to delete")
    if task_id is None:
        return

    task = task_store.get_task(task_id)
    if not task:
        print_error(f"Task #{task_id} not found.")
        return

    print("\nTask to delete:")
    display_task(task, detailed=True)

    if confirm("\nAre you sure you want to delete this task?", default=False):
        task_store.delete_task(task_id)
        print_success(f"Task #{task_id} deleted successfully!")
    else:
        print_info("Deletion cancelled.")


def mark_task_complete():
    """Quick action to mark a task as completed"""
    print_header("Mark Task Complete")

    task_id = get_int_input("Enter task ID to mark complete")
    if task_id is None:
        return

    task = task_store.mark_completed(task_id)
    if task:
        print_success(f"Task #{task_id} marked as completed!")
    else:
        print_error(f"Task #{task_id} not found.")


def search_tasks():
    """Search tasks by keyword"""
    print_header("Search Tasks")

    query = get_input("Enter search term")
    if not query:
        return

    results = task_store.search_tasks(query)
    display_task_list(results, f"Search Results for '{query}'")


def filter_tasks():
    """Filter tasks by status, priority, or due date"""
    print_header("Filter Tasks")

    filter_type = get_choice(
        "Filter by:",
        ["Status", "Priority", "Overdue"]
    )

    if filter_type is None:
        return

    if filter_type == 0:  # Status
        status = get_status()
        if status:
            tasks = task_store.get_tasks_by_status(status)
            display_task_list(tasks, f"Tasks with status: {status.value}")
    elif filter_type == 1:  # Priority
        priority = get_priority()
        if priority:
            tasks = task_store.get_tasks_by_priority(priority)
            display_task_list(tasks, f"Tasks with priority: {priority.value}")
    else:  # Overdue
        tasks = task_store.get_overdue_tasks()
        display_task_list(tasks, "Overdue Tasks")


def view_statistics():
    """Display task statistics"""
    stats = task_store.get_stats()
    display_stats(stats)


# ==================== AI FEATURES ====================

def ai_menu():
    """AI-powered features submenu"""
    while True:
        print_header("AI Assistant (Powered by Gemini)")

        if not gemini_service.is_available():
            print_warning("Gemini API is not configured!")
            print_info("Set GEMINI_API_KEY environment variable to enable AI features.")
            print_info("Get your API key at: https://makersuite.google.com/app/apikey")
            press_enter_to_continue()
            return

        menu_options = [
            ("1", "Get task improvement suggestions"),
            ("2", "Get priority recommendation"),
            ("3", "Break down a task"),
            ("4", "Summarize all tasks"),
            ("5", "Smart search with AI"),
            ("6", "Get daily motivation"),
            ("0", "Back to main menu")
        ]

        display_menu("AI Features", menu_options)
        choice = get_input("Select option", required=False)

        if choice == "1":
            ai_improve_task()
        elif choice == "2":
            ai_recommend_priority()
        elif choice == "3":
            ai_breakdown_task()
        elif choice == "4":
            ai_summarize_tasks()
        elif choice == "5":
            ai_smart_search()
        elif choice == "6":
            ai_motivation()
        elif choice == "0" or choice == "":
            break
        else:
            print_error("Invalid option. Please try again.")

        press_enter_to_continue()


def ai_improve_task():
    """Get AI suggestions to improve a task"""
    print_subheader("Task Improvement Suggestions")

    task_id = get_int_input("Enter task ID (or leave empty for new task)")

    if task_id:
        task = task_store.get_task(task_id)
        if not task:
            print_error(f"Task #{task_id} not found.")
            return
        title = task.title
        description = task.description
    else:
        title = get_input("Enter task title")
        description = get_input("Enter description (optional)", required=False)

    print_info("Getting AI suggestions...")
    suggestion = gemini_service.suggest_task_improvement(title, description)

    if suggestion:
        print_subheader("AI Suggestions")
        print(suggestion)
    else:
        print_error("Could not get AI suggestions. Please try again.")


def ai_recommend_priority():
    """Get AI recommendation for task priority"""
    print_subheader("Priority Recommendation")

    title = get_input("Enter task title")
    description = get_input("Enter description (optional)", required=False)

    print_info("Analyzing task...")
    recommendation = gemini_service.recommend_priority(title, description)

    if recommendation:
        print_subheader("AI Recommendation")
        print(recommendation)
    else:
        print_error("Could not get recommendation. Please try again.")


def ai_breakdown_task():
    """Break down a complex task into subtasks"""
    print_subheader("Task Breakdown")

    task_id = get_int_input("Enter task ID (or leave empty for new task)")

    if task_id:
        task = task_store.get_task(task_id)
        if not task:
            print_error(f"Task #{task_id} not found.")
            return
        title = task.title
        description = task.description
    else:
        title = get_input("Enter task title")
        description = get_input("Enter description (optional)", required=False)

    print_info("Breaking down task...")
    breakdown = gemini_service.break_down_task(title, description)

    if breakdown:
        print_subheader("Subtasks")
        print(breakdown)

        # Offer to create subtasks
        if confirm("\nWould you like to add these as new tasks?", default=False):
            print_info("You can copy these and add them manually using 'Add Task'")
    else:
        print_error("Could not break down task. Please try again.")


def ai_summarize_tasks():
    """Get AI summary of all tasks"""
    print_subheader("Task Summary")

    tasks = task_store.get_all_tasks()
    if not tasks:
        print_warning("No tasks to summarize.")
        return

    tasks_data = [task.to_dict() for task in tasks]

    print_info("Generating summary...")
    summary = gemini_service.summarize_tasks(tasks_data)

    if summary:
        print_subheader("AI Summary")
        print(summary)
    else:
        print_error("Could not generate summary. Please try again.")


def ai_smart_search():
    """Use AI to find relevant tasks"""
    print_subheader("Smart Search")

    tasks = task_store.get_all_tasks()
    if not tasks:
        print_warning("No tasks to search.")
        return

    query = get_input("What are you looking for? (natural language)")
    tasks_data = [task.to_dict() for task in tasks]

    print_info("Searching with AI...")
    result = gemini_service.smart_search_help(query, tasks_data)

    if result:
        print_subheader("Search Results")
        print(result)
    else:
        print_error("Could not perform search. Please try again.")


def ai_motivation():
    """Get a motivational message"""
    print_info("Getting your daily motivation...")
    message = gemini_service.daily_motivation()

    if message:
        print_subheader("Daily Motivation")
        print(f"\n  \"{message}\"\n")
    else:
        print_info("Stay productive and keep going! You've got this!")


# ==================== MAIN MENU ====================

def show_welcome():
    """Display welcome message"""
    clear_screen()
    print_header(f"{APP_NAME} v{APP_VERSION}")
    print(f"\n  {APP_DESCRIPTION}")
    print(f"\n  Your tasks are automatically saved to tasks.json")

    if gemini_service.is_available():
        print_info("AI features are enabled!")
    else:
        print_warning("AI features disabled. Set GEMINI_API_KEY to enable.")

    print()


def main_menu():
    """Main application menu loop"""
    show_welcome()

    while True:
        menu_options = [
            ("1", "Add new task"),
            ("2", "View all tasks"),
            ("3", "View task details"),
            ("4", "Update task"),
            ("5", "Delete task"),
            ("6", "Mark task complete"),
            ("7", "Search tasks"),
            ("8", "Filter tasks"),
            ("9", "View statistics"),
            ("A", "AI Assistant"),
            ("C", "Clear all tasks"),
            ("Q", "Quit")
        ]

        display_menu("Main Menu", menu_options)
        choice = get_input("Select option", required=False).upper()

        # Clear screen for better UX (optional)
        # clear_screen()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_task_details()
        elif choice == "4":
            update_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            mark_task_complete()
        elif choice == "7":
            search_tasks()
        elif choice == "8":
            filter_tasks()
        elif choice == "9":
            view_statistics()
        elif choice == "A":
            ai_menu()
        elif choice == "C":
            if confirm("Are you sure you want to delete ALL tasks?", default=False):
                count = task_store.clear_all()
                print_success(f"Cleared {count} task(s).")
            else:
                print_info("Operation cancelled.")
        elif choice == "Q" or choice == "":
            if confirm("Are you sure you want to quit?", default=True):
                print("\nThank you for using Task Manager Pro!")
                print("Your tasks have been saved to tasks.json\n")
                break
        else:
            print_error("Invalid option. Please try again.")

        press_enter_to_continue()


# ==================== ENTRY POINT ====================

def main():
    """Application entry point with error handling"""
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
