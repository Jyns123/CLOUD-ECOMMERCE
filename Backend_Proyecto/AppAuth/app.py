from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger, swag_from
import os

# Flask/SQLAlchemy instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "mysql+pymysql://root:utec@52.206.143.132:8005/dbLogin")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
swagger = Swagger(app)

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
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {
                'application/json': {'message': 'Login successful'}
            }
        },
        401: {
            'description': 'Invalid credentials',
            'examples': {
                'application/json': {'error': 'Invalid credentials'}
            }
        }
    }
})
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful'}), 200

# CREATE User
@app.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'User created successfully',
            'examples': {
                'application/json': {'message': 'User created successfully'}
            }
        }
    }
})
def create_user():
    data = request.get_json()
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# GET all Users
@app.route('/users', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of users',
            'examples': {
                'application/json': [{'id': 1, 'username': 'user1'}, {'id': 2, 'username': 'user2'}]
            }
        }
    }
})
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

# UPDATE User
@app.route('/users/<int:id>', methods=['PUT'])
@swag_from({
    'responses': {
        200: {
            'description': 'User updated successfully',
            'examples': {
                'application/json': {'message': 'User updated successfully'}
            }
        },
        404: {
            'description': 'Not found',
            'examples': {
                'application/json': {'error': 'Not found.'}
            }
        }
    }
})
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return not_found(404)
    data = request.get_json()
    user.username = data['username']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# DELETE User
@app.route('/users/<int:id>', methods=['DELETE'])
@swag_from({
    'responses': {
        204: {
            'description': 'User deleted successfully',
            'examples': {
                'application/json': {'message': 'User deleted successfully'}
            }
        },
        404: {
            'description': 'Not found',
            'examples': {
                'application/json': {'error': 'Not found.'}
            }
        }
    }
})
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return not_found(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
