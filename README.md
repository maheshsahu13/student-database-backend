# Student Database Application System

A full-stack student database application built with **FastAPI, SQLite, SQLAlchemy, JWT authentication, HTML/CSS/JavaScript, Google Gemini, LangChain, LangGraph, and ChromaDB**.

The system provides secure student management through REST APIs and a web-based frontend, along with an AI chatbot capable of answering structured, semantic, and hybrid questions about the student database.

---

## 📌 Project Overview

The **Student Database Application System** is designed to manage student information through a secure and scalable backend API.

The application supports:

- Student CRUD operations
- User registration and authentication
- JWT-based authorization
- Input validation
- Filtering and pagination
- Sorting
- Student statistics
- Interactive API documentation
- Web frontend
- AI-powered natural-language chatbot
- Google Gemini integration
- LangChain and LangGraph
- ChromaDB vector database
- Semantic search
- Structured SQL retrieval
- Hybrid retrieval
- Retrieval-Augmented Generation (RAG)
- Automatic synchronization between SQLite and ChromaDB
- Automated testing

---

# 🚀 Features

## 1. Student Management

The application provides complete CRUD functionality for students.

### Create

Add a new student with:

- Name
- Email
- Phone
- Department
- Course
- Semester
- CGPA

### Read

Retrieve:

- Individual student
- All students
- Filtered students
- Paginated students
- Sorted students
- Student statistics

### Update

Modify existing student information.

### Delete

Remove a student from the database.

---

# 🔐 Authentication

The application uses JWT-based authentication.

Users can:

- Register an account
- Login
- Receive an access token
- Access protected endpoints
- Retrieve their current user information

Student management endpoints are protected and require a valid JWT token.

### Authentication Endpoints

```text
POST /auth/register
POST /auth/login
GET  /auth/me
👨‍🎓 Student API

Main student endpoints:

GET    /students/
GET    /students/{student_id}
POST   /students/
PUT    /students/{student_id}
DELETE /students/{student_id}

Additional functionality includes:

GET /students/department/{department}
GET /students/course/{course}
GET /students/stats

The API also supports:

Pagination
Sorting
Filtering
Validation
Duplicate-email detection
Not-found handling
🤖 AI Chatbot

The project includes an AI-powered chatbot for interacting with the student database using natural language.

The chatbot uses:

Google Gemini
LangChain
LangGraph
ChromaDB
Gemini Embeddings
SQLite
Retrieval-Augmented Generation

The chatbot endpoint is:

POST /chat/

Example request:

{
  "question": "Which students have a CGPA above 8.5?"
}

Example response:

{
  "answer": "Aarav Sharma has a CGPA of 10.0..."
}
🧠 AI Retrieval Architecture

The chatbot does not rely on a single retrieval method.

It determines the appropriate retrieval strategy based on the user's question.

                    User Question
                          │
                          ▼
                    /chat/ endpoint
                          │
                          ▼
                    LangGraph
                          │
                          ▼
                Question Classification
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
          Structured    Semantic     Hybrid
              │           │           │
              ▼           ▼           ▼
           SQLite      ChromaDB    SQLite +
                                    ChromaDB
              │           │           │
              └───────────┼───────────┘
                          ▼
                       Context
                          │
                          ▼
                     Google Gemini
                          │
                          ▼
                    Final Answer
🗃️ Structured Retrieval

Structured retrieval is used for questions that require exact database values.

Examples:

Who has the highest CGPA?

Which students have CGPA above 8.5?

How many students are there?

Which students belong to the CSE department?

For these queries, SQLite is treated as the source of truth.

This helps ensure that exact numerical and database-related answers are generated from the actual student records.

🔎 Semantic Retrieval

Semantic retrieval is used for natural-language questions where keyword matching alone may not be sufficient.

The project uses:

ChromaDB
Gemini Embeddings
Cosine/distance-based semantic similarity retrieval

Example:

Who is studying computer science?

Which students have strong academic performance?

Find students with an academic profile similar to Rahul.

The question is converted into an embedding and compared with student embeddings stored in ChromaDB.

🔀 Hybrid Retrieval

Hybrid retrieval combines structured and semantic information.

Example:

Which CSE students have a CGPA above 8.5 and strong academic performance?

This type of question can require:

Exact CGPA information from SQLite
Department information from SQLite
Semantic interpretation of "strong academic performance" using vector retrieval

The system therefore combines both retrieval methods before generating the final answer.

📚 Retrieval-Augmented Generation (RAG)

The chatbot follows a Retrieval-Augmented Generation architecture.

Question
   │
   ▼
Question Classification
   │
   ▼
Information Retrieval
   │
   ├── SQLite
   │
   └── ChromaDB
   │
   ▼
Retrieved Context
   │
   ▼
Google Gemini
   │
   ▼
Grounded Natural-Language Answer

The Gemini model receives retrieved database information as context and generates the final response.

The system is instructed to:

Use provided information
Avoid inventing student information
Use SQLite for exact values
Use semantic retrieval for conceptual relationships
Combine structured and semantic information for hybrid questions
#🧮 Vector Database

# 🔬 Vector Database Research and Selection

The project uses **ChromaDB** as its vector database for semantic retrieval and the RAG architecture.

Before selecting the vector database, different approaches were considered based on the requirements of the project, including ease of integration, semantic similarity search, development complexity, cost, scalability, and compatibility with the existing Python/FastAPI architecture.

## Vector Database Options Considered

The main options considered were:

- ChromaDB
- FAISS
- Cloud-based vector database services

The project requires a vector database that can support semantic search over student information while remaining simple and cost-effective during development.

## Why ChromaDB Was Selected

### 1. Easy Python Integration

ChromaDB provides a Python interface that integrates naturally with the existing FastAPI application.

The project is already implemented in Python, so ChromaDB can be used directly from the application's service layer without introducing a separate technology stack.

### 2. Semantic Similarity Search

The chatbot needs to answer natural-language questions that cannot always be handled effectively using traditional SQL queries.

For example:

```text
Who is studying computer science?

