from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Flask/SQLAlchemy instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "mysql+pymysql://root:utec@52.206.143.132:8005/dbLogin")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 Error Handler
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# API ENDPOINTS

# LOGIN User
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful'}), 200

# CREATE User (for testing purposes)
@app.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
