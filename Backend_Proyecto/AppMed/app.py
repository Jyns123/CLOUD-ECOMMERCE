from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Flask/SQLAlchemy instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "mysql+pymysql://root:utec@52.206.143.132:8005/dbMeds")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Models
class Tipo(db.Model):
    __tablename__ = 'tipos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)

# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 Error Handler
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# API ENDPOINTS

# CRUD for Tipo
@app.route('/tipos', methods=['GET'])
def get_tipos():
    tipos = Tipo.query.all()
    return jsonify([{'id': tipo.id, 'nombre': tipo.nombre} for tipo in tipos]), 200

@app.route('/tipos', methods=['POST'])
def create_tipo():
    data = request.get_json()
    tipo = Tipo(nombre=data['nombre'])
    db.session.add(tipo)
    db.session.commit()
    return jsonify({'message': 'Tipo created successfully'}), 201

@app.route('/tipos/<int:id>', methods=['PUT'])
def update_tipo(id):
    tipo = Tipo.query.get(id)
    if tipo is None:
        return not_found(404)
    data = request.get_json()
    tipo.nombre = data['nombre']
    db.session.commit()
    return jsonify({'message': 'Tipo updated successfully'}), 200

@app.route('/tipos/<int:id>', methods=['DELETE'])
def delete_tipo(id):
    tipo = Tipo.query.get(id)
    if tipo is None:
        return not_found(404)
    db.session.delete(tipo)
    db.session.commit()
    return jsonify({'message': 'Tipo deleted successfully'}), 204

# CRUD for Marca
@app.route('/marcas', methods=['GET'])
def get_marcas():
    marcas = Marca.query.all()
    return jsonify([{'id': marca.id, 'nombre': marca.nombre} for marca in marcas]), 200

@app.route('/marcas', methods=['POST'])
def create_marca():
    data = request.get_json()
    marca = Marca(nombre=data['nombre'])
    db.session.add(marca)
    db.session.commit()
    return jsonify({'message': 'Marca created successfully'}), 201

@app.route('/marcas/<int:id>', methods=['PUT'])
def update_marca(id):
    marca = Marca.query.get(id)
    if marca is None:
        return not_found(404)
    data = request.get_json()
    marca.nombre = data['nombre']
    db.session.commit()
    return jsonify({'message': 'Marca updated successfully'}), 200

@app.route('/marcas/<int:id>', methods=['DELETE'])
def delete_marca(id):
    marca = Marca.query.get(id)
    if marca is None:
        return not_found(404)
    db.session.delete(marca)
    db.session.commit()
    return jsonify({'message': 'Marca deleted successfully'}), 204

# CRUD for Medicamento
@app.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    medicamentos = Medicamento.query.all()
    return jsonify([{'id': medicamento.id, 'nombre': medicamento.nombre, 'tipo_id': medicamento.tipo_id, 'marca_id': medicamento.marca_id} for medicamento in medicamentos]), 200

@app.route('/medicamentos', methods=['POST'])
def create_medicamento():
    data = request.get_json()
    medicamento = Medicamento(nombre=data['nombre'], tipo_id=data['tipo_id'], marca_id=data['marca_id'])
    db.session.add(medicamento)
    db.session.commit()
    return jsonify({'message': 'Medicamento created successfully'}), 201

@app.route('/medicamentos/<int:id>', methods=['PUT'])
def update_medicamento(id):
    medicamento = Medicamento.query.get(id)
    if medicamento is None:
        return not_found(404)
    data = request.get_json()
    medicamento.nombre = data['nombre']
    medicamento.tipo_id = data['tipo_id']
    medicamento.marca_id = data['marca_id']
    db.session.commit()
    return jsonify({'message': 'Medicamento updated successfully'}), 200

@app.route('/medicamentos/<int:id>', methods=['DELETE'])
def delete_medicamento(id):
    medicamento = Medicamento.query.get(id)
    if medicamento is None:
        return not_found(404)
    db.session.delete(medicamento)
    db.session.commit()
    return jsonify({'message': 'Medicamento deleted successfully'}), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8016, debug=True)
