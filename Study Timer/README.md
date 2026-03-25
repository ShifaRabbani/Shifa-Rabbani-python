# ⏱️ Study Timer Web App

A simple and clean web-based **Study Timer** that helps you stay focused by setting time blocks for different tasks like studying, workouts, or any daily activity.

---

## 🚀 Features

- ⏳ Create custom timers (e.g., Math Study – 30 mins)
- 📋 View all saved timers
- ✏️ Update existing timers
- ❌ Delete timers
- 🕒 Track when each timer was created
- ⚡ Real-time interaction with backend APIs

---

## 🛠️ Tech Stack

**Frontend:**
- HTML
- CSS
- JavaScript

**Backend:**
- Python (Flask)
- SQLAlchemy

**Database:**
- MySQL

---

## ⚙️ How It Works

- Users create a timer by entering:
  - Task name (e.g., Study, Workout)
  - Duration (in minutes)
- The data is stored in a MySQL database
- Backend APIs handle:
  - Fetching timers
  - Creating new timers
  - Updating timers
  - Deleting timers

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|--------|------------|
| GET | `/timers` | Get all timers |
| POST | `/create_time` | Create a new timer |
| PUT | `/update_timer/<id>` | Update a timer |
| DELETE | `/del_timer/<id>` | Delete a timer |

---

## 📂 Project Structure
study-timer/
│
├── app.py # Flask backend
├── index.html # UI
├── style.css # Styling
├── script.js # Frontend logic



---

## 💡 What I Learned

- Building REST APIs using Flask
- Connecting Python with MySQL using SQLAlchemy
- Performing CRUD operations
- Handling real-world user input
- Structuring a full-stack mini project

---

## 🎯 Future Improvements

- Add countdown timer UI
- Notifications or alerts
- User authentication
- Dark mode 🌙
- Mobile responsiveness

---

## 🙌 Acknowledgment

This project was built with the help of AI tools like DeepSeek for guidance and learning.

---

## 📌 Author

**Shifa Rabbani**