from flask import Blueprint, request, jsonify

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/servicios', methods=['POST'])
def create_servicio():
    from app.main import db
    from app.models.servicio import Servicio
    data = request.get_json()
    if not data:
        return jsonify({"message": "Datos no proporcionados"}), 400

    identificacion = data.get('identificacion')
    servicio = data.get('servicio')

    if Servicio.query.filter_by(identificacion=identificacion, servicio=servicio).first():
        return jsonify({"message": "El servicio ya existe para este cliente"}), 409

    nuevo_servicio = Servicio(
        identificacion=identificacion,
        servicio=servicio,
        fecha_inicio=data['fechaInicio'],
        ultima_facturacion=data['ultimaFacturacion'],
        ultimo_pago=data.get('ultimoPago', 0)
    )
    db.session.add(nuevo_servicio)
    db.session.commit()

    return jsonify({"message": "Servicio creado con éxito"}), 201

@servicios_bp.route('/servicios/<identificacion>', methods=['GET'])
def get_servicios(identificacion):
    from app.main import db
    from app.models.servicio import Servicio
    servicios = Servicio.query.filter_by(identificacion=identificacion).all()
    if not servicios:
        return jsonify({"message": "No se encontraron servicios para este cliente"}), 404

    servicios_list = [
        {
            "servicio": servicio.servicio,
            "fecha_inicio": servicio.fecha_inicio.strftime('%Y-%m-%d'),
            "ultima_facturacion": servicio.ultima_facturacion.strftime('%Y-%m-%d'),
            "ultimo_pago": servicio.ultimo_pago
        } for servicio in servicios
    ]

    return jsonify(servicios_list), 200

@servicios_bp.route('/servicios/<identificacion>/<servicio>', methods=['PUT'])
def update_servicio(identificacion, servicio):
    from app.main import db
    from app.models.servicio import Servicio
    servicio_obj = Servicio.query.filter_by(identificacion=identificacion, servicio=servicio).first()
    if not servicio_obj:
        return jsonify({"message": "Servicio no encontrado"}), 404

    data = request.get_json()
    servicio_obj.fecha_inicio = data.get('fechaInicio', servicio_obj.fecha_inicio)
    servicio_obj.ultima_facturacion = data.get('ultimaFacturacion', servicio_obj.ultima_facturacion)
    servicio_obj.ultimo_pago = data.get('ultimoPago', servicio_obj.ultimo_pago)

    db.session.commit()
    return jsonify({"message": "Servicio actualizado con éxito"}), 200

@servicios_bp.route('/servicios/<identificacion>/<servicio>', methods=['DELETE'])
def delete_servicio(identificacion, servicio):
    from app.main import db
    from app.models.servicio import Servicio
    servicio_obj = Servicio.query.filter_by(identificacion=identificacion, servicio=servicio).first()
    if not servicio_obj:
        return jsonify({"message": "Servicio no encontrado"}), 404

    db.session.delete(servicio_obj)
    db.session.commit()
    return jsonify({"message": "Servicio eliminado con éxito"}), 200
