from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:utec@52.202.106.35:8005/dbcloud"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Cliente Model
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
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    sexo = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Doctor {self.id}>'

# Cita Model
class Cita(db.Model):
    __tablename__ = 'cita'
    code = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    cliente_dni = db.Column(db.String(8), db.ForeignKey('cliente.dni'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 Error Handler
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# API ENDPOINTS

# CREATE Cita
@app.route('/cita', methods=['POST'])
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

# READ (all) Cita
@app.route('/cita', methods=['GET'])
def get_citas():
    citas = Cita.query.all()
    return jsonify([{
        'code': cita.code,
        'cliente_dni': cita.cliente_dni,
        'doctor_id': cita.doctor_id,
        'date': cita.date
    } for cita in citas]), 200

# READ (each) Cita
@app.route('/cita/<int:id>', methods=['GET'])
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

# UPDATE Cita
@app.route('/cita/<int:id>', methods=['PATCH'])
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

# DELETE Cita
@app.route('/cita/<int:id>', methods=['DELETE'])
def delete_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita deleted successfully'}), 204

# CREATE Cliente
@app.route('/cliente', methods=['POST'])
def create_cliente():
    data = request.get_json()
    cliente = Cliente(dni=data['dni'], nombre=data['nombre'], apellido=data['apellido'])
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente created successfully'}), 201

# READ (all) Cliente
@app.route('/cliente', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'dni': cliente.dni,
        'nombre': cliente.nombre,
        'apellido': cliente.apellido
    } for cliente in clientes]), 200

# READ (each) Cliente
@app.route('/cliente/<string:dni>', methods=['GET'])
def get_cliente(dni):
    cliente = Cliente.query.get(dni)
    if cliente is None:
        return not_found(404)
    
    return jsonify({
        'dni': cliente.dni,
        'nombre': cliente.nombre,
        'apellido': cliente.apellido
    }), 200

# UPDATE Cliente
@app.route('/cliente/<string:dni>', methods=['PATCH'])
def update_cliente(dni):
    cliente = Cliente.query.get(dni)
    if cliente is None:
        return not_found(404)

    data = request.get_json()

    if 'nombre' in data:
        cliente.nombre = data['nombre']
    
    if 'apellido' in data:
        cliente.apellido = data['apellido']
    
    db.session.commit()
    return jsonify({'message': 'Cliente updated successfully'}), 200

# DELETE Cliente
@app.route('/cliente/<string:dni>', methods=['DELETE'])
def delete_cliente(dni):
    cliente = Cliente.query.get(dni)
    if cliente is None:
        return not_found(404)
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente deleted successfully'}), 204

# CREATE Doctor
@app.route('/doctor', methods=['POST'])
def create_doctor():
    data = request.get_json()
    doctor = Doctor(nombre=data['nombre'], apellido=data['apellido'], sexo=data['sexo'], image=data['image'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor created successfully'}), 201

# READ (all) Doctor
@app.route('/doctor', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        'id': doctor.id,
        'nombre': doctor.nombre,
        'apellido': doctor.apellido,
        'sexo': doctor.sexo,
        'image': doctor.image
    } for doctor in doctors]), 200

# READ (each) Doctor
@app.route('/doctor/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor is None:
        return not_found(404)
    
    return jsonify({
        'id': doctor.id,
        'nombre': doctor.nombre,
        'apellido': doctor.apellido,
        'sexo': doctor.sexo,
        'image': doctor.image
    }), 200

# UPDATE Doctor
@app.route('/doctor/<int:id>', methods=['PATCH'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor is None:
        return not_found(404)

    data = request.get_json()

    if 'nombre' in data:
        doctor.nombre = data['nombre']
    
    if 'apellido' in data:
        doctor.apellido = data['apellido']
    
    if 'sexo' in data:
        doctor.sexo = data['sexo']
    
    if 'image' in data:
        doctor.image = data['image']
    
    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully'}), 200

# DELETE Doctor
@app.route('/doctor/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor is None:
        return not_found(404)
    
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'}), 204

# Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8014, debug=True)
