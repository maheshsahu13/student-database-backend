# Student Database Application System

A full-stack student database application built with **FastAPI, SQLite, SQLAlchemy, JWT authentication, HTML/CSS/JavaScript, Google Gemini, and LangGraph**.

The system provides secure student record management through a REST API and web dashboard, along with an AI-powered chatbot that can answer natural-language questions using information retrieved from the student database.

---

## 📌 Project Overview

The **Student Database Application System** is designed to provide a centralized platform for managing student information securely and efficiently.

The application combines:

* A **FastAPI REST backend**
* **SQLite database** for persistent student data
* **JWT-based authentication**
* A responsive **web dashboard**
* Complete **student CRUD operations**
* Filtering, sorting, pagination, and statistics
* A **Gemini-powered AI chatbot**
* A **LangGraph workflow** for AI processing
* **Automated API testing with Pytest**
* **Docker support** for containerized deployment

The current AI implementation uses **structured SQL/database retrieval** for student information rather than a vector database.

---

# ✨ Features

## 👨‍🎓 Student Management

The application provides complete student record management:

* Add new students
* View student records
* View individual student details
* Update student information
* Delete student records
* Filter students by department
* Filter students by course
* Sort student records
* Paginate student results
* View student statistics
* Email uniqueness validation
* Input validation and error handling

---

## 🔐 Authentication & Security

The application implements secure authentication using:

* User registration
* User login
* Password hashing
* JWT-based authentication
* Protected student APIs
* Protected AI chatbot endpoint
* Environment variables for sensitive configuration
* `.env` excluded from Git
* Database files excluded from Git
* Virtual environment excluded from Git

Sensitive credentials such as the Gemini API key are stored in environment variables rather than source code.

---

# 🤖 AI Student Assistant

The application includes an AI-powered chatbot integrated directly into the student dashboard.

The chatbot can answer natural-language questions about the available student database.

### Example questions

```text
How many students are in the database?
```

```text
Which students have a CGPA above 8?
```

```text
Which department has students?
```

```text
What is the CGPA of Rahul?
```

The chatbot retrieves relevant student information from the database and uses **Google Gemini** to generate the final natural-language response.

### AI Technologies

* Google Gemini
* LangChain
* LangGraph
* Structured database retrieval

The current implementation is designed to answer questions using information available in the student database and avoid intentionally generating student information that is not available in the retrieved data.

---

# 🧠 AI Chatbot Architecture

The current chatbot follows a retrieval-and-generation workflow:

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
                  Generate with Gemini
                           |
                           v
                    AI Response
                           |
                           v
                 Dashboard Chat UI
```

### Workflow

1. The authenticated user submits a natural-language question.
2. The request is sent to the `/chat/` endpoint.
3. Authentication verifies the user's JWT token.
4. LangGraph manages the AI workflow.
5. Relevant student information is retrieved from the structured database.
6. Gemini generates a natural-language response using the retrieved information.
7. The response is returned to the frontend chatbot.

---

# 🏗️ System Architecture

```text
                         USER
                           |
                           v
                  WEB DASHBOARD
                           |
                           v
                        FastAPI
                           |
              +------------+------------+
              |                         |
              v                         v
       Authentication              AI Chatbot
              |                         |
              v                         v
             JWT                    LangGraph
              |                         |
              |                  +------+------+
              |                  |             |
              |                  v             v
              |             Student DB      Gemini
              |                  |
              |                  |
              +--------+---------+
                       |
                       v
                    Response
