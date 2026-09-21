const API_URL = "http://127.0.0.1:8000";


// ===============================
// REGISTER
// ===============================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("registerUsername").value;

        const email =
            document.getElementById("registerEmail").value;

        const password =
            document.getElementById("registerPassword").value;

        const message =
            document.getElementById("registerMessage");

        try {

            const response = await fetch(
                `${API_URL}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username: username,
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (response.ok) {

                message.textContent =
                    "Registration successful! Redirecting to login...";

                message.style.color = "green";

                setTimeout(function () {
                    window.location.href = "login.html";
                }, 1500);

            } else {

                message.textContent =
                    data.detail || "Registration failed.";

                message.style.color = "red";
            }

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to the server.";

            message.style.color = "red";
        }

    });
}


// ===============================
// LOGIN
// ===============================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;

        const message =
            document.getElementById("loginMessage");

        try {

            /*
             Your FastAPI login endpoint uses
             OAuth2PasswordRequestForm.

             Therefore we MUST send form data,
             NOT JSON.
            */

            const formData = new URLSearchParams();

            formData.append("username", username);
            formData.append("password", password);

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body: formData
                }
            );

            const data = await response.json();

            if (response.ok) {

                /*
                 Save JWT token in browser storage.
                */

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

                localStorage.setItem(
                    "username",
                    username
                );

                message.textContent =
                    "Login successful! Redirecting...";

                message.style.color = "green";

                setTimeout(function () {
                    window.location.href =
                        "dashboard.html";
                }, 1000);

            } else {

                message.textContent =
                    data.detail || "Login failed.";

                message.style.color = "red";
            }

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to the server.";

            message.style.color = "red";
        }

    });
}