The project uses ChromaDB as its local vector database.

ChromaDB stores:

Student documents
Student embeddings
Student metadata

Example student document:

Student name: Aarav Sharma.
Email: aarav@example.com.
Department: CSE.
Course: Computer Science.
Semester: 6.
CGPA: 10.0.

This information is converted into a vector embedding using the Gemini embedding model.

🔢 Embeddings

The project uses Google's Gemini embedding model:

gemini-embedding-001

The embedding service converts text into numerical vectors.

Example:

Student Information
        │
        ▼
Gemini Embedding Model
        │
        ▼
Numerical Vector
        │
        ▼
ChromaDB

The generated embeddings are stored locally in ChromaDB for semantic retrieval.

🔄 SQLite and ChromaDB Synchronization

SQLite remains the primary source of truth.

ChromaDB acts as the semantic retrieval layer.

Whenever a student is created or updated, the corresponding vector record is updated.

Whenever a student is deleted, the corresponding ChromaDB record is also deleted.

              SQLite
          Source of Truth
                │
                │
        ┌───────┴────────┐
        │                │
      Create           Update
        │                │
        ▼                ▼
     ChromaDB         ChromaDB
     Upsert           Upsert
        │                │
        └───────┬────────┘
                │
             Delete
                │
                ▼
             ChromaDB
              Delete

This keeps the semantic search index synchronized with the student database.

📥 Initial Vector Indexing

For existing students, the project includes:

index_students.py

Run:

python index_students.py

This script:

Connects to SQLite
Retrieves existing students
Creates a text representation for each student
Generates embeddings
Stores them in ChromaDB

Example output:

Found 5 students in SQLite.
Indexed: Rahul (ID: 1)
Indexed: Mohit (ID: 2)
Indexed: Deepak (ID: 3)
Indexed: Aarav Sharma (ID: 4)
Indexed: Student A (ID: 5)

All students indexed successfully!
🗄️ Database

The project uses SQLite.

SQLite was selected because it is:

Lightweight
Local
Easy to configure
Suitable for this project
Zero-cost
Easy to use during development

SQLAlchemy is used as the ORM.

Student Model

The student table contains:

id
name
email
phone
department
course
semester
cgpa
🌐 Frontend

The project includes a web-based frontend built using:

HTML
CSS
JavaScript

The frontend provides:

Login page
Registration page
Dashboard
Student table
Add student
Edit student
Delete student
Statistics
Authentication handling
AI chatbot integration

JWT access tokens are stored on the client side for authenticated API requests.

📊 Dashboard

The dashboard provides student management functionality through a browser interface.

The dashboard includes:

Student statistics
Student records
Add student form
Edit functionality
Delete functionality
Authentication state
AI chatbot interaction
🧪 Testing

The project uses pytest for automated testing.

The test suite covers:

Student CRUD
Authentication
Validation
Error handling
Student retrieval
Vector synchronization
API behavior

Run the complete test suite:

python -m pytest -q

Current verified test result:

21 passed, 1 warning

The warning is a dependency deprecation warning and does not cause the tests to fail.

