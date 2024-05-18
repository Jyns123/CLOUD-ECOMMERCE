from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
doctor_api = Flask(__name__)
doctor_api.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:utec@52.202.106.35:8005/dbcloud"
doctor_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(doctor_api)
CORS(doctor_api)

# Doctor Model
class Doctor(db.Model):
    __tablename__ = 'Doctor'
    ID = db.Column(db.Integer, primary_key = True, nullable = False)
    Nombre = db.Column(db.String(30), primary_key = True, nullable = False)
    Apellido = db.Column(db.String(60), nullable = False)
    Sexo = db.Column(db.String(30), nullable = False)
    image = db.Column(db.String(150), nullable = False)

    def __repr__(self):
        return f'<Doctor {self.ID}>'

# 404 Error Handler 
@doctor_api.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not found.'}), 404

# 500 Error Handler
@doctor_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error' : 'Internal server error.'}), 500

# CREATE API Endpoint
@doctor_api.route('/Doctor', methods = ['POST'])
def create_dc():
    data = request.get_json()
    doctor = Doctor(ID = data['ID'], 
              Nombre = data['Nombre'], 
              Apellido = data['Apellido'], 
              Sexo = data['Sexo'], 
              image = data['image'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'message' : 'Doctor created successfully'}), 201

# READ (all) API Endpoint
@doctor_api.route('/Doctor', methods = ['GET'])
def get_alldoctor():
    doctors = Doctor.query.all()
    return jsonify([{'ID' : doctor.ID,
                        'Nombre' : doctor.nombre,
                        'Apellido': doctor.apellido,
                        'Sexo' : doctor.sexo,
                        'image': doctor.image} for doctor in doctors]), 200

# READ (each)
@doctor_api.route('/Doctor/<int:ID>', methods = ['GET'])
def get_doctor(ID):
    doctor = Doctor.query.get(ID)
    if doctor is None:
        return not_found(404)
    return jsonify({'ID' : doctor.ID,
                        'Nombre' : doctor.nombre,
                        'Apellido': doctor.apellido,
                        'Sexo' : doctor.sexo,
                        'image': doctor.image}), 200
    
# UPDATE
@Doctor.route('/Doctor/<int:ID>', methods = ['PATCH'])
def update_doctor(ID):
    doctor = Doctor.query.get(ID)

    if doctor is None:
        return jsonify({'error' : 'Doctor not found'}), 404

    data = request.get_json()
    if 'Nombre' in data:
        doctor.nombre = data['nombre']
    if 'Apellido' in data:
        doctor.Apellido = data['Apellido']
    if 'Sexo' in data:
        doctor.sexo = data['Sexo']
    if 'image' in data:
        doctor.image = data['image']

    db.session.commit()
    return jsonify({'message' : 'Doctor updated successfully'}), 200

# DELETE
@doctor_api.route('/Doctor/<int:ID>', methods = ['DELETE'])
def delete_doctor(ID):
    doctor = Doctor.query.get(ID)
    if doctor is None:
        return not_found(404)

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message' : 'Doctor deleted successfully'}),204

# Run
if __name__ == '__main__':
    doctor_api.run(host = '0.0.0.0', port = 8012, debug = True)

