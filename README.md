# Birds API Project

## Project Overview

This project is a RESTful API built with **Flask** that manages a collection of birds stored in a **MySQL** database. The API supports full **CRUD operations** (Create, Read, Update, Delete), user authentication using **JWT tokens**, search functionality, and optional **JSON or XML** responses.

The project also includes a **Python client/testing script** that demonstrates how to interact with the API step by step.

---

## Features

* User authentication using JWT (login required for protected routes)
* CRUD operations for birds
* Search birds by name, habitat, and status
* JSON (default) and XML response formats
* MySQL database integration
* Example client script using `requests`

---

## Technologies Used

* Python
* Flask
* Flask-MySQLdb
* JWT (JSON Web Tokens)
* MySQL
* Requests (for API testing)

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/birds-api.git
cd birds-api
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask flask-mysqldb pyjwt dicttoxml requests
```

### 4. Database Setup

Create a MySQL database named `animals` and a table named `birds`:

```sql
CREATE DATABASE animals;
USE animals;

CREATE TABLE birds (
  idbirds INT AUTO_INCREMENT PRIMARY KEY,
  specificname VARCHAR(100),
  scientificname VARCHAR(150),
  habitat VARCHAR(255),
  status VARCHAR(50)
);
```

Update database credentials in `app.py` if needed:

```python
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

## Authentication

### Login Endpoint

**POST /login**

Request body:

```json
{
  "username": "admin",
  "password": "password"
}
```

Response:

```json
{
  "token": "<JWT_TOKEN>"
}
```

This token must be included in the `Authorization` header for protected endpoints:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## API Endpoints

### Get All Birds

**GET /birds**

Optional:

* `?format=xml` for XML output

---

### Get Bird by ID

**GET /birds/<id>**

---

### Create a Bird (Protected)

**POST /birds**

Headers:

```
Authorization: Bearer <JWT_TOKEN>
```

Body:

```json
{
  "specificname": "Eagle",
  "scientificname": "Aquila chrysaetos",
  "habitat": "Mountains",
  "status": "Least Concern"
}
```

---

### Update a Bird (Protected)

**PUT /birds/<id>**

Headers:

```
Authorization: Bearer <JWT_TOKEN>
```

Body:

```json
{
  "specificname": "Updated Eagle",
  "scientificname": "Aquila updated",
  "habitat": "Cliffs",
  "status": "Vulnerable"
}
```

---

### Delete a Bird (Protected)

**DELETE /birds/<id>**

Headers:

```
Authorization: Bearer <JWT_TOKEN>
```

---

### Search Birds

**GET /birds/search**

Query parameters:

* `name`
* `habitat`
* `status`
* `format=xml`

Example:

```
/birds/search?name=Eagle&status=Vulnerable
```

---

## Client/Test Script

The provided Python script demonstrates:

* Logging in and retrieving a JWT token
* Creating a bird
* Fetching all birds
* Fetching a bird by ID
* Updating a bird
* Deleting a bird
* Searching birds
* Requesting XML output

Run the script while the Flask server is active:

```bash
python test_crud.py
```


