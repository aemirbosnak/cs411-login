# Flask Microservice Login Project

This project implements a microservice architecture for a simple login application using Flask, MongoDB, and Docker.
The microservice architecture approach separates backend and frontend as individual projects and further separates
the frontend to role based projects (admin, doctor, patient, etc.).

- **Backend**: A Flask-based API that handles authentication.
- **Frontend-Admin**: A simple HTML, CSS, and JavaScript-based application for admin users.
- **Frontend-Doctor**: A similar frontend for doctor users.

## Services Overview

**Backend**

- The backend is a Flask-based API responsible for handling authentication and connecting to MongoDB.
- The backend have two endpoints
  - `/api/auth/login` (POST): Authenticate user with email and password.
  - `/api/auth/logout` (POST): Log out authenticated user.
- JWT tokens are used for client side session management.

**Admin Frontend**
- A static HTML, CSS, and JS-based admin application that communicates with the backend for login and dashboard rendering.

**Doctor Frontend**
- Similar to the admin frontend but tailored for doctors.

## Installation and Deployment

### Prerequisites
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Getting Started

1. Clone the repository

    ```bash
    $ git clone https://github.com/aemirbosnak/cs411-login.git
    $ cd cs411-login
    ```
   
2. Build and start services with Docker Compose:

    ```bash
    $ docker compose up --build -d
   ```
   
This will build and start the following services:
- Backend on `localhost:5000`
- Admin frontend on `localhost:5001`
- Doctor frontend on `localhost:5002`
- MongoDB on `localhost:27000`

### Usage
When the containers are first started the MongoDB database will be empty, so we need to go inside 
the container and add entries manually (this will be fixed in the future with a sign-up functionality):

1. Execute into the MongoDB container

    ```bash
    $ docker exec -it code-mongo-1 /bin/bash
    ```
   
2. Start the interactive MongoDB shell and add admin and doctor entries

    ```bash
    $ mongosh
    test> use mydb
    mydb> db.Users.insertOne({ email: "admin@home.com", firstName: "Jane", lastName: "Doe", password: <bcrypt encrypted and utf-8 encoded password>, role: "admin", createdAt: new Date().getTime(), updatedAt: new Date().getTime() })
    mydb> db.Users.insertOne({ email: "doctor@home.com", firstName: "Adam", lastName: "Smith", password: <bcrypt encrypted and utf-8 encoded password>, role: "doctor", createdAt: new Date().getTime(), updatedAt: new Date().getTime() })
    ```

3. Encrypting the password to be added into the database:
    
    ```bash
    $ python3 -c 'import bcrypt; print(bcrypt.hashpw(<your-password>.encode(), bcrypt.gensalt()).decode())'
    output -> $2b$12$7rhIwwmCbC6o.s/2k8bPYecZPhf2.JIBYYDXaRDiHBUuPX5Cq6/Pa
    ```
   
    We can log in with `<your-password>` after encrypting it like above and putting the output in the database.


4. Now that we have an admin and doctor account we can go to their respective login pages to see if we can log in.
   - For admin go to `localhost:5001/login/login.html` and enter credentials.
   - For doctor go to `localhost:5002/login/login.html` and enter credentials.


### Extending the application
The application can be extended with adding new user roles. To add new user roles we should create a new `frontend-<role>`
project for the frontend and add the necessary API functions in the backend. A new role can easily be added into the 
`UserRole` class in the `backend/models.py` file. No change needed in the database. The new service should also be added
to the `docker-compose.yml` file.
