# Architecture Decision

## Vector Database Decision

### Decision

The current version of the Student Database Application uses SQLite and SQL-based retrieval for structured student information.

A vector database is not included in the current implementation.

### Reason

The primary data stored by the application is structured student information such as:

- Student ID
- Name
- Email
- Phone
- Department
- Course
- Semester
- CGPA

These fields are better handled using traditional relational database queries.

For example:

- Finding students with CGPA above a certain value
- Filtering students by department
- Finding students by course
- Counting students
- Retrieving a student by ID

These operations do not require semantic vector search.

### Current AI Architecture

```text
User
  |
  v
FastAPI Chat Endpoint
  |
  v
LangGraph
  |
  +----------------------+
  |                      |
  v                      v
SQLite Database       Gemini
  |                      |
  +----------+-----------+
             |
             v
        AI Response