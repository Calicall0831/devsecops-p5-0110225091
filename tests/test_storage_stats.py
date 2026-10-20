from app.stats import summarize
from app.storage import TaskStorage


def test_add_and_get():
    s = TaskStorage()
    t = s.add("  Tugas 1  ")
    assert t.title == "Tugas 1" and s.get(t.id) is t


def test_filter_and_update():
    s = TaskStorage()
    a = s.add("A", priority="high")
    s.add("B")
    s.update(a.id, done=True)
    assert len(s.list(done=True)) == 1
    assert len(s.list(priority="medium")) == 1


def test_update_missing_and_protected_fields():
    s = TaskStorage()
    assert s.update(99, title="x") is None
    t = s.add("A")
    s.update(t.id, id=500, title=" Baru ")
    assert t.id != 500 and t.title == "Baru"


def test_delete():
    s = TaskStorage()
    t = s.add("A")
    assert s.delete(t.id) is True
    assert s.delete(t.id) is False


def test_summarize():
    s = TaskStorage()
    s.add("A", priority="high")
    b = s.add("B")
    s.update(b.id, done=True)
    r = summarize(s.list())
    assert r["total"] == 2 and r["completion_rate"] == 50.0
    assert r["by_priority"]["high"] == 1


def test_summarize_empty():
    assert summarize([])["completion_rate"] == 0.0