✅ Verified AI Functionality

The AI system has been tested with different retrieval strategies.

Structured Query

Example:

Who has the highest CGPA?

The system retrieves structured information from SQLite.

Semantic Query

Example:

Who is studying computer science?

The system performs semantic retrieval using ChromaDB.

Hybrid Query

Example:

Which CSE students have a CGPA above 8.5 and strong academic performance?

The system combines:

Structured SQLite information
Semantic ChromaDB information

before sending the retrieved context to Gemini.

🛠️ Technology Stack
Backend
Python
FastAPI
Uvicorn
SQLAlchemy
SQLite
Authentication
JWT
Password hashing
OAuth2 Bearer authentication
AI
Google Gemini
Gemini Embeddings
LangChain
LangGraph
Vector Database
ChromaDB
Frontend
HTML
CSS
JavaScript
Testing
Pytest
Development Tools
Git
GitHub
VS Code
PowerShell
Deployment Preparation
Dockerfile
.dockerignore
📁 Project Structure
student-database-backend/
│
├── app/
│   ├── ai/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── prompts.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── crud/
│   │   └── student.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── student.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── students.py
│   │
│   ├── schemas/
│   │   ├── student.py
│   │   └── user.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   ├── jwt.py
│   │   └── password.py
│   │
│   └── services/
│       ├── embedding_service.py
│       ├── retrieval_service.py
│       ├── student_vector_service.py
│       └── vector_store.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── css/
│   └── js/
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_students.py
│   └── test_vector_sync.py
│
├── index_students.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
└── student_database.db

Database files and ChromaDB data are excluded from Git through .gitignore.

🔑 Environment Variables

Create a .env file in the project root.

Example:

DATABASE_URL=sqlite:///./student_database.db
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key

Do not commit .env to GitHub.

The .gitignore file excludes:

.env
*.db
chroma_db/
.venv/
__pycache__/
*.pyc
⚙️ Installation
1. Clone the Repository
git clone https://github.com/maheshsahu13/student-database-backend.git

Move into the project directory:

cd student-database-backend
🐍 2. Create Virtual Environment

Create the virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1
📦 3. Install Dependencies

Install the required packages:

pip install -r requirements.txt
🔐 4. Configure Environment Variables

Create:

.env

Add:

DATABASE_URL=sqlite:///./student_database.db
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key

Replace the placeholder values with your actual credentials.

▶️ 5. Run the Backend

Start the FastAPI application:

python -m uvicorn app.main:app --reload

The backend will normally be available at:

http://127.0.0.1:8000
📖 API Documentation

FastAPI automatically provides Swagger UI.

Open:

http://127.0.0.1:8000/docs

The ReDoc documentation is available at:

http://127.0.0.1:8000/redoc

Swagger can be used to test:

Authentication
Student CRUD
Filters
Pagination
Sorting
Statistics
AI chatbot
🧠 6. Build the Vector Index

After configuring the Gemini API key and ensuring student records exist in SQLite, run:

python index_students.py

This creates or updates the local:

chroma_db/

directory.

🧪 7. Run Tests

Run:

python -m pytest -q

Expected current result:

21 passed
🔄 Application Flow

The complete application flow is:

                ┌───────────────────┐
                │     Frontend      │
                │ HTML/CSS/JS       │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │     FastAPI       │
                │      Backend      │
                └─────────┬─────────┘
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
       Authentication   Students       Chat
             │            │             │
             ▼            ▼             ▼
           JWT         SQLite       LangGraph
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                            ▼                   ▼
                         SQLite             ChromaDB
                            │                   │
                            └─────────┬─────────┘
                                      │
                                      ▼
                                Gemini Model
                                      │
                                      ▼
                                AI Response
🔒 Security

The project implements several security measures:

JWT authentication
Password hashing
Protected student endpoints
Protected chatbot endpoint
Environment-based secret configuration
.env excluded from Git
Database files excluded from Git
Input validation using Pydantic

Sensitive credentials should never be hard-coded into source code.

⚠️ Error Handling

The API handles common error conditions including:

404

Student not found.

409

Duplicate email.

422

Invalid request data.

401

Unauthorized request or missing/invalid authentication.

📌 Example API Usage
Register
POST /auth/register

Example:

{
  "username": "student1",
  "email": "student1@example.com",
  "password": "password123"
}
Login
POST /auth/login

The login response provides a JWT access token.

Use the token to authorize protected API requests.

Create Student
POST /students/

Example:

