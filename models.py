"""
models.py - Data Models for Hackathon 2 Task Manager

This module defines the data structures used in the application.
Uses dataclasses for clean, readable model definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    """Task status options"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """
    Task model representing a single task item.

    Attributes:
        id: Unique identifier for the task
        title: Short title/name of the task
        description: Detailed description of what needs to be done
        priority: Task priority level (low, medium, high)
        status: Current status of the task
        due_date: Optional deadline for the task
        created_at: Timestamp when task was created
        updated_at: Timestamp of last update
        tags: List of tags for categorization
    """
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert task to dictionary for display/AI processing"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
            "tags": self.tags
        }

    def __str__(self) -> str:
        """Human-readable string representation"""
        status_emoji = {
            Status.PENDING: "⏳",
            Status.IN_PROGRESS: "🔄",
            Status.COMPLETED: "✅"
        }
        priority_emoji = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🔴"
        }
        return (
            f"[{self.id}] {status_emoji[self.status]} {self.title} "
            f"{priority_emoji[self.priority]} ({self.priority.value})"
        )