```

---

# 🗄️ Database

The application currently uses **SQLite** with **SQLAlchemy**.

The student database contains fields including:

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

SQLite was selected for the current implementation because it provides a lightweight relational database suitable for the project.

---

# 🔌 REST API

## Health Check

```http
GET /health
```

Checks whether the API is running.

Example:

```json
{
    "status": "healthy"
}
```

---

## Authentication

### Register

```http
POST /auth/register
```

Creates a new user account.

### Login

```http
POST /auth/login
```

Authenticates a user and returns an access token.

---

## Student APIs

```http
POST   /students/
GET    /students/
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}
GET    /students/stats
```

Student endpoints require authentication.

The API also supports student filtering, sorting, pagination, validation, and appropriate HTTP error responses.

---

## AI Chatbot

```http
POST /chat/
```

Accepts a natural-language question and returns an AI-generated answer based on the available student database.

Example request:

```json
{
    "question": "How many students are in the database?"
}
```

Example response:

```json
{
    "answer": "There are 5 students in the database."
}
```

---

# 🌐 Frontend

The application includes a browser-based frontend built using:

* HTML
* CSS
* JavaScript

### Frontend pages

```text
index.html
login.html
register.html
dashboard.html
```

The dashboard provides:

* Student listing
* Student statistics
* Add student
* Edit student
* Delete student
* Student filtering
* Authentication handling
* AI chatbot interface

The frontend communicates with the FastAPI backend through REST API requests.

---

# 🧪 Testing

The project includes automated tests using **Pytest**.

The test suite covers:

* User authentication
* Student creation
* Student retrieval
* Student updating
* Student deletion
* Validation
* Duplicate email handling
* Not-found responses
* Protected endpoints

### Run the test suite

Activate the virtual environment and run:

```powershell
python -m pytest
```

### Current final test result

```text
17 passed, 1 warning
```

The warning is a dependency deprecation warning from the Starlette/AnyIO stack and does not indicate a test failure.

---

# 🐳 Docker

The backend is also configured for containerized execution using Docker.

## Build the Docker image

From the project root:

```powershell
docker build -t student-database-api .
```

## Run the container

```powershell
docker run -p 8000:8000 --env-file .env student-database-api
```

The API can then be accessed at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Docker configuration has been tested as part of the final project preparation.

---

# 📁 Project Structure

```text
student-database-backend/
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
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── auth.js
│       └── dashboard.js
│
├── DOCS/
│   └── architecture_decision.md
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_students.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Vector Database Research and Selection

### Requirement

The project instructions require research into suitable vector databases and a technical justification for the selected option. The selection should consider integration, similarity search, scalability, development complexity, cost/free-tier availability, and compatibility with the project architecture.

### Options Considered

| Option       | Strengths                                                                                                                                                | Limitations                                                                                                                                        | Suitability                                                    |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **FAISS**    | Efficient dense-vector similarity search, strong Python support, lightweight for local development, supports multiple index types and similarity metrics | Primarily a vector-search library rather than a complete hosted database service; application code must handle persistence and metadata separately | High for this project's future local semantic-search extension |
| **Chroma**   | Developer-friendly vector storage and retrieval, suitable for local embedding and RAG experimentation                                                    | Adds another persistence and retrieval component that is unnecessary for the current structured student-data queries                               | Good for RAG experimentation                                   |
| **Pinecone** | Managed vector database with hosted infrastructure and scalable similarity search                                                                        | Adds an external cloud dependency and is unnecessary for the current small local project                                                           | Good for production-scale hosted semantic search               |

### Selected Option: FAISS

**FAISS (Facebook AI Similarity Search)** is selected as the vector-search technology for the future semantic-search extension of this project.

FAISS provides efficient similarity search and clustering of dense vectors and has Python support. It supports multiple index structures and similarity methods, including L2 distance and inner-product search. Cosine similarity can also be implemented by normalizing vectors before inner-product search.

### Technical Justification

FAISS was selected for the following reasons:

1. **Python compatibility**
   FAISS has Python support and can be incorporated into a Python-based AI application.

2. **Similarity search**
   It is designed for efficient similarity search over dense vector representations, which makes it suitable for future semantic-search functionality.

3. **Development simplicity**
   FAISS can be used locally without requiring a separate hosted database service, which keeps development relatively simple.

4. **Cost and open-source availability**
   FAISS is available as open-source software, making it suitable for a low-cost student project and local experimentation.

5. **Search scalability**
   FAISS provides different index structures that can support larger vector collections as the semantic-search dataset grows.

6. **Future RAG compatibility**
   FAISS can be used as the retrieval layer in a future Retrieval-Augmented Generation (RAG) architecture together with embeddings and Gemini.

### Why FAISS Is Not Integrated Into the Current Chatbot

The current Student Database application primarily contains structured relational information such as:

* Student name
* Email
* Phone
* Department
* Course
* Semester
* CGPA

Questions such as student counts, CGPA information, department information, filtering, and sorting are better handled through SQL queries against the SQLite database rather than semantic vector search.

Therefore, the current chatbot uses **SQL-based retrieval** for structured student information.

FAISS is selected as a **future extension** for semantic search over unstructured information such as:

* College policies
* Student handbooks
* Scholarship documents
* Course descriptions
* University notices
* PDF and text documents

This approach avoids adding unnecessary complexity to the current application while keeping the architecture ready for future semantic-search functionality.

### Future Hybrid Architecture

```text
User Question
      |
      v
   LangGraph
      |
      +--------------------+
      |                    |
      v                    v
 SQL / SQLite            FAISS
      |                    |
 Structured Data       Semantic Search
      |                    |
      +---------+----------+
                |
                v
             Gemini
                |
                v
          Final Response
```

