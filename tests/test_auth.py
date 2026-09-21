def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "wrongpassuser",
            "email": "wrongpass@example.com",
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrongpassuser",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401