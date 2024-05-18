from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask/SQLAlchemy instance
cliente_api = Flask(__name__)
cliente_api.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:utec@52.202.106.35:8005/dbcloud"
cliente_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(cliente_api)
CORS(cliente_api)

# Client Model
class Cliente(db.Model):
    __tablename__ = 'cliente'
    DNI = db.Column(db.Integer, primary_key = True, nullable = False)
    Nombre = db.Column(db.String(30), nullable = False)
    Apellido = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'<Cliente {self.id}>'

# 404 Error Handler 
@cliente_api.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not found.'}), 404

# 500 Error Handler
@cliente_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error' : 'Internal server error.'}), 500

# CREATE API Endopoint
@cliente_api.route('/cliente', methods = ['POST'])
def create_cliente():
    data = request.get_json()
    cliente = Cliente(DNI = data['DNI'], Nombre = data['Nombre'], Apellido = data['Apellido'])
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'message' : 'Client created successfully'}), 201

# READ (all) API Endpoint
@cliente_api.route('/cliente', methods = ['GET'])
def get_clientes():
    cliente = Cliente.query.all()
    return jsonify([{'DNI': client.DNI,
                     'Nombre': client.Nombre,
                     'Apellido': client.Apellido} for client in cliente]), 200

# READ (each) API Endpoint
@cliente_api.route('/cliente/<string:id>', methods = ['GET'])
def get_client(DNI):
    cliente = Cliente.query.get(DNI)
    if cliente is None:
        return not_found(404)
    return jsonify({'DNI': cliente.DNI,
                     'firstname': cliente.Nombre,
                     'lastname': cliente.Apellido}), 200

# UPDATE API Endpoint
@cliente_api.route('/cliente/<string:id>', methods = ['PATCH'])
def update_client(DNI):
    cliente = Cliente.query.get(DNI)

    if cliente is None:
        return not_found(404)

    data = request.get_json()
    if 'firstname' in data:
        cliente.firstname = data['firstname']
    if 'lastname' in data:
        cliente.lastname = data['lastname']
    db.session.commit()
    return jsonify({'message' : 'Client updated successfully'}), 200

# DELETE API Endpoint
@cliente_api.route('/cliente/<string:id>', methods = ['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente is None:
        return not_found(404)

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message' : 'Client deleted successfully'}), 204

# Run
if __name__ == '__main__':
    cliente_api.run(host = '0.0.0.0', port = 8011, debug = True)