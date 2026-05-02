# Student Result Management System

## Project Overview

This repository contains a simple student result management application built with Python.

There are two components:

- `sudent mangament/app.py`: A Flask web application with a responsive single-page dashboard for managing student records and results.
- `student_result_managment.py`: A basic command-line student manager for adding, viewing, and checking student results.

## Features

### Flask Web App

- Add new student records with marks
- View all students
- Update a student’s marks
- Delete a student record
- Check an individual student result
- Displays `Pass` or `Fail` automatically based on marks
- Uses MySQL for persistent storage

### CLI Script

- Add student name and marks
- View stored students in memory
- Check pass/fail status for a student

## Project Structure

```
studen managment system/
  README.md
  student_result_managment.py
  sudent mangament/
    app.py
    mySql.sql
    static/
      style.css
    templates/
      index.html
```

## Requirements

- Python 3.x
- Flask
- mysql-connector-python
- MySQL server

## Setup Instructions

1. Install dependencies:

```bash
pip install flask mysql-connector-python
```

2. Configure MySQL:

- Create the database and table using `sudent mangament/mySql.sql`.
- Update the database credentials in `sudent mangament/app.py` if needed.

3. Start the Flask app:

```bash
python "sudent mangament/app.py"
```

4. Open your browser:

- Visit `http://127.0.0.1:5000/`

## Database Schema

The `students` table is defined in `sudent mangament/mySql.sql`:

- `id` - auto-increment primary key
- `name` - unique student name
- `marks` - numeric score
- `result` - `Pass` or `Fail`
- `created_at` - created timestamp
- `updated_at` - updated timestamp

## API Endpoints

The web app uses the following JSON REST API endpoints:

- `POST /api/add_student` - Add a new student
- `GET /api/get_students` - Retrieve all students
- `GET /api/get_student/<name>` - Retrieve a student by name
- `PUT /api/update_student` - Update student marks
- `DELETE /api/delete_student/<name>` - Delete a student

## Notes

- The web UI is served by `templates/index.html` and uses `static/style.css`.
- The web app runs in debug mode by default.
- `student_result_managment.py` is an alternate terminal-based implementation that stores data in memory only.

## License

This project is provided as-is for learning and demo purposes.
