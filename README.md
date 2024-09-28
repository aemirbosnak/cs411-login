# Flask Login Application

This is a simple Flask application that provides separate login pages for admin and doctor users, using MongoDB for user management.

## Prerequisites

- Python 3.x
- MongoDB
- Pip (Python package installer)

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Install Requirements**

   ```bash
   pip install -r requirements.txt

3. **Set up the Database**

   ```bash
   sudo systemctl start mongod
   mongosh
   use mydb

   *Add admin user*
   ```bash
   db.users.insertOne({
      email: "admin@home.com",
      firstName: "Admin",
      lastName: "User",
      password: "password", // hash and salt with bcrypt before adding to database
      role: "admin",
      createdAt: new Date().getTime(),
      updatedAt: new Date().getTime()
   });

   *Add doctor user*
   ```bash
   db.users.insertOne({
      email: "doctor@home.com",
      firstName: "Doctor",
      lastName: "User",
      password: "password", // hash and salt with bcrypt before adding to database
      role: "doctor",
      createdAt: new Date().getTime(),
      updatedAt: new Date().getTime()
   });

4. **Run the Application**
   
   ```bash
   python3 app.py

   The application runs at localhost:5000
