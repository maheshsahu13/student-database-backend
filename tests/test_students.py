def get_auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "username": "studenttester",
            "email": "studenttester@example.com",
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "studenttester",
            "password": "TestPassword123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_students_requires_authentication(client):
    response = client.get("/students/")

    assert response.status_code == 401


def test_create_student(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Test Student",
            "email": "student1@example.com",
            "phone": "9876543210",
            "department": "Computer Engineering",
            "course": "B.Tech",
            "semester": 4,
            "cgpa": 9.03
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Student"
    assert data["email"] == "student1@example.com"
    assert data["department"] == "Computer Engineering"
    assert data["semester"] == 4


def test_get_students(client):
    headers = get_auth_headers(client)

    client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Student One",
            "email": "studentone@example.com",
            "phone": "9876543210",
            "department": "Computer Engineering",
            "course": "B.Tech",
            "semester": 4,
            "cgpa": 8.5
        }
    )

    response = client.get(
        "/students/",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Student One"


def test_get_student_by_id(client):
    headers = get_auth_headers(client)

    create_response = client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Individual Student",
            "email": "individual@example.com",
            "phone": "9876543210",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 3,
            "cgpa": 8.8
        }
    )

    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == student_id
    assert response.json()["name"] == "Individual Student"


def test_update_student(client):
    headers = get_auth_headers(client)

    create_response = client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Old Name",
            "email": "update@example.com",
            "phone": "9876543210",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 2,
            "cgpa": 8.0
        }
    )

    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        headers=headers,
        json={
            "name": "Updated Name",
            "email": "update@example.com",
            "phone": "9999999999",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 3,
            "cgpa": 8.7
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["semester"] == 3
    assert response.json()["cgpa"] == 8.7


def test_delete_student(client):
    headers = get_auth_headers(client)

    create_response = client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Delete Student",
            "email": "delete@example.com",
            "phone": "9876543210",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 1,
            "cgpa": 7.5
        }
    )

    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == student_id

    get_response = client.get(
        f"/students/{student_id}",
        headers=headers
    )

    assert get_response.status_code == 404


def test_student_not_found(client):
    headers = get_auth_headers(client)

    response = client.get(
        "/students/9999",
        headers=headers
    )

    assert response.status_code == 404


def test_duplicate_student_email(client):
    headers = get_auth_headers(client)

    student_data = {
        "name": "First Student",
        "email": "duplicate@example.com",
        "phone": "9876543210",
        "department": "CSE",
        "course": "B.Tech",
        "semester": 4,
        "cgpa": 8.5
    }

    first_response = client.post(
        "/students/",
        headers=headers,
        json=student_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/students/",
        headers=headers,
        json=student_data
    )

    assert second_response.status_code == 409


def test_invalid_student_data(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/students/",
        headers=headers,
        json={
            "name": "Invalid Student",
            "email": "invalid@example.com",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 0
        }
    )

    assert response.status_code == 422


def test_student_filtering(client):
    headers = get_auth_headers(client)

    client.post(
        "/students/",
        headers=headers,
        json={
            "name": "CSE Student",
            "email": "cse@example.com",
            "department": "CSE",
            "course": "B.Tech",
            "semester": 4,
            "cgpa": 9.0
        }
    )

    client.post(
        "/students/",
        headers=headers,
        json={
            "name": "ECE Student",
            "email": "ece@example.com",
            "department": "ECE",
            "course": "B.Tech",
            "semester": 4,
            "cgpa": 8.0
        }
    )

    response = client.get(
        "/students/?department=CSE",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["department"] == "CSE"


def test_student_pagination(client):
    headers = get_auth_headers(client)

    for i in range(3):
        client.post(
            "/students/",
            headers=headers,
            json={
                "name": f"Student {i}",
                "email": f"pagination{i}@example.com",
                "department": "CSE",
                "course": "B.Tech",
                "semester": 4,
                "cgpa": 8.0
            }
        )

    response = client.get(
        "/students/?page=1&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_student_sorting(client):
    headers = get_auth_headers(client)

    names = ["Zebra Student", "Alpha Student", "Middle Student"]

    for i, name in enumerate(names):
        client.post(
            "/students/",
            headers=headers,
            json={
                "name": name,
                "email": f"sorting{i}@example.com",
                "department": "CSE",
                "course": "B.Tech",
                "semester": 4,
                "cgpa": 8.0
            }
        )

    response = client.get(
        "/students/?sort_by=name&sort_order=asc",
        headers=headers
    )

    assert response.status_code == 200

    returned_names = [
        student["name"] for student in response.json()
    ]

    assert returned_names == [
        "Alpha Student",
        "Middle Student",
        "Zebra Student"
    ]


def test_student_statistics(client):
    headers = get_auth_headers(client)

    students = [
        ("Student A", "a@example.com", "CSE"),
        ("Student B", "b@example.com", "CSE"),
        ("Student C", "c@example.com", "ECE")
    ]

    for name, email, department in students:
        client.post(
            "/students/",
            headers=headers,
            json={
                "name": name,
                "email": email,
                "department": department,
                "course": "B.Tech",
                "semester": 4,
                "cgpa": 8.0
            }
        )

    response = client.get(
        "/students/stats",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_students"] == 3
    assert data["total_departments"] == 2
    assert data["students_by_department"]["CSE"] == 2
    assert data["students_by_department"]["ECE"] == 1