"""
Task Manager Console Application
================================
A menu-driven console application for managing personal tasks.
Demonstrates modular design, error handling, and clean I/O.

Author: Hackathon 2 - Phase 1
"""

# =============================================================================
# DATA STORAGE (In-Memory)
# =============================================================================

# Global list to store tasks as dictionaries
# Each task: {"id": int, "title": str, "description": str, "status": str, "priority": str}
tasks = []
next_id = 1  # Auto-incrementing ID counter


def load_sample_data():
    """Load sample tasks to demonstrate application functionality.

    Creates a variety of tasks with different statuses and priorities
    to showcase all features of the task manager.
    """
    global tasks, next_id

    sample_tasks = [
        {
            "id": 1,
            "title": "Complete project proposal",
            "description": "Write and submit the Q1 project proposal document with budget estimates",
            "status": "Completed",
            "priority": "High"
        },
        {
            "id": 2,
            "title": "Review pull requests",
            "description": "Review pending PRs from team members on the main repository",
            "status": "In Progress",
            "priority": "High"
        },
        {
            "id": 3,
            "title": "Update documentation",
            "description": "Update the API documentation with new endpoints and examples",
            "status": "In Progress",
            "priority": "Medium"
        },
        {
            "id": 4,
            "title": "Fix login bug",
            "description": "Investigate and fix the authentication timeout issue reported by users",
            "status": "Pending",
            "priority": "High"
        },
        {
            "id": 5,
            "title": "Team meeting preparation",
            "description": "Prepare slides and agenda for weekly team sync meeting",
            "status": "Pending",
            "priority": "Medium"
        },
        {
            "id": 6,
            "title": "Database optimization",
            "description": "Analyze slow queries and add necessary indexes to improve performance",
            "status": "Pending",
            "priority": "Medium"
        },
        {
            "id": 7,
            "title": "Write unit tests",
            "description": "Add unit tests for the new payment processing module",
            "status": "Pending",
            "priority": "Low"
        },
        {
            "id": 8,
            "title": "Organize code repository",
            "description": "Clean up unused branches and update README files",
            "status": "Completed",
            "priority": "Low"
        }
    ]

    tasks = sample_tasks
    next_id = len(sample_tasks) + 1


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_screen():
    """Print empty lines to simulate screen clearing (cross-platform)."""
    print("\n" * 2)


def print_header(title):
    """Display a formatted header for sections.

    Args:
        title: The header text to display
    """
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_separator():
    """Print a visual separator line."""
    print("-" * 50)


def get_valid_input(prompt, valid_options=None, allow_empty=False):
    """Get validated input from user.

    Args:
        prompt: The message to display to the user
        valid_options: List of acceptable inputs (None = any input)
        allow_empty: Whether empty input is acceptable

    Returns:
        The validated user input string
    """
    while True:
        user_input = input(prompt).strip()

        # Check for empty input
        if not user_input and not allow_empty:
            print("  [!] Input cannot be empty. Please try again.")
            continue

        # Check against valid options if provided
        if valid_options and user_input.lower() not in [opt.lower() for opt in valid_options]:
            print(f"  [!] Invalid option. Choose from: {', '.join(valid_options)}")
            continue

        return user_input


def get_integer_input(prompt, min_val=None, max_val=None):
    """Get validated integer input from user.

    Args:
        prompt: The message to display to the user
        min_val: Minimum acceptable value (inclusive)
        max_val: Maximum acceptable value (inclusive)

    Returns:
        The validated integer, or None if user cancels
    """
    while True:
        user_input = input(prompt).strip()

        # Allow user to cancel/go back
        if user_input.lower() in ['', 'q', 'quit', 'cancel']:
            return None

        try:
            value = int(user_input)

            # Validate range
            if min_val is not None and value < min_val:
                print(f"  [!] Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  [!] Value must be at most {max_val}.")
                continue

            return value

        except ValueError:
            print("  [!] Please enter a valid number.")


