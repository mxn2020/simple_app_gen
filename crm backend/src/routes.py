from flask import Flask, jsonify, request
from models import db, User

app = Flask(__name__)

# Define route for user registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

if __name__ == '__main__':
    app.run()