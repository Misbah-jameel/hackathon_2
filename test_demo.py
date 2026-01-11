"""Quick test script to demonstrate Task Manager functionality."""

# Import everything from task_manager
from task_manager import (
    load_sample_data,
    view_all_tasks,
    view_task_details,
    search_tasks,
    filter_by_status,
    tasks,
    print_header,
    print_separator,
    format_task
)

# Load sample data
load_sample_data()

# Show welcome message
print("\n" + "=" * 50)
print("    WELCOME TO TASK MANAGER")
print("    Your Personal Productivity Assistant")
print("=" * 50)
print("\n  [i] 8 sample tasks loaded for demonstration")

# Demonstrate View All Tasks
print_header("ALL TASKS")
print(f"  Total Tasks: {len(tasks)}\n")
print("  Legend: [ ] Pending  [~] In Progress  [X] Completed")
print("          !!! High  !! Medium  ! Low")
print_separator()

for task in tasks:
    print(format_task(task))

print_separator()

# Show summary
pending = sum(1 for t in tasks if t["status"] == "Pending")
in_progress = sum(1 for t in tasks if t["status"] == "In Progress")
completed = sum(1 for t in tasks if t["status"] == "Completed")
print(f"  Summary: {pending} Pending | {in_progress} In Progress | {completed} Completed")

# Show detailed view of one task
print_header("VIEW TASK DETAILS (Task #4)")
task = tasks[3]  # Fix login bug
print(format_task(task, detailed=True))
print_separator()

print("\n  [i] Demo complete! Run 'python task_manager.py' for interactive mode.")

