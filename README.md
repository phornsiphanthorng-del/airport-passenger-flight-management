# ✈️ Airport Passenger & Flight Data Management System

A Python-based desktop application for managing airport passenger, flight, booking, and baggage information through a MySQL database.

This project demonstrates database management, Python application development, SQL operations, and data visualization in an airport management environment.

## 📌 Project Overview

The Airport Passenger & Flight Data Management System is designed to organize and manage important airport operational information in one centralized application.

It provides an interface for administrators to manage records, monitor database information, and view summarized operational data.

## ✨ Main Features

### 1. Dashboard
- Display total passengers, flights, bookings, and baggage.
- Visualize flights by airline.
- Display bookings by travel class.
- View upcoming flights and recent database activity.

### 2. Passenger Management
- View passenger records.
- Add new passengers.
- Edit passenger information.
- Delete passenger records.
- Search passenger information.

### 3. Flight Management
- View flight information.
- Add, edit, and delete flight records.
- Search flights by flight number or status.

### 4. Booking Management
- Manage passenger flight bookings.
- Add, edit, and delete booking records.

### 5. Baggage Management
- Manage baggage information.
- View and update baggage records.

### 6. Reports
- Generate summarized reports.
- Analyze flights by airline.
- Analyze bookings by class.
- View baggage information by status.

### 7. Settings
- View database connection information.
- Check database connection status.
- Change application appearance.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| CustomTkinter | Desktop user interface |
| MySQL | Relational database management |
| MySQL Connector | Python–MySQL connection |
| SQL | Database queries and operations |
| Matplotlib | Data visualization |

## 📁 Project Structure

```text
airport-passenger-flight-management/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
└── pages/
    ├── __init__.py
    ├── passengers.py
    ├── flights.py
    ├── booking.py
    ├── baggage.py
    ├── reports.py
    └── settings.py
```

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your computer.
- MySQL Server installed and running.
- Git installed.
- A MySQL database named `airport_management`, with the required tables created.

### Step 1: Clone the repository

```bash
git clone https://github.com/phornsiphanthorng-del/airport-passenger-flight-management.git
```

### Step 2: Open the project folder

```bash
cd airport-passenger-flight-management
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create your local `.env` file by copying `.env.example`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your own MySQL connection settings:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=airport_management
```

Replace the example password with your own MySQL password.

**Security:** Never upload your `.env` file or database credentials to GitHub.

### Step 5: Prepare the database

Ensure that the `airport_management` database and all required tables have been created in MySQL before running the application.

### Step 6: Run the application

```bash
python main.py
```

## 🔐 Database Security

- Database credentials are stored in environment variables.
- The `.env` file is excluded from Git tracking.
- SQL queries use parameterized statements in the application modules.

## 🎯 Project Objectives

- Apply relational database management concepts.
- Develop a desktop application using Python.
- Implement SQL CRUD operations.
- Connect a Python application to MySQL.
- Present operational data through dashboards and reports.
- Build practical software development and database management skills.

## 🚀 Future Improvements

- Improve data validation and user experience.
- Add user authentication and role management.
- Improve report generation and export options.
- Add more advanced data analytics.
- Explore AI-based flight and passenger data analysis.

## 👨‍💻 Author

**Phorn Siphanthorng**

Data Science & AI Engineering Student

CamTech University

## 📄 Project Status

The application has been implemented with a working dashboard, database connection, and management modules. Further improvements and documentation are ongoing.

---

*Developed as an academic and portfolio project.*