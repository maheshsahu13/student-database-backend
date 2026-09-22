# Student Database Application System

A full-stack student database application with secure authentication, REST APIs, database management, and an AI-powered chatbot for querying student information.

## Features

### Student Management

* Add student records
* View student records
* Update student information
* Delete student records
* Filter students by department and course
* Sort student records
* Paginate student results
* View student statistics

### Authentication

* User registration
* User login
* Password hashing
* JWT-based authentication
* Protected student APIs
* Protected AI chatbot endpoint

### AI Student Assistant

* Natural-language questions about student data
* Gemini-powered responses
* LangGraph workflow
* Student database retrieval
* AI chatbot integrated into the dashboard
* Responses based on the available student database
* Prevents the AI from intentionally inventing unavailable student information

### Frontend

* Login page
* Registration page
* Student dashboard
* Student management interface
* Statistics cards
* AI chatbot interface
* Responsive layout

---

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* JWT Authentication
* Password Hashing

### AI

* Google Gemini
* LangChain
* LangGraph

### Frontend

* HTML
* CSS
* JavaScript

### Development

* Git
* GitHub
* Python Virtual Environment
* Pytest

---

## System Architecture

```text
                         USER
                           |
                           v
                    FRONTEND DASHBOARD
                           |
                           v
                         FastAPI
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Authentication              AI Chatbot
             |                           |
             v                           v
            JWT                       LangGraph
             |                           |
             |                    +------+------+
             |                    |             |
             |                    v             v
             |              Student DB       Gemini
             |                    |             |
             |                    +------+------+
             |                           |
             +-------------+-------------+
                           |
                           v
                       RESPONSE
```

---

## AI Chatbot Architecture

The AI chatbot follows a simple retrieval-and-generation workflow:

```text
User Question
      |
      v
POST /chat/
      |
      v
JWT Authentication
      |
      v
LangGraph
      |
      v
Retrieve Student Data
      |
      v
Generate Answer with Gemini
      |
      v
Return AI Response
      |
      v
Dashboard Chat Interface
```

The current implementation uses structured database retrieval rather than vector search.

---

## Database

The application currently uses SQLite with SQLAlchemy.

The student table contains fields such as:

| Field      | Description               |
| ---------- | ------------------------- |
| ID         | Unique student identifier |
| Name       | Student name              |
| Email      | Student email             |
| Phone      | Student phone number      |
| Department | Student department        |
| Course     | Student course            |
| Semester   | Current semester          |
| CGPA       | Student CGPA              |

---

## API Endpoints

### Health

```text
GET /health
```

Checks whether the API is running.

### Authentication

```text
POST /auth/register
POST /auth/login
```

Used for user registration and authentication.

### Students

```text
POST   /students/
GET    /students/
GET    /students/{student_id}
GET    /students/stats
PUT    /students/{student_id}
DELETE /students/{student_id}
```

Student management endpoints require authentication.

### AI Chatbot

```text
POST /chat/
```

Accepts a natural-language question and returns an AI-generated answer based on the student database.

Example request:

```json
{
    "question": "Which students have a CGPA above 8?"
}
```

Example response:

```json
{
    "answer": "The following students have a CGPA above 8..."
}
```

---

## Project Structure

```text
Student-Database-Application/
│
├── app/
│   ├── ai/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── prompts.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── __init__.py
│   │
│   ├── crud/
│   │   ├── student.py
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── student.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── students.py
│   │   ├── chat.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── student.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   ├── jwt.py
│   │   ├── password.py
│   │   └── __init__.py
│   │
│   └── main.py
│
├── frontend/
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── auth.js
│       └── dashboard.js
│
├── docs/
│   └── architecture_decision.md
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_students.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Vector Database Decision

A vector database is **not included in the current implementation**.

The primary application data is structured student information. SQL-based retrieval is therefore used for the current chatbot.

A vector database can be introduced in a future version for semantic search over unstructured information such as:

* College policies
* Student handbooks
* Scholarship documents
* Course descriptions
* University notices
* PDF and text documents

This would allow the application to use a hybrid architecture:

```text
                    User
                      |
                      v
                 AI Chatbot
                      |
                      v
                  LangGraph
                   /      \
                  /        \
                 v          v
        SQL Database    Vector Database
        Structured       Unstructured
           Data             Data
                  \        /
                   \      /
                    v    v
                    Gemini
                      |
                      v
                   Response
```

The vector database is therefore considered a **future extension**, not a required component of the current system.

---

## Security

The application uses several security mechanisms:

* Password hashing
* JWT authentication
* Protected student endpoints
* Protected AI chatbot endpoint
* Environment variables for sensitive configuration
* `.env` excluded from Git
* Database files excluded from Git

The Gemini API key is stored in the environment rather than directly in source code.

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./student_database.db
GEMINI_API_KEY=your_gemini_api_key
```

Never commit the actual `.env` file or API key to GitHub.

---

## Running the Backend

Create and activate a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---
## Running with Docker

The backend can also be run using Docker.

### Build the Docker Image

From the project root:

```powershell
docker build -t student-database-api .

## Testing

The project includes automated tests for authentication and student APIs.

Run:

```powershell
pytest
```

The AI chatbot has also been tested through the LangGraph workflow and the `/chat/` API endpoint using database-related questions.

---

## Example AI Questions

The chatbot can answer questions such as:

```text
How many students are in the database?
```

```text
Which students have a CGPA above 8?
```

```text
Which department has students?
```

The chatbot uses the available student database information when generating its responses.

---

## Future Improvements

Potential future improvements include:

* Vector database integration
* Retrieval-Augmented Generation (RAG)
* Semantic search over college documents
* More advanced AI query routing
* Student document ingestion
* Improved chatbot conversation memory
* Role-based access control
* Production database such as PostgreSQL
* Cloud deployment
* Improved frontend design
* Monitoring and logging

---

## Project Status

The current version includes:

* Full CRUD student management
* User authentication
* JWT security
* SQLite database
* REST API
* Interactive frontend dashboard
* Gemini AI integration
* LangGraph workflow
* AI student database chatbot
* Protected chatbot endpoint
* Architecture documentation

The project is currently in the final testing and deployment stage.



