# 🧠 Pomodoro Task Tracker  
_A modular, override-proof productivity tool built in Python with GUI clarity and emotional feedback loops._

## 📦 Overview

This is a **chunky, icon-enhanced Pomodoro Task Tracker** built with `tkinter`. It blends task management with Pomodoro timing, designed for clarity, accessibility, and override-resilient styling.

Features include:

- ✅ Add, delete, and reorder tasks with confirmation  
- ⏱️ Integrated Pomodoro timer with start/pause/reset  
- 🎨 Accessible color scheme and bold calculator aesthetics  
- 🧩 Modular layout with side-by-side task and timer panels  
- 🔔 Looping system alert and flashing screen on timer completion  
- 🧹 Focus Mode removed for clarity and emotional coherence  

## 🧩 Layout

```
| Entry Panel | Task Display (50%) | Timer Panel |
```

- **Entry Panel**: Add tasks with priority, icons, and feedback  
- **Task Display**: Scrollable, reorderable list with color-coded priorities  
- **Timer Panel**: Pomodoro logic with visual cues and duration presets  

## 🎯 Features

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| ➕ Add Task            | Input field with priority dropdown and icon-enhanced buttons                |
| 🗑️ Delete Task         | Confirmation prompt before removal                                          |
| 🔼🔽 Reorder Tasks      | Move tasks up/down with persistent state                                    |
| 💾 Save/Load Tasks     | JSON-based local storage with fallback creation                             |
| ⏱️ Pomodoro Timer      | 15/20/25/30-min cycles with progress bar and visual feedback                |
| 🔔 Alert System        | Looping sound and flashing screen when timer ends                           |
| 🎨 Accessible Design   | High-contrast colors, readable fonts, and modular layout                    |
| 🧹 Removed Focus Mode  | Simplified interface for emotional clarity and reduced cognitive load       |

## 🧪 QA Notes

- Override-proof styling using brute-force widget configuration  
- Modular code blocks for easy extension and debugging  
- Accessible color palette tested for contrast and readability  
- Resilient against layout breakage on resize  
- Uses `winsound` for native alerting (Windows only)  

## 📁 File Structure

```
pomodoro-task-tracker/
├── tracker.py         # Main GUI logic
├── tasks.json         # Auto-generated task storage
```

## 🧠 Philosophy

This tracker is built for **intentional productivity**. It respects emotional boundaries, honors clarity, and avoids clutter. Every button, color, and layout choice is designed to support real focus—not just perform it.