In the current implementation, the SQL/SQLite retrieval path is used. FAISS is documented as the selected vector-search technology for a future semantic-search and document-retrieval extension.


---

# 🔒 Security

The application uses multiple security mechanisms:

* Password hashing
* JWT authentication
* Protected student endpoints
* Protected chatbot endpoint
* Environment variables for sensitive configuration
* `.env` excluded from Git
* Database files excluded from Git
* `.venv` excluded from Git

The Gemini API key is stored in the environment and is not included in the source code or Git repository.

---

# ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./student_database.db
GEMINI_API_KEY=your_gemini_api_key
```

Never commit the actual `.env` file or API key to GitHub.

A `.env.example` file is provided as a template.

---

# 🚀 Installation & Local Setup

## 1. Clone the repository

```powershell
git clone https://github.com/maheshsahu13/student-database-backend.git
```

Move into the project directory:

```powershell
cd student-database-backend
```

---

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

---

## 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./student_database.db
GEMINI_API_KEY=your_gemini_api_key
```

---

## 6. Start the backend

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

The Swagger interface can be used to inspect and test the available REST API endpoints.

---

# 💬 Example AI Queries

The chatbot can process natural-language questions related to available student data.

Examples:

```text
How many students are in the database?
```

```text
Which students have a CGPA above 8?
```

```text
What is the CGPA of Rahul?
```

```text
Which department has students?
```

```text
Show me the students in CSE.
```

The chatbot uses the available database information when generating responses.

---

# 🔄 Application Flow

The overall application flow is:

```text
User
 |
 v
Frontend
 |
 +--------------------+
 |                    |
 v                    v
Login/Register      Dashboard
 |                    |
 v                    |
JWT Authentication   |
 |                    |
 +----------+---------+
            |
            v
         FastAPI
            |
      +-----+------+
      |            |
      v            v
   SQLite       AI Chat
                   |
                   v
               LangGraph
                   |
                   v
            Student Retrieval
                   |
                   v
                Gemini
                   |
                   v
              AI Response
```

---

# 🛠️ Technology Stack

| Category             | Technologies          |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Backend Framework    | FastAPI               |
| Database             | SQLite                |
| ORM                  | SQLAlchemy            |
| Validation           | Pydantic              |
| Authentication       | JWT                   |
| Password Security    | Password Hashing      |
| AI Model             | Google Gemini         |
| AI Workflow          | LangGraph             |
| AI Framework         | LangChain             |
| Frontend             | HTML, CSS, JavaScript |
| Testing              | Pytest                |
| Containerization     | Docker                |
| Version Control      | Git                   |
| Repository           | GitHub                |

---

# 📈 Future Improvements

Possible future improvements include:

* Vector database integration
* Retrieval-Augmented Generation (RAG)
* Semantic search over college documents
* Student document ingestion
* Advanced AI query routing
* Improved chatbot conversation memory
* Role-based access control
* Production database such as PostgreSQL
* Cloud deployment
* Monitoring and logging
* Improved frontend design
* Additional analytics and reporting

These features are considered future extensions and are not required for the current implementation.

---

# 📊 Project Status

The current version includes:

* ✅ Full student CRUD management
* ✅ SQLite database
* ✅ SQLAlchemy integration
* ✅ REST API
* ✅ User registration and login
* ✅ JWT authentication
* ✅ Password hashing
* ✅ Protected student APIs
* ✅ Student filtering
* ✅ Pagination
* ✅ Sorting
* ✅ Student statistics
* ✅ Frontend dashboard
* ✅ Gemini AI integration
* ✅ LangGraph workflow
* ✅ AI student database chatbot
* ✅ Protected chatbot endpoint
* ✅ Automated tests
* ✅ Docker configuration
* ✅ Architecture documentation
* ✅ Environment variable configuration
* ✅ Git/GitHub version control

## Final Verification

The application has been tested across the major user flows, including:

```text
Registration
     ↓
Login
     ↓
Dashboard
     ↓
Student CRUD
     ↓
Statistics / Filtering
     ↓
AI Chatbot
     ↓
Database Retrieval
     ↓
Gemini Response
```

The automated test suite currently passes:

```text
17 passed
```

---

# 👨‍💻 Author

**Mahesh Sahu**

B.Tech Computer Engineering
Odisha University of Technology and Research (OUTR), Bhubaneswar

---

# 📄 License

This project is developed for educational and project submission purposes.

