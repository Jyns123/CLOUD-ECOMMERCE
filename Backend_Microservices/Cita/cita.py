from flask import Blueprint, request, jsonify
from app import db
from models import Appointment, Doctor

cita_bp = Blueprint('cita', __name__)

@cita_bp.route('/', methods=['POST'])
def create_appointment():
    data = request.get_json()
    doctor_id = data['doctor_id']
    user_name = data['user_name']
    duration = data['duration']
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor no encontrado'}), 404
    new_appointment = Appointment(doctor_id=doctor_id, user_name=user_name, duration=duration)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Cita creada correctamente'}), 201
