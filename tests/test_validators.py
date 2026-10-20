from app.validators import validate_task_payload


def test_valid_payload():
    assert validate_task_payload({"title": "Belajar CI/CD", "priority": "high"}) == []


def test_missing_title():
    assert "Field 'title' wajib diisi" in validate_task_payload({})


def test_empty_title():
    assert validate_task_payload({"title": "  "})


def test_title_too_long():
    assert validate_task_payload({"title": "x" * 101})


def test_invalid_priority_and_done():
    errs = validate_task_payload({"title": "a", "priority": "urgent", "done": "yes"})
    assert len(errs) == 2


def test_non_dict_payload():
    assert validate_task_payload([1, 2]) == ["Payload harus berupa objek JSON"]


def test_partial_allows_missing_title():
    assert validate_task_payload({"done": True}, partial=True) == []


def test_description_too_long():
    assert validate_task_payload({"title": "a", "description": "x" * 501})
