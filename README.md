# 🎟 Ticket Tracking System

## 📌 Project Overview

The Ticket Tracking System is a web-based application developed using
Python (Flask) that allows users to create, track, update, and manage
support tickets efficiently.

The system follows a layered architecture based on: - MVC
(Model--View--Controller) - Domain-Driven Design (DDD) - Repository
Pattern - Clean Code principles

------------------------------------------------------------------------

## 🏗 Architecture

Controller → Service → Repository → Domain Model → Database

### MVC Pattern

-   Model → Domain + Repository layer
-   View → HTML templates (Jinja2)
-   Controller → Flask route handlers

------------------------------------------------------------------------

## 📂 Folder Structure

ticket-tracking-system/ │ ├── controller/ \# Route handlers ├── service/
\# Business logic ├── repository/ \# Database interaction ├── domain/ \#
Core domain models ├── templates/ \# HTML views ├── static/ \# CSS & JS
├── app.py \# Entry point ├── requirements.txt \# Dependencies └──
README.md

------------------------------------------------------------------------

## 💡 Features

-   Create support tickets
-   View all tickets
-   Update ticket status
-   Delete tickets
-   Structured database interaction

------------------------------------------------------------------------

## ⚙️ Technologies Used

- Python 3
- Flask
- mysql-connector-python
- HTML5
- CSS3
- Jinja2
- Werkzeug (Password Hashing)

------------------------------------------------------------------------

## 🚀 How to Run

1.  Create virtual environment: python -m venv venv

2.  Activate: Windows: venv`\Scripts`{=tex}`\activate`{=tex} Mac/Linux:
    source venv/bin/activate

3.  Install dependencies: pip install -r requirements.txt

4.  Run: python app.py

App runs at: http://127.0.0.1:5000

------------------------------------------------------------------------

## 👨‍💻 Author

Noor Hazmath Shaik\
B.Tech -- Computer Science Engineering\
Email: shaiknoorhazmath@gmail.com\
Phone: +91 7032563635
