"""
store.py - Persistent Data Store for Hackathon 2

This module manages data storage and CRUD operations.
Data is persisted to a JSON file and survives program restarts.
"""

import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from models import Task, Priority, Status


# Default file path for task storage
DEFAULT_STORAGE_FILE = Path(__file__).parent / "tasks.json"


class TaskStore:
    """
    Persistent storage manager for tasks.

    Tasks are saved to a JSON file and automatically loaded on startup.
    """

    def __init__(self, storage_file: Path = None):
        """Initialize task store and load existing tasks from file"""
        self._tasks: dict[int, Task] = {}  # Dictionary to store tasks by ID
        self._next_id: int = 1  # Auto-incrementing ID counter
        self._storage_file: Path = storage_file or DEFAULT_STORAGE_FILE

        # Load existing tasks from file
        self._load_from_file()

    # ==================== CREATE ====================

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        tags: list = None,
        due_date: datetime = None
    ) -> Task:
        """
        Create a new task and add it to the store.

        Args:
            title: Task title (required)
            description: Task description (optional)
            priority: Task priority level (default: MEDIUM)
            tags: List of tags (optional)
            due_date: Task deadline (optional)

        Returns:
            The newly created Task object
        """
        # Create new task with auto-generated ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags or []
        )

        # Store task and increment ID counter
        self._tasks[self._next_id] = task
        self._next_id += 1

        # Persist to file
        self._save_to_file()

        return task

    # ==================== READ ====================

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a single task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the store.

        Returns:
            List of all Task objects
        """
        return list(self._tasks.values())

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """
        Filter tasks by their status.

        Args:
            status: The status to filter by

        Returns:
            List of tasks matching the status
        """
        return [task for task in self._tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """
        Filter tasks by their priority level.

        Args:
            priority: The priority to filter by

        Returns:
            List of tasks matching the priority
        """
        return [task for task in self._tasks.values() if task.priority == priority]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            query: Search string to match against title/description

        Returns:
            List of tasks matching the search query
        """
        query_lower = query.lower()
        return [
            task for task in self._tasks.values()
            if query_lower in task.title.lower() or query_lower in task.description.lower()
        ]

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are past their due date and not completed.

        Returns:
            List of overdue tasks
        """
        from datetime import date
        today = date.today()
        return [
            task for task in self._tasks.values()
            if task.due_date
            and task.due_date.date() < today
            and task.status != Status.COMPLETED
        ]

    def get_tasks_due_this_week(self) -> List[Task]:
        """
        Get all tasks due within the next 7 days (including today).

        Returns:
            List of tasks due this week
        """
        from datetime import date, timedelta
        today = date.today()
        week_end = today + timedelta(days=7)
        return [
            task for task in self._tasks.values()
            if task.due_date
            and today <= task.due_date.date() <= week_end
            and task.status != Status.COMPLETED
        ]

    # ==================== UPDATE ====================

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        status: Optional[Status] = None,
        due_date: Optional[datetime] = None,
        clear_due_date: bool = False,
        tags: Optional[list] = None
    ) -> Optional[Task]:
        """
        Update an existing task with new values.

        Only provided fields will be updated; others remain unchanged.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            status: New status (optional)
            due_date: New due date (optional)
            clear_due_date: If True, removes the due date
            tags: New tags list (optional)

        Returns:
            Updated Task object if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Update only provided fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if status is not None:
            task.status = status
        if clear_due_date:
            task.due_date = None
        elif due_date is not None:
            task.due_date = due_date
        if tags is not None:
            task.tags = tags

        # Update timestamp
        task.updated_at = datetime.now()

        # Persist to file
        self._save_to_file()

        return task

    def mark_completed(self, task_id: int) -> Optional[Task]:
        """
        Quick method to mark a task as completed.

        Args:
            task_id: ID of the task to complete

        Returns:
            Updated Task object if found, None otherwise
        """
        return self.update_task(task_id, status=Status.COMPLETED)

    # ==================== DELETE ====================

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the store.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save_to_file()
            return True
        return False

    def clear_all(self) -> int:
        """
        Remove all tasks from the store.

        Returns:
            Number of tasks that were deleted
        """
        count = len(self._tasks)
        self._tasks.clear()
        self._save_to_file()
        return count

    # ==================== UTILITY ====================

    def count(self) -> int:
        """Return the total number of tasks"""
        return len(self._tasks)

    def get_stats(self) -> dict:
        """
        Get statistics about tasks in the store.

        Returns:
            Dictionary with task counts by status and priority
        """
        tasks = self.get_all_tasks()
        return {
            "total": len(tasks),
            "overdue": len(self.get_overdue_tasks()),
            "by_status": {
                "pending": len([t for t in tasks if t.status == Status.PENDING]),
                "in_progress": len([t for t in tasks if t.status == Status.IN_PROGRESS]),
                "completed": len([t for t in tasks if t.status == Status.COMPLETED])
            },
            "by_priority": {
                "high": len([t for t in tasks if t.priority == Priority.HIGH]),
                "medium": len([t for t in tasks if t.priority == Priority.MEDIUM]),
                "low": len([t for t in tasks if t.priority == Priority.LOW])
            }
        }


    # ==================== PERSISTENCE ====================

    def _save_to_file(self):
        """Save all tasks to the JSON file"""
        data = {
            "next_id": self._next_id,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "tags": task.tags
                }
                for task in self._tasks.values()
            ]
        }
        with open(self._storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_from_file(self):
        """Load tasks from the JSON file if it exists"""
        if not self._storage_file.exists():
            return

        try:
            with open(self._storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._next_id = data.get("next_id", 1)

            for task_data in data.get("tasks", []):
                due_date_str = task_data.get("due_date")
                task = Task(
                    id=task_data["id"],
                    title=task_data["title"],
                    description=task_data.get("description", ""),
                    priority=Priority(task_data["priority"]),
                    status=Status(task_data["status"]),
                    due_date=datetime.fromisoformat(due_date_str) if due_date_str else None,
                    created_at=datetime.fromisoformat(task_data["created_at"]),
                    updated_at=datetime.fromisoformat(task_data["updated_at"]),
                    tags=task_data.get("tags", [])
                )
                self._tasks[task.id] = task
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Could not load tasks from file: {e}")
            # Start fresh if file is corrupted
            self._tasks = {}
            self._next_id = 1


# Create a global store instance for the application
task_store = TaskStore()
