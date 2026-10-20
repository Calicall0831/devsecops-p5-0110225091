"""TaskTracker API - aplikasi manajemen tugas sederhana berbasis Flask."""
from flask import Flask

from .routes import bp as tasks_bp
from .storage import TaskStorage


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["STORAGE"] = TaskStorage()
    app.register_blueprint(tasks_bp)
    return app
