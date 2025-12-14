# CSE1 Final Project – Student CRUD REST API

## Project Overview

This project is a **CRUD (Create, Read, Update, Delete) REST API** developed as a final requirement for **CSE1**. The API is built using **Flask** and **MySQL** and allows clients to manage student records securely.

The system supports:

* Secure access using **JWT authentication**
* Full CRUD operations on student data
* **Search functionality**
* API responses in **JSON or XML format**
* Automated testing using **pytest**

---

## Technologies Used

* Python 3
* Flask
* MySQL
* flask-mysqldb
* flask-jwt-extended (JWT Authentication)
* dicttoxml
* pytest

---

## Database Structure

The project uses a MySQL database with the following tables:

* **student** – main table used for CRUD operations
* **instructor** – referenced by student (foreign key)
* **program** – referenced by student (foreign key)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CSE-CRUD-PROJECT.git
cd CSE-CRUD-PROJECT
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv flaskvenv
flaskvenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

* Make sure **MySQL Server** is running
* Import the provided SQL file into MySQL
* Update database credentials in `app.py` if needed

### 5. Run the Application

```bash
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

## Authentication (JWT)

### Login Endpoint

**POST** `/login`

Request Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

The token must be included in the **Authorization header** for all protected routes:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## API Endpoints

| Method | Endpoint               | Description             |
| ------ | ---------------------- | ----------------------- |
| GET    | /students              | Retrieve all students   |
| POST   | /students              | Create a new student    |
| PUT    | /students/             | Update a student        |
| DELETE | /students/             | Delete a student        |
| GET    | /students/search?name= | Search students by name |

---

## Response Formats

### JSON (Default)

```http
GET /students
```

### XML

```http
GET /students?format=xml
```

---

## Edge Case Handling

The API handles multiple edge cases including:

* Missing or invalid request bodies
* Unauthorized access (JWT required)
* Missing search parameters
* Operations on non-existent student records
* Invalid input formats

Proper HTTP status codes such as **400, 401,F, 404, 201, and 200** are returned accordingly.

---

## Automated Testing

Automated tests were implemented using **pytest** to validate:

* Authentication
* CRUD operations
* Edge cases (missing data, non-existent records, unauthorized access)

### Run Tests

```bash
pytest
```

---

## Author

**Juan Miguel M. Malate**  
BSCS3-B2
