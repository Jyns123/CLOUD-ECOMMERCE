from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

from models import User, Doctor, Appointment
from Cliente.cliente import cliente_bp
from Doctor.doctor import doctor_bp
from Cita.cita import cita_bp

app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
app.register_blueprint(doctor_bp, url_prefix='/api/doctores')
app.register_blueprint(cita_bp, url_prefix='/api/citas')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
