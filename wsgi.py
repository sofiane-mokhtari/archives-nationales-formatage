# Flask Application - Runs the AI microservice (called by gunicorn)

from api import app

if __name__ == "__main__":
    app.run()
