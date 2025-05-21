import pytest
from app import create_app, db
from sqlalchemy.exc import OperationalError
from flask import Flask

def test_database_connection():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        result = db.session.execute(db.text('SELECT 1')).fetchall()
        assert result == [(1,)]



def test_invalid_database_connection():
    # Create a new Flask app just for this test
    test_app = Flask(__name__)
    
    # Set invalid database URI
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/invalid.db'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with this new app
    db.init_app(test_app)

    with test_app.app_context():
        # Force connection by attempting a query
        with pytest.raises(OperationalError):
            db.session.execute(db.text('SELECT 1'))

