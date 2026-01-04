"""
gemini_service.py - Gemini LLM Integration for Hackathon 2

This module handles all AI-related functionality using Google's Gemini API.
Provides intelligent assistance for task management.
"""

import os
from typing import List, Optional

# Try to import google generative AI, handle if not installed
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Note: google-generativeai not installed. AI features will be limited.")
    print("Install with: pip install google-generativeai")


class GeminiService:
    """
    Service class for Gemini LLM interactions.

    Provides AI-powered features for the task manager:
    - Task suggestions and improvements
    - Priority recommendations
    - Task summaries
    - Smart task breakdown
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini service.

        Args:
            api_key: Gemini API key. If not provided, tries to read from
                     GEMINI_API_KEY environment variable.
        """
        self.is_configured = False
        self.model = None

        if not GEMINI_AVAILABLE:
            return

        # Get API key from parameter or environment
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Using gemini-1.5-flash for fast responses
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                self.is_configured = True
            except Exception as e:
                print(f"Warning: Could not configure Gemini: {e}")

    def is_available(self) -> bool:
        """Check if Gemini service is available and configured"""
        return self.is_configured and self.model is not None

    def _generate(self, prompt: str) -> Optional[str]:
        """
        Internal method to generate response from Gemini.

        Args:
            prompt: The prompt to send to Gemini

        Returns:
            Generated text response or None if failed
        """
        if not self.is_available():
            return None

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None

    # ==================== AI FEATURES ====================

    def suggest_task_improvement(self, title: str, description: str = "") -> Optional[str]:
        """
        Get AI suggestions to improve a task's clarity and actionability.

        Args:
            title: Current task title
            description: Current task description

        Returns:
            Suggestions for improving the task, or None if unavailable
        """
        prompt = f"""You are a productivity expert. Analyze this task and provide brief, actionable suggestions to make it clearer and more achievable.

Task Title: {title}
Description: {description if description else "No description provided"}

Provide 2-3 short suggestions to improve this task. Keep your response under 100 words."""

        return self._generate(prompt)

    def recommend_priority(self, title: str, description: str = "") -> Optional[str]:
        """
        Get AI recommendation for task priority.

        Args:
            title: Task title
            description: Task description

        Returns:
            Priority recommendation with reasoning, or None if unavailable
        """
        prompt = f"""You are a productivity expert. Based on this task, recommend a priority level.

Task Title: {title}
Description: {description if description else "No description provided"}

Respond with one of: HIGH, MEDIUM, or LOW
Then provide a one-sentence reason why. Keep total response under 50 words."""

        return self._generate(prompt)

    def break_down_task(self, title: str, description: str = "") -> Optional[str]:
        """
        Break down a complex task into smaller subtasks.

        Args:
            title: Task title
            description: Task description

        Returns:
            List of subtasks, or None if unavailable
        """
        prompt = f"""You are a productivity expert. Break down this task into 3-5 smaller, actionable subtasks.

Task Title: {title}
Description: {description if description else "No description provided"}

List each subtask on a new line with a bullet point. Keep each subtask concise (under 10 words)."""

        return self._generate(prompt)

    def summarize_tasks(self, tasks_data: List[dict]) -> Optional[str]:
        """
        Generate a summary of all tasks.

        Args:
            tasks_data: List of task dictionaries

        Returns:
            Summary of tasks and productivity insights, or None if unavailable
        """
        if not tasks_data:
            return "No tasks to summarize."

        tasks_text = "\n".join([
            f"- {t['title']} (Priority: {t['priority']}, Status: {t['status']})"
            for t in tasks_data
        ])

        prompt = f"""You are a productivity assistant. Summarize these tasks and provide brief insights.

Tasks:
{tasks_text}

Provide:
1. A one-sentence overview
2. What to focus on first
3. One productivity tip

Keep total response under 100 words."""

        return self._generate(prompt)

    def smart_search_help(self, query: str, tasks_data: List[dict]) -> Optional[str]:
        """
        Help user find relevant tasks based on natural language query.

        Args:
            query: User's natural language query
            tasks_data: List of all tasks

        Returns:
            AI interpretation and matching task suggestions
        """
        if not tasks_data:
            return "No tasks available to search."

        tasks_text = "\n".join([
            f"[{t['id']}] {t['title']} - {t['description'][:50] if t['description'] else 'No description'}"
            for t in tasks_data
        ])

        prompt = f"""Given these tasks:
{tasks_text}

User query: "{query}"

Which task IDs are most relevant to this query? List the IDs and briefly explain why. Keep response under 50 words."""

        return self._generate(prompt)

    def daily_motivation(self) -> Optional[str]:
        """
        Generate a short motivational message for productivity.

        Returns:
            Motivational message, or None if unavailable
        """
        prompt = """Generate a short, unique motivational quote about productivity and task management. Keep it under 20 words. Be encouraging but not cheesy."""

        return self._generate(prompt)


# Create a global service instance
gemini_service = GeminiService()
