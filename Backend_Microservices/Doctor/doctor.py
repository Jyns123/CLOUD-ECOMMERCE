from flask import Blueprint, request, jsonify
from app import db
from models import Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    result = [{'id': doc.id, 'first_name': doc.first_name, 'last_name': doc.last_name, 'age': doc.age, 'gender': doc.gender, 'years_of_experience': doc.years_of_experience} for doc in doctors]
    return jsonify(result), 200

@doctor_bp.route('/post', methods=['POST'])
def create_doctor():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']
