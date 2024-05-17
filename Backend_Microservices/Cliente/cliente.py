from flask import Blueprint, request, jsonify
from app import db
from models import User

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Usuario ya existe'}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado correctamente'}), 201

@cliente_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login correcto', 'username': username}), 200
    return jsonify({'message': 'Credenciales no son correctas'}), 401
