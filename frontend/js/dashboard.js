const API_URL = "http://127.0.0.1:8000";


// ========================================
// CHECK LOGIN
// ========================================

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "login.html";
}


// ========================================
// AUTHORIZATION HEADER
// ========================================

function getAuthHeaders() {

    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };

}


// ========================================
// DISPLAY USERNAME
// ========================================

const username = localStorage.getItem("username");

const welcomeUser =
    document.getElementById("welcomeUser");

if (welcomeUser && username) {
    welcomeUser.textContent = `Welcome, ${username}`;
}


// ========================================
// LOGOUT
// ========================================

const logoutButton =
    document.getElementById("logoutButton");

if (logoutButton) {

    logoutButton.addEventListener("click", function () {

        localStorage.removeItem("access_token");
        localStorage.removeItem("username");

        window.location.href = "login.html";

    });

}


// ========================================
// LOAD STUDENT STATISTICS
// ========================================

async function loadStatistics() {

    try {

        const response = await fetch(
            `${API_URL}/students/stats`,
            {
                method: "GET",
                headers: getAuthHeaders()
            }
        );

        if (response.status === 401) {

            logoutUser();
            return;

        }

        if (!response.ok) {

            throw new Error("Failed to load statistics");

        }

        const data = await response.json();

        document.getElementById(
            "totalStudents"
        ).textContent = data.total_students;

        document.getElementById(
            "totalDepartments"
        ).textContent = data.total_departments;

        document.getElementById(
            "totalCourses"
        ).textContent = data.total_courses;

    } catch (error) {

        console.error(
            "Statistics error:",
            error
        );

    }

}


// ========================================
// LOAD STUDENTS
// ========================================

async function loadStudents() {

    const tableBody =
        document.getElementById(
            "studentTableBody"
        );

    try {

        tableBody.innerHTML = `
            <tr>
                <td colspan="9">
                    Loading students...
                </td>
            </tr>
        `;

        const response = await fetch(
            `${API_URL}/students/?page=1&limit=100&sort_by=id&sort_order=asc`,
            {
                method: "GET",
                headers: getAuthHeaders()
            }
        );

        if (response.status === 401) {

            logoutUser();
            return;

        }

        if (!response.ok) {

            throw new Error("Failed to load students");

        }

        const students = await response.json();

        displayStudents(students);

    } catch (error) {

        console.error(
            "Student loading error:",
            error
        );

        tableBody.innerHTML = `
            <tr>
                <td colspan="9">
                    Unable to load students.
                </td>
            </tr>
        `;

    }

}


// ========================================
// DISPLAY STUDENTS
// ========================================

function displayStudents(students) {

    const tableBody =
        document.getElementById(
            "studentTableBody"
        );

    if (students.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="9">
                    No students found.
                </td>
            </tr>
        `;

        return;
    }


    tableBody.innerHTML = "";


    students.forEach(function (student) {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>${student.id}</td>

            <td>${student.name}</td>

            <td>${student.email}</td>

            <td>${student.phone || "-"}</td>

            <td>${student.department}</td>

            <td>${student.course}</td>

            <td>${student.semester}</td>

            <td>${student.cgpa ?? "-"}</td>

            <td>

                <button
                    class="edit-button"
                    data-id="${student.id}"
                >
                    Edit
                </button>

                <button
                    class="delete-button"
                    onclick="deleteStudent(${student.id})"
                >
                    Delete
                </button>

            </td>

        `;


        tableBody.appendChild(row);


        // EDIT BUTTON

        const editButton =
            row.querySelector(".edit-button");


        editButton.addEventListener(
            "click",
            function () {

                const studentId =
                    Number(this.dataset.id);

                editStudent(studentId);

            }
        );

    });

}


// ========================================
// ADD STUDENT
// ========================================

const studentForm =
    document.getElementById("studentForm");


