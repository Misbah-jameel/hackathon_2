# Project Constitution

## Task Manager Pro - Complete Project Overview

---

## 1. Project Identity

**Name:** Task Manager Pro
**Version:** 1.0.0
**Type:** AI-Powered Task Management Console Application
**License:** MIT
**Repository:** https://github.com/Misbah-jameel/hackathon_2

---

## 2. Purpose and Mission

Task Manager Pro is a Python-based productivity tool designed to help users efficiently manage tasks through a menu-driven console interface. The application combines traditional task management with AI-powered features via Google Gemini integration.

**Core Mission:**
- Provide a lightweight, offline-capable task management solution
- Enable comprehensive CRUD operations for tasks
- Organize tasks using priority levels, status tracking, tags, and due dates
- Integrate intelligent AI assistance for enhanced productivity
- Deliver a cross-platform console application

---

## 3. Project Structure

```
hackathon_2/
├── Core Application
│   ├── main.py              # Entry point and menu system
│   ├── models.py            # Data models (Task, Priority, Status)
│   ├── store.py             # Persistence and CRUD operations
│   ├── ui.py                # Console UI utilities
│   └── gemini_service.py    # AI integration service
│
├── Data
│   ├── tasks.json           # Persistent task storage
│   └── requirements.txt     # Dependencies
│
├── Documentation
│   ├── README.md            # User documentation
│   ├── HISTORY.md           # Project history
│   ├── CONSTITUTION.md      # This file
│   └── LICENSE              # MIT License
│
├── Demo & Testing
│   ├── demo.py              # Feature demonstration
│   └── test_demo.py         # Test scripts
│
└── Configuration
    ├── .specify/            # Specification framework
    └── .claude/             # Development commands
```

---

## 4. Architecture

### 4.1 Design Principles

1. **Separation of Concerns** - Each module has a single responsibility
2. **Graceful Degradation** - Core features work without external dependencies
3. **Data Integrity** - Automatic persistence after every operation
4. **User Experience** - Input validation and clear feedback at every step
5. **Extensibility** - Clean interfaces for future enhancements

### 4.2 Module Responsibilities

| Module | Purpose |
|--------|---------|
| `models.py` | Define data structures (Task dataclass, Priority/Status enums) |
| `store.py` | Handle all CRUD operations and JSON persistence |
| `ui.py` | Manage console display, formatting, and user input |
| `main.py` | Orchestrate application flow and menu navigation |
| `gemini_service.py` | Encapsulate all AI interactions |

### 4.3 Data Flow

```
User Input → Validation (UI) → Business Logic (Store) →
Persistence (JSON) → Display (UI) → User Output
```

---

## 5. Features

### 5.1 Core Features

**Task Management:**
- Create tasks with title, description, priority, due date, and tags
- View all tasks or individual task details
- Update any task attribute
- Delete individual tasks or clear all

**Task Attributes:**
- Title (required)
- Description (optional)
- Priority: Low, Medium, High
- Status: Pending, In Progress, Completed
- Due Date with overdue detection
- Tags (multiple, comma-separated)
- Timestamps: Created at, Updated at

**Search and Filter:**
- Keyword search across title and description
- Filter by status
- Filter by priority
- Filter for overdue tasks

**Statistics:**
- Total task count
- Status breakdown
- Priority breakdown
- Overdue task count

### 5.2 AI Features (Gemini Integration)

1. **Task Improvement Suggestions** - Analyzes tasks and suggests improvements
2. **Priority Recommendations** - AI-suggested priority levels with reasoning
3. **Task Breakdown** - Decomposes complex tasks into subtasks
4. **Task Summarization** - Overview of all tasks with focus recommendations
5. **Smart Search** - Natural language query matching
6. **Daily Motivation** - Productivity quotes and encouragement

---

## 6. Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| AI Service | Google Generative AI (Gemini 1.5 Flash) |
| Data Storage | JSON |
| Platform | Windows, Linux, macOS |

**Dependencies:**
- `google-generativeai>=0.3.0` (optional, for AI features)
- Python standard library (core functionality)

---

## 7. Usage

### Installation

```bash
git clone https://github.com/Misbah-jameel/hackathon_2.git
cd hackathon_2
pip install -r requirements.txt
```

### Configuration (Optional)

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/macOS
export GEMINI_API_KEY=your_api_key_here
```

### Running

```bash
python main.py
```

### Main Menu Options

| Option | Action |
|--------|--------|
| 1 | Add New Task |
| 2 | View All Tasks |
| 3 | View Task Details |
| 4 | Update Task |
| 5 | Delete Task |
| 6 | Search Tasks |
| 7 | Filter Tasks |
| 8 | Mark Task Complete |
| 9 | View Statistics |
| A | AI Assistant |
| C | Clear All Tasks |
| Q | Quit |

---

## 8. Data Model

### Task Entity

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: Priority      # LOW, MEDIUM, HIGH
    status: Status          # PENDING, IN_PROGRESS, COMPLETED
    due_date: Optional[str]
    created_at: str
    updated_at: str
    tags: List[str]
```

### Persistence

Tasks are stored in `tasks.json` with the following structure:
- Human-readable JSON format
- Auto-incrementing IDs
- Automatic save after each operation
- Automatic load on startup

---

## 9. Development Standards

### Code Quality

- Type hints throughout codebase
- Docstrings for all public functions
- Consistent naming conventions
- Modular design with clear interfaces

### Error Handling

- Try-catch blocks for file operations
- Graceful degradation for missing API keys
- User-friendly error messages
- Input validation at entry points

### Testing

- Demo script for feature verification
- Manual testing procedures documented
- Test-first approach encouraged

---

## 10. Governance

### Versioning

The project follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to core functionality
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes and minor improvements

### Current Version: 1.0.0

### Decision Making

Architectural decisions are documented using Architecture Decision Records (ADRs) in the `.specify/` directory when applicable.

---

## 11. Roadmap

### Completed (Phase 1)
- Core task management functionality
- JSON persistence
- AI integration
- Console interface
- Documentation

### Planned (Future Phases)
- Database migration (SQL)
- Web interface
- Multi-user support
- Task categories/projects
- Recurring tasks
- Calendar integration
- Mobile client
- Data export/import

---

## 12. License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 13. Contact

**Author:** Misbah-jameel
**Repository:** https://github.com/Misbah-jameel/hackathon_2

---

*Constitution Version: 1.0*
*Last Updated: January 2026*
