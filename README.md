# Task Manager Pro

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
[![GitHub stars](https://img.shields.io/github/stars/Misbah-jameel/hackathon_2?style=social)](https://github.com/Misbah-jameel/hackathon_2)

AI-Powered Task Management Console Application built with Python and Google Gemini.

## Demo

<!-- Add your screenshot or demo gif here -->
<!-- ![Demo](assets/demo.gif) -->
<!-- ![Screenshot](assets/screenshot.png) -->

> **Coming Soon:** Add a screenshot or demo gif to showcase the application.
>
> To add your own:
> 1. Create an `assets` folder in the project root
> 2. Add your `screenshot.png` or `demo.gif`
> 3. Uncomment the appropriate line above

## Features

- **Task Management (CRUD)**: Create, view, update, and delete tasks
- **Priority Levels**: Low, Medium, High, Urgent
- **Status Tracking**: Pending, In Progress, Completed, Cancelled
- **Due Dates**: Set and track task deadlines
- **Tags**: Organize tasks with custom tags
- **Search & Filter**: Find tasks by keyword, status, priority, or overdue status
- **Statistics**: View task completion stats and summaries

### AI Features (Powered by Google Gemini)

- Task improvement suggestions
- Priority recommendations
- Task breakdown into subtasks
- Smart natural language search
- Task summarization
- Daily motivation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Misbah-jameel/hackathon_2.git
cd hackathon_2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Gemini API for AI features:
```bash
set GEMINI_API_KEY=your_api_key_here
```
Get your API key at: https://makersuite.google.com/app/apikey

## Usage

Run the application:
```bash
python main.py
```

### Main Menu Options

| Option | Description |
|--------|-------------|
| 1 | Add new task |
| 2 | View all tasks |
| 3 | View task details |
| 4 | Update task |
| 5 | Delete task |
| 6 | Mark task complete |
| 7 | Search tasks |
| 8 | Filter tasks |
| 9 | View statistics |
| A | AI Assistant |
| C | Clear all tasks |
| Q | Quit |

## Project Structure

```
hackathon_2/
├── main.py           # Entry point and menu system
├── models.py         # Task, Priority, Status models
├── store.py          # Task storage and persistence
├── ui.py             # User interface utilities
├── gemini_service.py # Google Gemini AI integration
├── tasks.json        # Task data storage
└── requirements.txt  # Python dependencies
```

## License

MIT
