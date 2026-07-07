# Smart Civic: Issue Reporting Platform
### Project Explanation & Run Guide for Professor Reference

---

## 1. Project Overview
**Smart Civic** is a modern, Flask-based civic issue reporting web application designed to bridge the communication gap between citizens, local municipality officers, and city administrators. 

The primary goal of the application is to empower citizens to easily report local infrastructure issues (like potholes, street light failures, garbage dumps, or water leakages), while providing public officers and administrators with a structured pipeline to assign, track, and resolve these issues efficiently.

---

## 2. Target User Roles & Capabilities
The application supports three distinct user groups with role-based access control:

### A. Citizen (The Public User)
* **Registration & Auth**: Can create an account and sign in.
* **Report Issues**: File a new complaint by selecting a category (e.g., Road damage, Water leakage), describing the problem, uploading an image, and capturing their automatic GPS coordinates.
* **Dashboard**: Track the real-time status of their reported complaints and view issue histories.
* **Explore Nearby**: View recent issues reported in their vicinity using coordinates.

### B. Officer (The Field Worker)
* **Assigned Queue**: View all civic issues assigned to them or their department.
* **Assign Self**: Take ownership of unassigned active issues.
* **Update Status**: Change the state of complaints (e.g., from *Open* to *In Progress* or *Resolved*), add resolution remarks, and upload "before and after" photos.

### C. Administrator (The Municipal Manager)
* **Central Dashboard**: View visual analytics and trends of incoming civic issues using Chart.js graphs.
* **User Management**: View citizen directories.
* **Officer Management**: Create and manage field officer profiles and assign them to departments/areas.
* **Category Management**: Edit, delete, and add new issue categories.
* **Complaint Control**: Manually re-route, assign, or overwrite any issue status or officer assignment.

---

## 3. Technology Stack & Database Architecture

### Technology Stack
* **Frontend**: HTML5, CSS3, Bootstrap 5 (Responsive Layouts), Chart.js (Data Analytics/Graphs), Jinja2 (Python template rendering).
* **Backend Framework**: Python Flask.
* **Database Access**: Flask-SQLAlchemy (Object Relational Mapping) and Flask-Migrate.
* **Security & Authentication**: Flask-Login (session-based authentication) and Flask-WTF (CSRF protection against web attacks).
* **Database Driver**: `psycopg2-binary` (PostgreSQL adapter).
* **Cloud Database**: Neon Tech Serverless PostgreSQL Database.
* **Cloud Storage**: AWS S3 integration for hosting uploaded issue/resolution images.

### Database Schema (ERD Design)
The system operates on 6 main database tables modeled via SQLAlchemy in Python:

1. **`users`**: Stores user authentication credentials, names, roles (`citizen`, `officer`, `admin`), and phone/address info.
2. **`officers`**: Extends the `users` table for officers, tracking department fields and assigned service areas.
3. **`categories`**: Stores valid issue categories (e.g., "Street light failure").
4. **`complaint_status`**: Stores state values ("Open", "In Progress", "Resolved").
5. **`complaints`**: The central transactional table storing the user who reported it, assigned officer, coordinates, description, and AWS S3 URLs for submitted images.
6. **`notifications`**: Stores log messages triggered automatically when status changes occur to notify the user.

---

## 4. Complete End-to-End Execution Guide

Follow these steps to set up and run the project locally on your system.

### Prerequisites
* **Python** (version 3.10 or higher) installed on your system.
* Internet connection (for database and styling resources).

### Step 1: Create Virtual Environment
Open your terminal (PowerShell, Command Prompt, or Bash) in the project directory:
```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (macOS/Linux)
source venv/bin/activate
```

### Step 2: Install Dependencies
Install all required libraries, including the web framework, security packages, and database adapters:
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (`.env`)
Create a file named `.env` in the root of the project (if it doesn't already exist) and insert the database credentials.
```env
DATABASE_URL=postgresql://neondb_owner:npg_S39KbqGOwRjF@ep-shy-morning-aovce2jj.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=super-secret-key
```
*(Note: This uses the cloud Neon Tech serverless PostgreSQL database instance for live database connectivity.)*

### Step 4: Initialize and Seed the Database
To create the necessary PostgreSQL tables and seed them with default administration users, categories, and test issues, run:
```powershell
python seed_db.py
```
This runs the initialization script and prints success statements for tables created and data seeded.

### Step 5: Start the Development Server
Run the Flask server:
```powershell
python run.py
```
The server will boot up and should be active at `http://127.0.0.1:5000/`.

---

## 5. Testing Credentials

You can test the three different system roles using these pre-seeded accounts:

* **Administrator Login**:
  * **Email**: `admin@smartcivic.local`
  * **Password**: `password`
* **Citizen Login**:
  * **Email**: `jane.user@example.com`
  * **Password**: `password`
* **Officer Login**:
  * **Email**: `joe.officer@example.com`
  * **Password**: `password`
