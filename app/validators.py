"""Validasi input untuk endpoint TaskTracker."""
from .models import VALID_PRIORITIES

MAX_TITLE_LENGTH = 100
MAX_DESC_LENGTH = 500


def validate_task_payload(data, partial=False):
    """Mengembalikan daftar pesan error. List kosong berarti valid."""
    errors = []
    if not isinstance(data, dict):
        return ["Payload harus berupa objek JSON"]

    if not partial and "title" not in data:
        errors.append("Field 'title' wajib diisi")

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            errors.append("Field 'title' harus berupa teks tidak kosong")
        elif len(title) > MAX_TITLE_LENGTH:
            errors.append(f"Field 'title' maksimal {MAX_TITLE_LENGTH} karakter")

    if "description" in data:
        desc = data["description"]
        if not isinstance(desc, str) or len(desc) > MAX_DESC_LENGTH:
            errors.append(f"Field 'description' maksimal {MAX_DESC_LENGTH} karakter")

    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        errors.append("Field 'priority' harus salah satu dari: " + ", ".join(VALID_PRIORITIES))

    if "done" in data and not isinstance(data["done"], bool):
        errors.append("Field 'done' harus bertipe boolean")

    return errors
