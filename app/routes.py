"""Endpoint REST untuk TaskTracker."""
from flask import Blueprint, current_app, jsonify, request

from .stats import summarize
from .validators import validate_task_payload

bp = Blueprint("tasks", __name__)


def _storage():
    return current_app.config["STORAGE"]


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/tasks")
def list_tasks():
    done_arg = request.args.get("done")
    done = None
    if done_arg is not None:
        if done_arg.lower() not in ("true", "false"):
            return jsonify({"errors": ["Parameter 'done' harus true/false"]}), 400
        done = done_arg.lower() == "true"
    tasks = _storage().list(done=done, priority=request.args.get("priority"))
    return jsonify([t.to_dict() for t in tasks])


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    errors = validate_task_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400
    task = _storage().add(data["title"], data.get("description", ""),
                          data.get("priority", "medium"))
    return jsonify(task.to_dict()), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = _storage().get(task_id)
    if task is None:
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return jsonify(task.to_dict())


@bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    errors = validate_task_payload(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    task = _storage().update(task_id, **data)
    if task is None:
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return jsonify(task.to_dict())


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if not _storage().delete(task_id):
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return "", 204


@bp.get("/stats")
def stats():
    return jsonify(summarize(_storage().list()))
