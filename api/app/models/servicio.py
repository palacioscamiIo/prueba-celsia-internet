from app.main import db

class Servicio(db.Model):
    __tablename__ = 'servicios'
    identificacion = db.Column(db.String(20), db.ForeignKey('clientes.identificacion'), primary_key=True)
    servicio = db.Column(db.String(80), primary_key=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    ultima_facturacion = db.Column(db.Date, nullable=False)
    ultimo_pago = db.Column(db.Integer, nullable=False, default=0)
