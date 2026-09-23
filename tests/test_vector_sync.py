from unittest.mock import MagicMock

from app.services.student_vector_service import StudentVectorService


def create_mock_student(
    student_id=11,
    name="Test Student",
    email="test@example.com",
    department="CSE",
    course="B.Tech",
    semester=4,
    cgpa=9.0,
):
    student = MagicMock()

    student.id = student_id
    student.name = name
    student.email = email
    student.phone = "9999999999"
    student.department = department
    student.course = course
    student.semester = semester
    student.cgpa = cgpa

    return student


def test_student_create_sync():
    service = StudentVectorService()
    service.vector_store = MagicMock()

    student = create_mock_student()

    service.index_student(student)

    service.vector_store.add_student.assert_called_once()

    call = service.vector_store.add_student.call_args

    assert call.kwargs["student_id"] == 11
    assert "Test Student" in call.kwargs["text"]
    assert "CSE" in call.kwargs["text"]
    assert "B.Tech" in call.kwargs["text"]
    assert call.kwargs["metadata"]["cgpa"] == 9.0


def test_student_update_sync():
    service = StudentVectorService()
    service.vector_store = MagicMock()

    updated_student = create_mock_student(
        name="Updated Student",
        course="Machine Learning",
        semester=5,
        cgpa=9.6,
    )

    service.index_student(updated_student)

    service.vector_store.add_student.assert_called_once()

    call = service.vector_store.add_student.call_args

    assert call.kwargs["student_id"] == 11
    assert "Updated Student" in call.kwargs["text"]
    assert "Machine Learning" in call.kwargs["text"]
    assert "Semester: 5" in call.kwargs["text"]
    assert "CGPA: 9.6" in call.kwargs["text"]

    assert call.kwargs["metadata"]["course"] == "Machine Learning"
    assert call.kwargs["metadata"]["semester"] == 5
    assert call.kwargs["metadata"]["cgpa"] == 9.6


def test_student_delete_sync():
    service = StudentVectorService()
    service.vector_store = MagicMock()

    student_id = 11

    service.vector_store.collection.delete(
        ids=[str(student_id)]
    )

    service.vector_store.collection.delete.assert_called_once_with(
        ids=["11"]
    )

def test_extract_filters():
    from app.ai.nodes import extract_filters

    filters = extract_filters(
        "Which CSE students have CGPA above 8.5?"
    )

    assert filters["department"] == "cse"
    assert filters["cgpa_operator"] == ">"
    assert filters["cgpa_value"] == 8.5