"""
ui.py - Console UI Utilities for Hackathon 2

This module provides helper functions for console-based user interaction.
Handles display formatting, input validation, and menu rendering.
"""

from typing import Optional, List, Callable
from datetime import datetime, date
from models import Task, Priority, Status


# ==================== DISPLAY HELPERS ====================

def clear_screen():
    """Clear the console screen (cross-platform)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str, char: str = "="):
    """
    Print a formatted header with decorative borders.

    Args:
        text: Header text to display
        char: Character to use for border (default: =)
    """
    width = max(50, len(text) + 4)
    border = char * width
    print(f"\n{border}")
    print(f"  {text}")
    print(f"{border}")


def print_subheader(text: str):
    """Print a smaller subheader"""
    print(f"\n--- {text} ---")


def print_success(message: str):
    """Print a success message with green indicator"""
    print(f"[SUCCESS] {message}")


def print_error(message: str):
    """Print an error message with red indicator"""
    print(f"[ERROR] {message}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"[WARNING] {message}")


def print_info(message: str):
    """Print an info message"""
    print(f"[INFO] {message}")


# ==================== TASK DISPLAY ====================

def format_due_date(due_date: Optional[datetime]) -> str:
    """Format due date with overdue indicator"""
    if not due_date:
        return "None"

    today = date.today()
    due = due_date.date()
    formatted = due_date.strftime('%Y-%m-%d')

    if due < today:
        return f"{formatted} (OVERDUE)"
    elif due == today:
        return f"{formatted} (TODAY)"
    else:
        days_left = (due - today).days
        if days_left == 1:
            return f"{formatted} (tomorrow)"
        elif days_left <= 7:
            return f"{formatted} ({days_left} days left)"
        return formatted


def display_task(task: Task, detailed: bool = False):
    """
    Display a single task.

    Args:
        task: Task object to display
        detailed: If True, show all details; if False, show summary
    """
    if detailed:
        print(f"\n{'='*50}")
        print(f"  Task #{task.id}")
        print(f"{'='*50}")
        print(f"  Title:       {task.title}")
        print(f"  Description: {task.description or 'None'}")
        print(f"  Priority:    {task.priority.value.upper()}")
        print(f"  Status:      {task.status.value.replace('_', ' ').title()}")
        print(f"  Due Date:    {format_due_date(task.due_date)}")
        print(f"  Tags:        {', '.join(task.tags) if task.tags else 'None'}")
        print(f"  Created:     {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Updated:     {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*50}")
    else:
        print(f"  {task}")


def display_task_list(tasks: List[Task], title: str = "Tasks"):
    """
    Display a list of tasks in a formatted table.

    Args:
        tasks: List of Task objects
        title: Title for the list
    """
    print_subheader(title)

    if not tasks:
        print("  No tasks found.")
        return

    # Print table header
    print(f"\n  {'ID':<5} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Title':<25}")
    print(f"  {'-'*5} {'-'*12} {'-'*10} {'-'*12} {'-'*25}")

    # Print each task
    for task in tasks:
        status_display = task.status.value.replace('_', ' ').title()
        title_display = task.title[:23] + ".." if len(task.title) > 25 else task.title
        due_display = task.due_date.strftime('%Y-%m-%d') if task.due_date else '-'
        print(f"  {task.id:<5} {status_display:<12} {task.priority.value:<10} {due_display:<12} {title_display:<25}")

    print(f"\n  Total: {len(tasks)} task(s)")


def display_stats(stats: dict):
    """Display task statistics"""
    print_subheader("Task Statistics")

    print(f"\n  Total Tasks: {stats['total']}")
    overdue = stats.get('overdue', 0)
    if overdue > 0:
        print(f"  Overdue:     {overdue} [!]")
    else:
        print(f"  Overdue:     {overdue}")

    print("\n  By Status:")
    print(f"    Pending:     {stats['by_status']['pending']}")
    print(f"    In Progress: {stats['by_status']['in_progress']}")
    print(f"    Completed:   {stats['by_status']['completed']}")

    print("\n  By Priority:")
    print(f"    High:   {stats['by_priority']['high']}")
    print(f"    Medium: {stats['by_priority']['medium']}")
    print(f"    Low:    {stats['by_priority']['low']}")


# ==================== INPUT HELPERS ====================

def get_input(prompt: str, required: bool = True, default: str = "") -> str:
    """
    Get string input from user with validation.

    Args:
        prompt: Prompt to display
        required: If True, empty input is not allowed
        default: Default value if input is empty

    Returns:
        User input string
    """
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()

        if user_input or not required:
            return user_input

        print_error("This field is required. Please enter a value.")


def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    """
    Get integer input from user with optional range validation.

    Args:
        prompt: Prompt to display
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)

    Returns:
        Integer value or None if user cancels
    """
    while True:
        user_input = input(f"{prompt}: ").strip()

        if not user_input:
            return None

        try:
            value = int(user_input)

            if min_val is not None and value < min_val:
                print_error(f"Value must be at least {min_val}")
                continue

            if max_val is not None and value > max_val:
                print_error(f"Value must be at most {max_val}")
                continue

            return value

        except ValueError:
            print_error("Please enter a valid number")


def get_choice(prompt: str, options: List[str], allow_cancel: bool = True) -> Optional[int]:
    """
    Display numbered options and get user's choice.

    Args:
        prompt: Question/prompt to display
        options: List of option strings
        allow_cancel: If True, allow user to enter 0 to cancel

    Returns:
        Index of chosen option (0-based) or None if cancelled
    """
    print(f"\n{prompt}")

    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    if allow_cancel:
        print(f"  0. Cancel")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))

            if allow_cancel and choice == 0:
                return None

            if 1 <= choice <= len(options):
                return choice - 1  # Return 0-based index

            print_error(f"Please enter a number between {0 if allow_cancel else 1} and {len(options)}")

        except ValueError:
            print_error("Please enter a valid number")


def get_priority() -> Optional[Priority]:
    """Get priority selection from user"""
    options = ["Low", "Medium", "High"]
    choice = get_choice("Select priority:", options)

    if choice is None:
        return None

    return [Priority.LOW, Priority.MEDIUM, Priority.HIGH][choice]


def get_status() -> Optional[Status]:
    """Get status selection from user"""
    options = ["Pending", "In Progress", "Completed"]
    choice = get_choice("Select status:", options)

    if choice is None:
        return None

    return [Status.PENDING, Status.IN_PROGRESS, Status.COMPLETED][choice]


def get_due_date(allow_clear: bool = False) -> tuple[Optional[datetime], bool]:
    """
    Get due date input from user.

    Args:
        allow_clear: If True, allows user to clear an existing due date

    Returns:
        Tuple of (due_date, should_clear). due_date is None if not provided or cleared.
    """
    print("\nEnter due date (YYYY-MM-DD format)")
    if allow_clear:
        print("  Leave empty to keep current, or enter 'clear' to remove due date")
    else:
        print("  Leave empty to skip")

    while True:
        user_input = input("Due date: ").strip()

        if not user_input:
            return (None, False)

        if allow_clear and user_input.lower() == 'clear':
            return (None, True)

        try:
            due_date = datetime.strptime(user_input, "%Y-%m-%d")
            return (due_date, False)
        except ValueError:
            print_error("Invalid date format. Please use YYYY-MM-DD (e.g., 2024-12-31)")


def confirm(prompt: str, default: bool = False) -> bool:
    """
    Ask user for yes/no confirmation.

    Args:
        prompt: Question to ask
        default: Default value if user just presses Enter

    Returns:
        True for yes, False for no
    """
    default_hint = "[Y/n]" if default else "[y/N]"
    response = input(f"{prompt} {default_hint}: ").strip().lower()

    if not response:
        return default

    return response in ('y', 'yes')


def press_enter_to_continue():
    """Pause and wait for user to press Enter"""
    input("\nPress Enter to continue...")


# ==================== MENU HELPERS ====================

def display_menu(title: str, options: List[tuple]):
    """
    Display a formatted menu.

    Args:
        title: Menu title
        options: List of (key, description) tuples
    """
    print_header(title)
    print()

    for key, description in options:
        print(f"  [{key}] {description}")

    print()
