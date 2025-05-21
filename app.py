"""This module handles the main functionality for the Book Reservation Backend."""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


