```python
# database.py

class Database:
    def __init__(self):
        # Initialize database connection or setup
        
    def register_user(self, username, password):
        # Logic to register a new user in the database
        # Include validation and encryption of password
        
    def authenticate_user(self, username, password):
        # Verify user credentials for login
        # Return True if authentication is successful
        
    def store_calculation_history(self, user_id, calculation):
        # Store user's calculation history in the database
        
    def retrieve_calculation_history(self, user_id):
        # Retrieve and return the calculation history for a specific user

# Additional functions and helper methods can be added as needed
```

Instructions:
1. This implementation file `database.py` is responsible for handling database connections and operations for user registration and storing calculation history in the calculator Python Flask app.
2. To use the file, create an instance of the `Database` class and call its methods to register users, authenticate users, store calculation history, and retrieve calculation history based on user ID. Make sure to set up the database connection and handling according to your database system requirements.