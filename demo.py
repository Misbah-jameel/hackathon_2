"""
demo.py - Demonstration of Hackathon 2 Task Manager

This script demonstrates all the core features without interactive input.
"""

from models import Task, Priority, Status
from store import task_store
from ui import (
    print_header, print_success, print_info,
    display_task, display_task_list, display_stats
)


def run_demo():
    """Run a complete demonstration of the Task Manager"""

    print_header("HACKATHON 2 - TASK MANAGER DEMO")
    print("\nThis demo shows all CRUD operations and features.\n")
    input("Press Enter to start the demo...")

    # ==================== CREATE ====================
    print_header("1. CREATE - Adding Tasks")

    # Add sample tasks
    task1 = task_store.add_task(
        title="Complete hackathon project",
        description="Build the in-memory task manager with AI features",
        priority=Priority.HIGH,
        tags=["hackathon", "python"]
    )
    print_success(f"Created task #{task1.id}")
    display_task(task1, detailed=True)

    task2 = task_store.add_task(
        title="Write documentation",
        description="Add README and code comments",
        priority=Priority.MEDIUM,
        tags=["docs"]
    )
    print_success(f"Created task #{task2.id}")

    task3 = task_store.add_task(
        title="Test all features",
        description="Verify CRUD operations work correctly",
        priority=Priority.HIGH,
        tags=["testing", "qa"]
    )
    print_success(f"Created task #{task3.id}")

    task4 = task_store.add_task(
        title="Code review",
        description="Review code for best practices",
        priority=Priority.LOW,
        tags=["review"]
    )
    print_success(f"Created task #{task4.id}")

    input("\nPress Enter to continue...")

    # ==================== READ ====================
    print_header("2. READ - Viewing Tasks")

    # View all tasks
    all_tasks = task_store.get_all_tasks()
    display_task_list(all_tasks, "All Tasks")

    # View single task
    print("\nViewing task #1 in detail:")
    task = task_store.get_task(1)
    display_task(task, detailed=True)

    input("\nPress Enter to continue...")

    # ==================== UPDATE ====================
    print_header("3. UPDATE - Modifying Tasks")

    # Update task status
    print("\nUpdating task #1 status to 'In Progress'...")
    task_store.update_task(1, status=Status.IN_PROGRESS)
    print_success("Task #1 updated!")

    # Update task priority
    print("\nUpdating task #2 priority to 'High'...")
    task_store.update_task(2, priority=Priority.HIGH)
    print_success("Task #2 updated!")

    # Mark task complete
    print("\nMarking task #3 as completed...")
    task_store.mark_completed(3)
    print_success("Task #3 completed!")

    # Show updated list
    display_task_list(task_store.get_all_tasks(), "Updated Tasks")

    input("\nPress Enter to continue...")

    # ==================== SEARCH & FILTER ====================
    print_header("4. SEARCH & FILTER")

    # Search
    print("\nSearching for 'code'...")
    results = task_store.search_tasks("code")
    display_task_list(results, "Search Results for 'code'")

    # Filter by status
    print("\nFiltering by status: COMPLETED...")
    completed = task_store.get_tasks_by_status(Status.COMPLETED)
    display_task_list(completed, "Completed Tasks")

    # Filter by priority
    print("\nFiltering by priority: HIGH...")
    high_priority = task_store.get_tasks_by_priority(Priority.HIGH)
    display_task_list(high_priority, "High Priority Tasks")

    input("\nPress Enter to continue...")

    # ==================== STATISTICS ====================
    print_header("5. STATISTICS")

    stats = task_store.get_stats()
    display_stats(stats)

    input("\nPress Enter to continue...")

    # ==================== DELETE ====================
    print_header("6. DELETE - Removing Tasks")

    print("\nDeleting task #4...")
    task_store.delete_task(4)
    print_success("Task #4 deleted!")

    # Show final list
    display_task_list(task_store.get_all_tasks(), "Final Task List")

    # Final stats
    print(f"\nTotal tasks remaining: {task_store.count()}")

    # ==================== DEMO COMPLETE ====================
    print_header("DEMO COMPLETE!")
    print("""
    Features demonstrated:
    [x] CREATE - Add new tasks with title, description, priority, tags
    [x] READ   - View all tasks, view single task, search, filter
    [x] UPDATE - Modify task fields, change status, mark complete
    [x] DELETE - Remove individual tasks
    [x] STATS  - View task statistics

    AI Features (requires GEMINI_API_KEY):
    [ ] Task improvement suggestions
    [ ] Priority recommendations
    [ ] Task breakdown into subtasks
    [ ] Smart search with natural language
    [ ] Task summary generation

    Run 'python main.py' for the full interactive experience!
    """)


if __name__ == "__main__":
    run_demo()
