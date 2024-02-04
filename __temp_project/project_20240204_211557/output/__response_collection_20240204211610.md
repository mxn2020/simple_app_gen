{
    "file_path": "/src/app.py",
    "code": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello, World!'\n\nif __name__ == '__main__':\n    app.run()",
    "file_instruction": "This file contains the main application logic for running the app. It initializes a Flask application, defines a route for the home page, and runs the app when executed. To use the file, run it using a Python interpreter to start the Flask application."
}