if (studentForm) {

    studentForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const studentData = {

                name:
                    document.getElementById(
                        "studentName"
                    ).value,

                email:
                    document.getElementById(
                        "studentEmail"
                    ).value,

                phone:
                    document.getElementById(
                        "studentPhone"
                    ).value || null,

                department:
                    document.getElementById(
                        "studentDepartment"
                    ).value,

                course:
                    document.getElementById(
                        "studentCourse"
                    ).value,

                semester:
                    Number(
                        document.getElementById(
                            "studentSemester"
                        ).value
                    ),

                cgpa:
                    document.getElementById(
                        "studentCgpa"
                    ).value === ""
                        ? null
                        : Number(
                            document.getElementById(
                                "studentCgpa"
                            ).value
                        )

            };


            const message =
                document.getElementById(
                    "studentMessage"
                );


            try {

                const response = await fetch(
                    `${API_URL}/students/`,
                    {
                        method: "POST",

                        headers:
                            getAuthHeaders(),

                        body:
                            JSON.stringify(
                                studentData
                            )
                    }
                );


                const data =
                    await response.json();


                if (response.status === 401) {

                    logoutUser();
                    return;

                }


                if (!response.ok) {

                    message.textContent =
                        data.detail ||
                        "Failed to add student.";

                    message.style.color =
                        "red";

                    return;

                }


                message.textContent =
                    "Student added successfully.";

                message.style.color =
                    "green";


                studentForm.reset();


                await loadStudents();

                await loadStatistics();


            } catch (error) {

                console.error(error);

                message.textContent =
                    "Unable to connect to the server.";

                message.style.color =
                    "red";

            }

        }
    );

}


// ========================================
// DELETE STUDENT
// ========================================

