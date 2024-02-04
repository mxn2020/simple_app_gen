from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if db.authenticate_user(username, password):
            return redirect(url_for('calculator'))
    return render_template('login.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

if __name__ == '__main__':
    app.run(debug=True)