{
  "name": "Aarav Sharma",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "department": "CSE",
  "course": "Computer Science",
  "semester": 6,
  "cgpa": 10.0
}
AI Chat
POST /chat/

Example:

{
  "question": "Which CSE students have strong academic performance?"
}
💬 Example AI Questions

The chatbot can handle different types of questions.

Exact Database Questions
Who has the highest CGPA?
Which students have CGPA above 8.5?
How many students are in the database?
Semantic Questions
Who is studying computer science?
Which students have strong academic performance?
Find students with a similar academic profile to Rahul.
Hybrid Questions
Which CSE students have a CGPA above 8.5 and strong academic performance?
Find students from the CSE department who perform strongly academically.
📈 Current Project Status

The project currently includes:

 FastAPI backend
 SQLite database
 SQLAlchemy ORM
 Student CRUD
 Data validation
 Filtering
 Pagination
 Sorting
 Student statistics
 Swagger API documentation
 User registration
 JWT authentication
 Protected student routes
 Automated testing
 Web frontend
 Dashboard
 Gemini API integration
 LangChain integration
 LangGraph integration
 AI chatbot
 ChromaDB vector database
 Gemini embeddings
 Semantic search
 Structured retrieval
 Hybrid retrieval
 RAG architecture
 SQLite ↔ ChromaDB synchronization
 Initial vector indexing script
 Vector synchronization tests
 Docker deployment configuration
🐳 Docker

A Dockerfile and .dockerignore are included as part of the project's deployment preparation.

The intended Docker architecture is:

Docker Container
       │
       ▼
   FastAPI App
       │
       ├── SQLite
       │
       ├── ChromaDB
       │
       └── Gemini API

Docker configuration is included for deployment preparation.

Docker execution has not been validated locally in the current development environment, so Docker should be considered deployment-ready configuration rather than a locally verified deployment.

🔮 Future Improvements

Possible future improvements include:

Production cloud deployment
Managed database
Improved frontend UI/UX
Role-based access control
Advanced analytics
More sophisticated query classification
Better hybrid retrieval strategies
Conversation history
Streaming AI responses
More comprehensive AI evaluation
Automated deployment pipeline
Cloud-hosted vector database
Production monitoring and logging
🧩 Design Principles

The project follows several important architectural principles.

SQLite as Source of Truth

Exact student information is maintained in SQLite.

ChromaDB as Semantic Layer

ChromaDB is used for semantic similarity and natural-language retrieval.

Gemini as Generation Layer

Gemini generates natural-language responses using retrieved context.

LangGraph as Orchestration Layer

LangGraph controls the chatbot workflow:

Question
   ↓
Classification
   ↓
Retrieval
   ↓
Context
   ↓
Generation
   ↓
Answer

This separation makes the system easier to maintain and extend.

📚 Main Dependencies

The primary project dependencies include:

chromadb==1.5.9
fastapi==0.141.1
google-genai==2.24.0
langchain==1.4.2
langchain-core==1.6.4
langchain-google-genai==4.4.0
langchain-protocol==0.0.19
langgraph==1.2.12
langgraph-checkpoint==4.2.0
langgraph-prebuilt==1.1.0
langgraph-sdk==0.4.5
pytest==9.1.1
SQLAlchemy==2.0.54
uvicorn==0.53.0
🏗️ Architecture Summary

The overall system can be summarized as:

                       STUDENT DATABASE SYSTEM
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
             ▼                                     ▼
         Frontend                              FastAPI
      HTML/CSS/JS                              Backend
                                                   │
                         ┌─────────────────────────┼────────────────────────┐
                         │                         │                        │
                         ▼                         ▼                        ▼
                    Authentication             Student API              Chat API
                         │                         │                        │
                         ▼                         ▼                        ▼
                        JWT                    SQLite DB              LangGraph
                                                                          │
                                                         ┌────────────────┼───────────────┐
                                                         │                │               │
                                                         ▼                ▼               ▼
                                                      SQLite          ChromaDB         Gemini
                                                        │                │               │
                                                        └────────────────┴───────────────┘
                                                                         │
                                                                         ▼
                                                                    AI Response
🎯 Project Objective

The objective of this project is to build a complete student database system that combines traditional database management with modern AI-based natural-language interaction.

The system demonstrates how:

REST APIs
Relational databases
Authentication
Frontend applications
Large Language Models
Embeddings
Vector databases
Semantic search
Retrieval-Augmented Generation
Workflow orchestration

can be combined into a single application.

👤 Author

Mahesh Sahu

B.Tech Computer Engineering

📄 License

This project is developed for educational and portfolio purposes.

