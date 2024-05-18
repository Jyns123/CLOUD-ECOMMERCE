from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
cita_api = Flask(__name__)
cita_api.config['SQLALCHEMY_DATABASE_URI'] = ""
cita_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(cita_api)
CORS(cita_api)

# Client Model
class Cliente(db.Model):
    __tablename__ = 'cliente'
    DNI = db.Column(db.Integer, primary_key = True, nullable = False)
    Nombre = db.Column(db.String(30), nullable = False)
    Apellido = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'<Cliente {self.id}>'

# Doctor Model
class Doctor(db.Model):
    __tablename__ = 'doctor'
    ID = db.Column(db.Integer, primary_key = True, nullable = False)
    Nombre = db.Column(db.String(30), primary_key = True, nullable = False)
    Apellido = db.Column(db.String(60), nullable = False)
    Sexo = db.Column(db.String(30), nullable = False)
    image = db.Column(db.String(150), nullable = False)

    def __repr__(self):
        return f'<Doctor {self.ID}>'
    
# Resevation Model
class Cita(db.Model):
    __tablename__ = 'cita'
    code = db.Column(db.Integer, primary_key = True, nullable = False)
    cliente_DNI = db.Column(db.String(8), db.ForeignKey('Cliente.DNI'), nullable = False)
    cliente_Nombre = db.Column(db.String(8), db.ForeignKey('Cliente.Nombre'), nullable = False)
    cliente_Apellido = db.Column(db.String(8), db.ForeignKey('Cliente.Apellido'), nullable = False)
    doctor_ID = db.Column(db.Integer, db.ForeignKey('Doctor.ID'), nullable = False)
    doctor_Nombre = db.Column(db.Integer, db.ForeignKey('Doctor.Nombre'), nullable = False)
    doctor_Apellido = db.Column(db.Integer, db.ForeignKey('Doctor.Apellido'), nullable = False)
    date = db.Column(db.DateTime, nullable = False)

# 404 Error Handler
@cita_api.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not found.'}), 404

# 500 Error Handler
@cita_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error' : 'Internal server error.'}), 500

# API ENDPOINTS
# CREATE
@cita_api.route('/cita', methods = ['POST'])
def crear_cita():
    data = request.get_json()
    
    cliente = Cliente.query.get(data['cliente_DNI'])
    if cliente is None:
        return not_found(404)

    doctor = Doctor.query.get(data['doctor_ID'])
    if doctor is None:
        return not_found(404)

    cita = Cita(cliente_DNI = data['cliente_DNI'],cliente_nomrbe = data['cliente_Nombre'],cliente_Apellido = data['cliente_Apellido'],doctor_ID = data['doctor_id'], doctor_Nombre = data['doctor_Nombre'],doctor_Apellido = data['doctor_Apellido'], date = data['date'])
    db.session.add(cita)
    db.session.commit()
    return jsonify({'message': 'date created sucessfully'}), 201

# READ (all)
@cita_api.route('/cita', methods = ['GET'])
def get_citas():
    cita = Cita.query.all()
    return jsonify([{'Code': cita.code,
                     'cliente_DNI': cita.cliente_DNI,
                     'cliente_Nombre': cita.cliente_Nombre,
                     'Doctor_ID': cita.doctor_ID,
                     'Doctor_Nombre': cita.doctor_Nombre,
                     'date': cita.date,
                    } for cita in cita]), 200

# READ (each)
@cita_api.route('/cita/<int:id>', methods = ['GET'])
def get_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    return jsonify({'Code': cita.code,
                     'cliente_DNI': cita.cliente_DNI,
                     'cliente_Nombre': cita.cliente_Nombre,
                     'Doctor_ID': cita.doctor_ID,
                     'Doctor_Nombre': cita.doctor_Nombre,
                     'date': cita.date
                     }), 200
# UPDATE
@cita_api.route('/cita/<int:id>', methods = ['PATCH'])
def update_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)

    data = request.get_json()

    if 'cliente_DNI' in data:
        cliente = Cliente.query.get(data['cliente_DNI'])
        if cliente is None:
            return jsonify({'error' : 'Cliente not found'}), 404
        else:
            cita.cliente_DNI = data['cliente_DNI']

    if 'doctor_ID' in data:
        doctor = Doctor.query.get(data['doctor_ID'])
        if doctor is None:
            return not_found(404)
        else:
            cita.doctor_ID = data['doctor_ID']
    
    if 'date' in data:
        cita.date = data['date']
    
    db.session.commit()
    return jsonify({'message': 'Sate updated successfully'}), 200

# DELETE
@cita_api.route('/cita/<int:id>', methods = ['DELETE'])
def delete_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Date deleted successfully'}), 204

# Run
if __name__ == '__main__':
    cita_api.run(host = '0.0.0.0', port = 8014, debug = True)