def find_task_by_id(task_id):
    """Find a task by its ID.

    Args:
        task_id: The ID of the task to find

    Returns:
        The task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def format_task(task, detailed=False):
    """Format a task for display.

    Args:
        task: The task dictionary to format
        detailed: Whether to show full details

    Returns:
        Formatted string representation of the task
    """
    status_icon = {"Pending": "[ ]", "In Progress": "[~]", "Completed": "[X]"}
    priority_indicator = {"High": "!!!", "Medium": "!!", "Low": "!"}

    icon = status_icon.get(task["status"], "[ ]")
    priority = priority_indicator.get(task["priority"], "!")

    if detailed:
        return (
            f"\n  ID: {task['id']}\n"
            f"  Title: {task['title']}\n"
            f"  Description: {task['description']}\n"
            f"  Status: {task['status']}\n"
            f"  Priority: {task['priority']}"
        )
    else:
        return f"  {icon} #{task['id']:03d} {priority} {task['title']} ({task['status']})"


# =============================================================================
# CORE TASK OPERATIONS
# =============================================================================

def add_task():
    """Add a new task to the system.

    Collects task information from user and creates a new task entry.
    """
    global next_id

    print_header("ADD NEW TASK")
    print("  Enter task details (or 'q' to cancel)\n")

    # Get task title
    title = input("  Title: ").strip()
    if title.lower() == 'q' or not title:
        if not title:
            print("  [!] Title cannot be empty. Task not created.")
        else:
            print("  [i] Task creation cancelled.")
        return

    # Get task description
    description = input("  Description: ").strip()
    if not description:
        description = "No description provided"

    # Get priority level
    print("\n  Priority Levels: High, Medium, Low")
    priority = get_valid_input("  Priority: ", ["High", "Medium", "Low", "H", "M", "L"])

    # Normalize priority input
    priority_map = {"h": "High", "m": "Medium", "l": "Low"}
    priority = priority_map.get(priority.lower(), priority.capitalize())

    # Create the task
    new_task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "Pending",
        "priority": priority
    }

    tasks.append(new_task)
    next_id += 1

    print_separator()
    print(f"  [+] Task #{new_task['id']} created successfully!")


def view_all_tasks():
    """Display all tasks in the system.

    Shows a summary list of all tasks with their status and priority.
    """
    print_header("ALL TASKS")

    if not tasks:
        print("  No tasks found. Add a task to get started!")
        return

    print(f"  Total Tasks: {len(tasks)}\n")
    print("  Legend: [ ] Pending  [~] In Progress  [X] Completed")
    print("          !!! High  !! Medium  ! Low")
    print_separator()

    for task in tasks:
        print(format_task(task))

    print_separator()

    # Show summary statistics
    pending = sum(1 for t in tasks if t["status"] == "Pending")
    in_progress = sum(1 for t in tasks if t["status"] == "In Progress")
    completed = sum(1 for t in tasks if t["status"] == "Completed")

    print(f"  Summary: {pending} Pending | {in_progress} In Progress | {completed} Completed")


def view_task_details():
    """View detailed information about a specific task.

    Prompts user for task ID and displays full task details.
    """
    print_header("VIEW TASK DETAILS")

    if not tasks:
        print("  No tasks available to view.")
        return

    # Show available task IDs
    print("  Available Task IDs:", ", ".join(str(t["id"]) for t in tasks))
    print()

    task_id = get_integer_input("  Enter Task ID (or 'q' to cancel): ")

    if task_id is None:
        print("  [i] View cancelled.")
        return

    task = find_task_by_id(task_id)

    if task:
        print_separator()
        print(format_task(task, detailed=True))
        print_separator()
    else:
        print(f"  [!] Task #{task_id} not found.")


def update_task():
    """Update an existing task's information.

    Allows modification of title, description, status, or priority.
    """
    print_header("UPDATE TASK")

    if not tasks:
        print("  No tasks available to update.")
        return

    # Show available tasks
    print("  Available Tasks:")
    for task in tasks:
        print(format_task(task))
    print()

    task_id = get_integer_input("  Enter Task ID to update (or 'q' to cancel): ")

    if task_id is None:
        print("  [i] Update cancelled.")
        return

    task = find_task_by_id(task_id)

    if not task:
        print(f"  [!] Task #{task_id} not found.")
        return

    print(f"\n  Updating Task: {task['title']}")
    print("  Press Enter to keep current value\n")

    # Update title
    new_title = input(f"  Title [{task['title']}]: ").strip()
    if new_title:
        task["title"] = new_title

    # Update description
    new_desc = input(f"  Description [{task['description'][:30]}...]: ").strip()
    if new_desc:
        task["description"] = new_desc

    # Update status
    print(f"\n  Current Status: {task['status']}")
    print("  Options: Pending, In Progress, Completed")
    new_status = input("  New Status: ").strip()
    if new_status:
        status_map = {
            "pending": "Pending",
            "in progress": "In Progress",
            "inprogress": "In Progress",
            "completed": "Completed",
            "done": "Completed"
        }
        normalized = status_map.get(new_status.lower(), new_status.title())
        if normalized in ["Pending", "In Progress", "Completed"]:
            task["status"] = normalized
        else:
            print("  [!] Invalid status. Status not changed.")

    # Update priority
    print(f"\n  Current Priority: {task['priority']}")
    print("  Options: High, Medium, Low")
    new_priority = input("  New Priority: ").strip()
    if new_priority:
        priority_map = {"h": "High", "m": "Medium", "l": "Low"}
        normalized = priority_map.get(new_priority.lower(), new_priority.capitalize())
        if normalized in ["High", "Medium", "Low"]:
            task["priority"] = normalized
        else:
            print("  [!] Invalid priority. Priority not changed.")

    print_separator()
    print(f"  [+] Task #{task_id} updated successfully!")


def delete_task():
    """Delete a task from the system.

    Prompts for confirmation before permanent deletion.
    """
    print_header("DELETE TASK")

    if not tasks:
        print("  No tasks available to delete.")
        return

    # Show available tasks
    print("  Available Tasks:")
    for task in tasks:
        print(format_task(task))
    print()

    task_id = get_integer_input("  Enter Task ID to delete (or 'q' to cancel): ")

    if task_id is None:
        print("  [i] Deletion cancelled.")
        return

    task = find_task_by_id(task_id)

    if not task:
        print(f"  [!] Task #{task_id} not found.")
        return

    # Confirm deletion
    print(f"\n  Task to delete: {task['title']}")
    confirm = input("  Are you sure? (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        tasks.remove(task)
        print_separator()
        print(f"  [-] Task #{task_id} deleted successfully!")
    else:
        print("  [i] Deletion cancelled.")


def search_tasks():
    """Search tasks by title or description.

    Performs case-insensitive search across task titles and descriptions.
    """
    print_header("SEARCH TASKS")

    if not tasks:
        print("  No tasks available to search.")
        return

    search_term = input("  Enter search term: ").strip().lower()

    if not search_term:
        print("  [!] Search term cannot be empty.")
        return

    # Search in title and description
    results = []
    for task in tasks:
        if (search_term in task["title"].lower() or
            search_term in task["description"].lower()):
            results.append(task)

    print_separator()

    if results:
        print(f"  Found {len(results)} matching task(s):\n")
        for task in results:
            print(format_task(task))
    else:
        print(f"  No tasks found matching '{search_term}'")


def filter_by_status():
    """Filter and display tasks by their status.

    Allows user to view only Pending, In Progress, or Completed tasks.
    """
    print_header("FILTER BY STATUS")

    if not tasks:
        print("  No tasks available to filter.")
        return

    print("  Status Options:")
    print("    1. Pending")
    print("    2. In Progress")
    print("    3. Completed")
    print()

    choice = get_valid_input("  Select status (1-3): ", ["1", "2", "3"])

    status_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
    selected_status = status_map[choice]

    filtered = [t for t in tasks if t["status"] == selected_status]

    print_separator()
    print(f"  Tasks with status '{selected_status}': {len(filtered)}\n")

    if filtered:
        for task in filtered:
            print(format_task(task))
    else:
        print(f"  No tasks with status '{selected_status}'")


def filter_by_priority():
    """Filter and display tasks by their priority level.

    Allows user to view only High, Medium, or Low priority tasks.
    """
    print_header("FILTER BY PRIORITY")

    if not tasks:
        print("  No tasks available to filter.")
        return

    print("  Priority Options:")
    print("    1. High")
    print("    2. Medium")
    print("    3. Low")
    print()

    choice = get_valid_input("  Select priority (1-3): ", ["1", "2", "3"])

    priority_map = {"1": "High", "2": "Medium", "3": "Low"}
    selected_priority = priority_map[choice]

    filtered = [t for t in tasks if t["priority"] == selected_priority]

    print_separator()
    print(f"  Tasks with '{selected_priority}' priority: {len(filtered)}\n")

    if filtered:
        for task in filtered:
            print(format_task(task))
    else:
        print(f"  No tasks with '{selected_priority}' priority")


# =============================================================================
# MENU SYSTEM
# =============================================================================

def display_main_menu():
    """Display the main menu options.

    Returns:
        None (prints menu to console)
    """
    print_header("TASK MANAGER - MAIN MENU")
    print("""
    1. Add New Task
    2. View All Tasks
    3. View Task Details
    4. Update Task
    5. Delete Task
    6. Search Tasks
    7. Filter by Status
    8. Filter by Priority
    9. Exit
    """)


def main():
    """Main application entry point.

    Runs the main menu loop and dispatches to appropriate functions.
    """
    # Load sample data for demonstration
    load_sample_data()

    print("\n" + "=" * 50)
    print("    WELCOME TO TASK MANAGER")
    print("    Your Personal Productivity Assistant")
    print("=" * 50)
    print("\n  [i] 8 sample tasks loaded for demonstration")

    # Menu action mapping
    menu_actions = {
        "1": add_task,
        "2": view_all_tasks,
        "3": view_task_details,
        "4": update_task,
        "5": delete_task,
        "6": search_tasks,
        "7": filter_by_status,
        "8": filter_by_priority,
    }

    while True:
        display_main_menu()

        choice = input("  Enter your choice (1-9): ").strip()

        if choice == "9":
            print_header("GOODBYE!")
            print("  Thank you for using Task Manager.")
            print("  Have a productive day!")
            print_separator()
            break

        if choice in menu_actions:
            try:
                menu_actions[choice]()
            except KeyboardInterrupt:
                print("\n  [i] Operation cancelled.")
            except Exception as e:
                print(f"\n  [!] An error occurred: {e}")
                print("  [i] Please try again.")
        else:
            print("\n  [!] Invalid choice. Please enter a number between 1-9.")

        input("\n  Press Enter to continue...")
        clear_screen()


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [!] Program terminated by user.")
        print("  Goodbye!")
