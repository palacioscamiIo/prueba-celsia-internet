from app.main import db
from app.models.servicio import Servicio  # Importar el modelo Servicio

class Cliente(db.Model):
    __tablename__ = 'clientes'
    identificacion = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    tipo_identificacion = db.Column(db.String(2), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    numero_celular = db.Column(db.String(20), nullable=False)
    correo_electronico = db.Column(db.String(80), nullable=False)

    # Definir la relación con el modelo Servicio
    servicios = db.relationship('Servicio', backref='cliente', lazy=True)
