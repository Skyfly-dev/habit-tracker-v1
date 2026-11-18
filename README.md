
# Python Habit Tracker (CLI)

A command-line habit tracking application built with pure Python. 

## Features
- **Persistent Storage:** Saves data locally using JSON.
- **Relational Data:** Uses foreign keys (`habit_id`) to link daily logs to specific habits.
- **Dynamic Status:** Calculates today's status dynamically (defaults to "not done" if no log exists).
- **Cascade Delete:** Deleting a habit safely removes all its historical logs to prevent orphaned data.
- **Input Validation:** Handles missing files, corrupted JSON, and duplicate daily logs.

## How to Run
1. Clone the repository.
2. Run `python habit_tracker.py` in your terminal.
