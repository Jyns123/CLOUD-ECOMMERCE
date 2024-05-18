from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
medicamento_api = Flask(__name__)
medicamento_api.config['SQLALCHEMY_DATABASE_URI'] = ""
medicamento_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(medicamento_api)
CORS(medicamento_api)

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
    
# Resevation Model
class Medicamento(db.Model):
    __tablename__ = 'Medicamento'
    serie = db.Column(db.Integer, primary_key = True, nullable = False)
    Nombre_M = db.Column(db.String(30), nullable = False)
    fecha_V = db.Column(db.DateTime, nullable = False)
    doctor_ID = db.Column(db.Integer, db.ForeignKey('Doctor.ID'), nullable = False)
    doctor_Nombre = db.Column(db.Integer, db.ForeignKey('Doctor.Nombre'), nullable = False)
    doctor_Apellido = db.Column(db.Integer, db.ForeignKey('Doctor.Apellido'), nullable = False)

# 404 Error Handler
@medicamento_api.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not found.'}), 404

# 500 Error Handler
@medicamento_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error' : 'Internal server error.'}), 500

# API ENDPOINTS
# CREATE
@medicamento_api.route('/Medicamento', methods = ['POST'])
def crear_medicamento():
    data = request.get_json()

    doctor = Doctor.query.get(data['doctor_ID'])
    if doctor is None:
        return not_found(404)

    medicamento = Medicamento(serie = data['serie'], Nombre_M = data['Nombre_M'], fecha_V = data['date'],doctor_ID = data['doctor_id'], doctor_Nombre = data['doctor_Nombre'],doctor_Apellido = data['doctor_Apellido'])
    db.session.add(medicamento)
    db.session.commit()
    return jsonify({'message': 'date created sucessfully'}), 201

# READ (all)
@medicamento_api.route('/Medicamento', methods = ['GET'])
def get_Medicamentos():
    medicamento = Medicamento.query.all()
    return jsonify([{'Serie': medicamento.serie,
                     'Nombre_Medicamento': medicamento.Nombre,
                     'Doctor_ID': medicamento.doctor_ID,
                     'Doctor_Nombre': medicamento.doctor_Nombre,
                     'Doctor_Apellido': medicamento.doctor_Nombre,
                     'Fecha_V': medicamento.fecha_V,
                    } for medicamento in medicamento]), 200

# READ (each)
@medicamento_api.route('/Medicamento/<int:serie>', methods = ['GET'])
def get_medicamento(id):
    medicamento = Medicamento.query.get(id)
    if medicamento is None:
        return not_found(404)
    
    return jsonify({'Serie': medicamento.serie,
                     'Nombre_Medicamento': medicamento.Nombre,
                     'Doctor_ID': medicamento.doctor_ID,
                     'Doctor_Nombre': medicamento.doctor_Nombre,
                     'Doctor_Apellido': medicamento.doctor_Nombre,
                     'Fecha_V': medicamento.fecha_V
                     }), 200

# UPDATE
@medicamento_api.route('/Medicameto/<int:serie>', methods = ['PATCH'])
def update_medicamento(id):
    medicamento = Medicamento.query.get(id)
    if medicamento is None:
        return not_found(404)

    data = request.get_json()

    if 'doctor_ID' in data:
        doctor = Doctor.query.get(data['doctor_ID'])
        if doctor is None:
            return not_found(404)
        else:
            medicamento.doctor_ID = data['doctor_ID']
    
    if 'fecha_V' in data:
        medicamento.date = data['Fecha_V']
    
    db.session.commit()
    return jsonify({'message': 'Medicine updated successfully'}), 200

# DELETE
@medicamento_api.route('/Medicamento/<int:serie>', methods = ['DELETE'])
def delete_medicamento(id):
    medicamento = Medicamento.query.get(id)
    if medicamento is None:
        return not_found(404)
    
    db.session.delete(medicamento)
    db.session.commit()
    return jsonify({'message': 'Medicine deleted successfully'}), 204

# Run
if __name__ == '__main__':
    medicamento_api.run(host = '0.0.0.0', port = 8014, debug = True)