async function deleteStudent(studentId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this student?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/students/${studentId}`,
            {
                method: "DELETE",
                headers: getAuthHeaders()
            }
        );


        if (response.status === 401) {

            logoutUser();
            return;

        }


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Failed to delete student."
            );

            return;

        }


        alert(
            "Student deleted successfully."
        );


        await loadStudents();

        await loadStatistics();


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the server."
        );

    }

}


// ========================================
// EDIT STUDENT
// ========================================

// ========================================
// EDIT STUDENT
// ========================================

async function editStudent(studentId) {

    console.log("Opening edit form for student:", studentId);

    try {

        // Get the existing student data
        const response = await fetch(
            `${API_URL}/students/${studentId}`,
            {
                method: "GET",
                headers: getAuthHeaders()
            }
        );


        if (response.status === 401) {

            logoutUser();
            return;

        }


        if (!response.ok) {

            throw new Error(
                "Failed to load student information"
            );

        }


        const student =
            await response.json();


        // Create edit form
        const editForm =
            document.createElement("div");


        editForm.id = "editFormContainer";


        editForm.innerHTML = `

            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            ">

                <div style="
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    width: 90%;
                    max-width: 600px;
                    max-height: 90vh;
                    overflow-y: auto;
                ">

                    <h2>Edit Student</h2>

                    <form id="editStudentForm">

                        <label>Name</label>

                        <input
                            type="text"
                            id="editName"
                            value="${student.name}"
                            required
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>Email</label>

                        <input
                            type="email"
                            id="editEmail"
                            value="${student.email}"
                            required
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>Phone</label>

                        <input
                            type="text"
                            id="editPhone"
                            value="${student.phone || ""}"
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>Department</label>

                        <input
                            type="text"
                            id="editDepartment"
                            value="${student.department}"
                            required
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>Course</label>

                        <input
                            type="text"
                            id="editCourse"
                            value="${student.course}"
                            required
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>Semester</label>

                        <input
                            type="number"
                            id="editSemester"
                            value="${student.semester}"
                            min="1"
                            max="8"
                            required
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 15px;
                            "
                        >


                        <label>CGPA</label>

                        <input
                            type="number"
                            id="editCgpa"
                            value="${student.cgpa ?? ""}"
                            min="0"
                            max="10"
                            step="0.01"
                            style="
                                width:100%;
                                padding:10px;
                                margin:6px 0 20px;
                            "
                        >


                        <button
                            type="submit"
                            style="
                                padding:10px 20px;
                                margin-right:10px;
                                background:#2563eb;
                                color:white;
                                border:none;
                                border-radius:6px;
                                cursor:pointer;
                            "
                        >
                            Update Student
                        </button>


                        <button
                            type="button"
                            id="cancelEdit"
                            style="
                                padding:10px 20px;
                                background:#6b7280;
                                color:white;
                                border:none;
                                border-radius:6px;
                                cursor:pointer;
                            "
                        >
                            Cancel
                        </button>

                    </form>

                </div>

            </div>

        `;


        document.body.appendChild(editForm);


        // Cancel button

        document
            .getElementById("cancelEdit")
            .addEventListener(
                "click",
                function () {

                    editForm.remove();

                }
            );


        // Submit edited student

        document
            .getElementById("editStudentForm")
            .addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();


                    const studentData = {

                        name:
                            document.getElementById(
                                "editName"
                            ).value,

                        email:
                            document.getElementById(
                                "editEmail"
                            ).value,

                        phone:
                            document.getElementById(
                                "editPhone"
                            ).value || null,

                        department:
                            document.getElementById(
                                "editDepartment"
                            ).value,

                        course:
                            document.getElementById(
                                "editCourse"
                            ).value,

                        semester:
                            Number(
                                document.getElementById(
                                    "editSemester"
                                ).value
                            ),

                        cgpa:
                            document.getElementById(
                                "editCgpa"
                            ).value === ""
                                ? null
                                : Number(
                                    document.getElementById(
                                        "editCgpa"
                                    ).value
                                )

                    };


                    try {

                        const updateResponse =
                            await fetch(
                                `${API_URL}/students/${studentId}`,
                                {
                                    method: "PUT",

                                    headers:
                                        getAuthHeaders(),

                                    body:
                                        JSON.stringify(
                                            studentData
                                        )
                                }
                            );


                        if (
                            updateResponse.status === 401
                        ) {

                            logoutUser();
                            return;

                        }


                        const updateData =
                            await updateResponse.json();


                        if (!updateResponse.ok) {

                            alert(
                                updateData.detail ||
                                "Failed to update student."
                            );

                            return;

                        }


                        editForm.remove();


                        alert(
                            "Student updated successfully."
                        );


                        await loadStudents();

                        await loadStatistics();


                    } catch (error) {

                        console.error(error);

                        alert(
                            "Unable to connect to the server."
                        );

                    }

                }
            );


    } catch (error) {

        console.error(error);

        alert(
            "Unable to load student information."
        );

    }

}


// ========================================
// LOGOUT FUNCTION
// ========================================

function logoutUser() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "username"
    );

    window.location.href =
        "login.html";

}


// ========================================
// REFRESH BUTTON
// ========================================

const refreshButton =
    document.getElementById(
        "refreshButton"
    );


if (refreshButton) {

    refreshButton.addEventListener(
        "click",
        async function () {

            await loadStudents();

            await loadStatistics();

        }
    );

}


// ========================================
// INITIAL LOAD
// ========================================

loadStudents();

loadStatistics();

// ========================================
// AI CHATBOT
// ========================================

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const chatButton = document.getElementById("chatButton");

if (chatForm) {
    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const question = chatInput.value.trim();

        if (!question) {
            return;
        }

        // Show user's question
        addChatMessage(question, "user-message");

        // Clear input
        chatInput.value = "";

        // Disable button while AI is responding
        chatButton.disabled = true;
        chatButton.textContent = "Thinking...";

        // Show temporary loading message
        const loadingMessage = addChatMessage(
            "Thinking...",
            "bot-message"
        );

        try {
            const response = await fetch(
                `${API_URL}/chat/`,
                {
                    method: "POST",
                    headers: getAuthHeaders(),
                    body: JSON.stringify({
                        question: question
                    })
                }
            );

            // If token expired
            if (response.status === 401) {
                logoutUser();
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Failed to get AI response."
                );
            }

            // Replace "Thinking..." with AI answer
            loadingMessage.textContent = data.answer;

        } catch (error) {
            console.error("Chat error:", error);

            loadingMessage.textContent =
                "Unable to get a response from the AI assistant.";
        } finally {
            chatButton.disabled = false;
            chatButton.textContent = "Ask AI";
            chatInput.focus();
        }
    });
}


// ========================================
// ADD CHAT MESSAGE
// ========================================

function addChatMessage(message, className) {

    const messageElement = document.createElement("div");

    messageElement.className =
        `chat-message ${className}`;

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    // Automatically scroll to latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageElement;
}