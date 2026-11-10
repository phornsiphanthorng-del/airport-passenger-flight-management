# ✈️ Airport Passenger & Flight Data Management System

## 📌 Project Overview

The Airport Passenger & Flight Data Management System is a desktop application designed to manage airport passenger and flight information in one centralized system.

The application uses Python and MySQL to organize and manage passenger records, flight schedules, bookings, baggage information, and operational reports.

## 🎯 Project Objectives

- Organize airport passenger and flight information.
- Manage booking and baggage records.
- Provide a centralized database for airport operations.
- Generate useful reports and statistics.
- Build practical skills in database management and application development.

## 🚀 Main Features

- **Dashboard:** View passenger, flight, booking, and baggage statistics.
- **Passenger Management:** Add, view, search, edit, and delete passenger records.
- **Flight Management:** Manage flight information and schedules.
- **Booking Management:** Manage passenger flight bookings.
- **Baggage Management:** Manage baggage records.
- **Reports:** View summarized airport information.
- **Settings:** View application and database connection information.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming |
| CustomTkinter | Desktop user interface |
| MySQL | Database management |
| MySQL Connector/Python | Python–MySQL connection |
| python-dotenv | Environment variable management |
| Git | Version control |
| GitHub | Project hosting |

## 📂 Project Structure

```text
Airport-Passenger-Flight-Data-Management-System/
│
├── pages/
│   ├── __init__.py
│   ├── passengers.py
│   ├── flights.py
│   ├── booking.py
│   ├── baggage.py
│   ├── reports.py
│   └── settings.py
│
├── .env.example
├── .gitignore
├── database.py
├── requirements.txt
├── main.py
│
├── SQL Scripts/
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Airport-Passenger-Flight-Data-Management-System
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Configure the database

- Install and start MySQL Server.
- Create the `airport_management` database.
- Import the project's SQL schema and sample data scripts.
- Create your local `.env` file using `.env.example` as a reference.
- Enter your own MySQL connection details in `.env`.

**Important:** Never upload your `.env` file or database password to GitHub.

### 5. Run the application

```bash
python main.py
```

Use the actual application entry-point filename if it differs from `main.py`.

## 🗄️ Database

The application uses MySQL to store and manage airport-related information.

The database includes records for passengers, flights, bookings, and baggage, together with related airport information.

## 🔐 Security

- Database credentials are stored in environment variables.
- The `.env` file is excluded from Git tracking.
- SQL queries use parameterized statements in the application.

## 📊 Project Status

The project includes database implementation and a working Python desktop application with a dashboard and management modules.

Further improvements and testing may be added as development continues.

## 👨‍💻 Author

Developed as an academic project for Data Science and AI Engineering.

---

**Project:** Airport Passenger & Flight Data Management System  
**Database:** MySQL  
**Application:** Python Desktop Application