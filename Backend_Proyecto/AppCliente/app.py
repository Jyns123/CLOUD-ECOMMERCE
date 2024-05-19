from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger, swag_from

# Flask/SQLAlchemy instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:utec@52.206.143.132:8005/dbCliente"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
swagger = Swagger(app)

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
@swag_from({
    'responses': {
        201: {
            'description': 'Cita created successfully',
            'examples': {
                'application/json': {'message': 'Cita created successfully'}
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
@swag_from({
    'responses': {
        200: {
            'description': 'List of citas',
            'examples': {
                'application/json': [{'code': 1, 'cliente_dni': '12345678', 'doctor_id': 1, 'date': '2023-05-19T14:30:00'}]
            }
        }
    }
})
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
@swag_from({
    'responses': {
        200: {
            'description': 'Cita details',
            'examples': {
                'application/json': {'code': 1, 'cliente_dni': '12345678', 'doctor_id': 1, 'date': '2023-05-19T14:30:00'}
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
@swag_from({
    'responses': {
        200: {
            'description': 'Cita updated successfully',
            'examples': {
                'application/json': {'message': 'Cita updated successfully'}
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
@swag_from({
    'responses': {
        204: {
            'description': 'Cita deleted successfully',
            'examples': {
                'application/json': {'message': 'Cita deleted successfully'}
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
def delete_cita(id):
    cita = Cita.query.get(id)
    if cita is None:
        return not_found(404)
    
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'message': 'Cita deleted successfully'}), 204

# CREATE Cliente
@app.route('/cliente', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Cliente created successfully',
            'examples': {
                'application/json': {'message': 'Cliente created successfully'}
            }
        }
    }
})
def create_cliente():
    data = request.get_json()
    cliente = Cliente(dni=data['dni'], nombre=data['nombre'], apellido=data['apellido'])
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente created successfully'}), 201

# READ (all) Cliente
@app.route('/cliente', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of clientes',
            'examples': {
                'application/json': [{'dni': '12345678', 'nombre': 'Juan', 'apellido': 'Perez'}]
            }
        }
    }
})
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'dni': cliente.dni,
        'nombre': cliente.nombre,
        'apellido': cliente.apellido
    } for cliente in clientes]), 200

# READ (each) Cliente
@app.route('/cliente/<string:dni>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Cliente details',
            'examples': {
                'application/json': {'dni': '12345678', 'nombre': 'Juan', 'apellido': 'Perez'}
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
@swag_from({
    'responses': {
        200: {
            'description': 'Cliente updated successfully',
            'examples': {
                'application/json': {'message': 'Cliente updated successfully'}
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
@swag_from({
    'responses': {
        204: {
            'description': 'Cliente deleted successfully',
            'examples': {
                'application/json': {'message': 'Cliente deleted successfully'}
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
def delete_cliente(dni):
    cliente = Cliente.query.get(dni)
    if cliente is None:
        return not_found(404)
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente deleted successfully'}), 204

# CREATE Doctor
@app.route('/doctor', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Doctor created successfully',
            'examples': {
                'application/json': {'message': 'Doctor created successfully'}
            }
        }
    }
})
def create_doctor():
    data = request.get_json()
    doctor = Doctor(nombre=data['nombre'], apellido=data['apellido'], sexo=data['sexo'], image=data['image'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor created successfully'}), 201

# READ (all) Doctor
@app.route('/doctor', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of doctors',
            'examples': {
                'application/json': [{'id': 1, 'nombre': 'Dr. Smith', 'apellido': 'Johnson', 'sexo': 'M', 'image': 'image1.jpg'}]
            }
        }
    }
})
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
@swag_from({
    'responses': {
        200: {
            'description': 'Doctor details',
            'examples': {
                'application/json': {'id': 1, 'nombre': 'Dr. Smith', 'apellido': 'Johnson', 'sexo': 'M', 'image': 'image1.jpg'}
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
@swag_from({
    'responses': {
        200: {
            'description': 'Doctor updated successfully',
            'examples': {
                'application/json': {'message': 'Doctor updated successfully'}
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
@swag_from({
    'responses': {
        204: {
            'description': 'Doctor deleted successfully',
            'examples': {
                'application/json': {'message': 'Doctor deleted successfully'}
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
