from flask import Blueprint, request, jsonify

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    from app.main import db
    from app.models.cliente import Cliente
    data = request.get_json()
    if not data:
        return jsonify({"message": "Datos no proporcionados"}), 400

    identificacion = data.get('identificacion')
    if Cliente.query.get(identificacion):
        return jsonify({"message": "El registro ya existe"}), 409

    nuevo_cliente = Cliente(
        identificacion=identificacion,
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        tipo_identificacion=data['tipoIdentificacion'],
        fecha_nacimiento=data['fechaNacimiento'],
        numero_celular=data['numeroCelular'],
        correo_electronico=data['correoElectronico']
    )
    db.session.add(nuevo_cliente)
    db.session.commit()

    return jsonify({"message": "Cliente creado con éxito"}), 201

@clientes_bp.route('/clientes/<identificacion>', methods=['GET'])
def get_cliente(identificacion):
    from app.main import db
    from app.models.cliente import Cliente
    cliente = Cliente.query.get(identificacion)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    return jsonify({
        "identificacion": cliente.identificacion,
        "nombres": cliente.nombres,
        "apellidos": cliente.apellidos,
        "tipo_identificacion": cliente.tipo_identificacion,
        "fecha_nacimiento": cliente.fecha_nacimiento.strftime('%Y-%m-%d'),
        "numero_celular": cliente.numero_celular,
        "correo_electronico": cliente.correo_electronico
    }), 200

@clientes_bp.route('/clientes/<identificacion>', methods=['PUT'])
def update_cliente(identificacion):
    from app.main import db
    from app.models.cliente import Cliente

    cliente = Cliente.query.get(identificacion)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    data = request.get_json()
    cliente.nombres = data.get('nombres', cliente.nombres)
    cliente.apellidos = data.get('apellidos', cliente.apellidos)
    cliente.tipo_identificacion = data.get('tipoIdentificacion', cliente.tipo_identificacion)
    cliente.fecha_nacimiento = data.get('fechaNacimiento', cliente.fecha_nacimiento)
    cliente.numero_celular = data.get('numeroCelular', cliente.numero_celular)
    cliente.correo_electronico = data.get('correoElectronico', cliente.correo_electronico)

    db.session.commit()
    return jsonify({"message": "Cliente actualizado con éxito"}), 200

@clientes_bp.route('/clientes/<identificacion>', methods=['DELETE'])
def delete_cliente(identificacion):
    from app.main import db
    from app.models.cliente import Cliente

    cliente = Cliente.query.get(identificacion)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado con éxito"}), 200
