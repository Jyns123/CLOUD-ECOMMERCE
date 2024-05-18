import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
cita_api = Flask(__name__)
cita_api.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
cita_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(cita_api)
CORS(cita_api)

# Client Model
class Cliente(db.Model):
    __tablename__ = 'cliente'
    dni = db.Column(db.String(8), primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.dni}>'

# Doctor Model
class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    sexo = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Doctor {self.id}>'

# Reservation Model
class Cita(db.Model):
    __tablename__ = 'cita'
    code = db.Column(db.Integer, primary_key=True, nullable=False)
    cliente_dni = db.Column(db.String(8), db.ForeignKey('cliente.dni'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# 404 Error Handler
@cita_api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 Error Handler
@cita_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# API ENDPOINTS
# CREATE
@cita_api.route('/cita', methods=['POST'])
def crear_cita():
    data = request.get_json()
    
    cliente = Cliente.query.get(data['cliente_dni'])
    if cliente is None:
        return not_found(404)

    doctor = Doctor.query.get(data['doctor_id'])
    if doctor is None:
        return not_found(404)

    cita = Cita(cliente_dni=data['cliente_dni'], doctor_id=data['doctor_id'], date=data['date'])
    db.session.add(cita)
    db.session.commit()
    return jsonify({'message': 'Cita created successfully'}), 201

# READ (all)
@cita_api.route('/cita', methods=['GET'])
def get_citas():
    citas = Cita.query.all()
    return jsonify([{
        'code': cita.code,
        'cliente_dni': cita.cliente_dni,
        'doctor_id': cita.doctor_id,
        'date': cita.date
    } for cita in citas]), 200

# READ (each)
@cita_api.route('/cita/<int:id>', methods=['GET'])
def get_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    return jsonify({
        'code': cita.code,
        'cliente_dni': cita.cliente_dni,
        'doctor_id': cita.doctor_id,
        'date': cita.date
    }), 200

# UPDATE
@cita_api.route('/cita/<int:id>', methods=['PATCH'])
def update_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)

    data = request.get_json()

    if 'cliente_dni' in data:
        cliente = Cliente.query.get(data['cliente_dni'])
        if cliente is None:
            return jsonify({'error': 'Cliente not found'}), 404
        else:
            cita.cliente_dni = data['cliente_dni']

    if 'doctor_id' in data:
        doctor = Doctor.query.get(data['doctor_id'])
        if doctor is None:
            return not_found(404)
        else:
            cita.doctor_id = data['doctor_id']
    
    if 'date' in data:
        cita.date = data['date']
    
    db.session.commit()
    return jsonify({'message': 'Cita updated successfully'}), 200

# DELETE
@cita_api.route('/cita/<int:id>', methods=['DELETE'])
def delete_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita deleted successfully'}), 204

# Run
if __name__ == '__main__':
    cita_api.run(host='0.0.0.0', port=8014, debug=True)
