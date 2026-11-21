# Python Habit Tracker (Full Stack)

A full-stack habit tracking application built with Python. It started as a Command-Line Interface (CLI) and evolved into a web application with a REST API and an interactive frontend.

## 🏗️ Architecture
- **Backend API:** FastAPI (Python)
- **Frontend UI:** Streamlit (Python)
- **Database:** JSON (Local file storage for V2)

## ✨ Features
- **REST API:** Fully functional CRUD API built with FastAPI.
- **Interactive UI:** Streamlit dashboard to add, mark, skip, and delete habits.
- **Persistent Storage:** Saves data locally using JSON.
- **Relational Data:** Uses foreign keys (`habit_id`) to link daily logs to specific habits.
- **Dynamic Status:** Calculates today's status dynamically (defaults to "not done" if no log exists).
- **Cascade Delete:** Deleting a habit safely removes all its historical logs.
- **Streaks:** Calculates current streaks using date math (`timedelta`).
- **Visual Charts:** Generates a 7-day (or custom length) bar chart of habits.

## 🚀 How to Run Locally

You need two terminals running simultaneously.

**Terminal 1: Start the FastAPI Backend**
1. Install dependencies: `pip install fastapi uvicorn requests streamlit`
2. Run the API: `fastapi dev main.py` (or `uvicorn main:app --reload`)
3. View API docs at: `http://127.0.0.1:8000/docs`

**Terminal 2: Start the Streamlit Frontend**
1. Run the UI: `streamlit run app.py`
2. View the app at: `http://localhost:8501`

## 💻 CLI Version
You can still run the original terminal version:
`python habitTracker.py`