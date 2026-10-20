"""Entry point: python run.py"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Bind ke localhost saja; debug dimatikan demi keamanan.
    app.run(host="127.0.0.1", port=5000, debug=False)
