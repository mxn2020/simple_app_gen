{
    "file_path": "src/models.py",
    "code": "from flask_sqlalchemy import SQLAlchemy\n\n# Initialize SQLAlchemy\ndb = SQLAlchemy()\n\nclass User(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(50), unique=True, nullable=False)\n    password = db.Column(db.String(100), nullable=False)\n\n# Add more models for lead, contact, task, etc. as needed\n",
    "file_instruction": "This file contains the database models for the application using SQLAlchemy. It defines an initial User model with id, username, and password fields. Additional models for leads, contacts, tasks, etc. can be added as needed. To use this file, ensure that SQLAlchemy is properly set up and configured in the Flask application."
}