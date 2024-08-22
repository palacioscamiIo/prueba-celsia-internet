from flask import Flask, request, jsonify, render_template # type: ignore
from flask_cors import CORS # type: ignore
import sqlite3
import logging
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    db_path = os.path.join(app.instance_path, 'celsia.db')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    def init_db():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    identificacion TEXT PRIMARY KEY,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    tipo_identificacion TEXT NOT NULL,
                    fecha_nacimiento DATE NOT NULL,
                    numero_celular TEXT NOT NULL,
                    correo_electronico TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS servicios (
                    identificacion TEXT NOT NULL,
                    servicio TEXT NOT NULL,
                    fecha_inicio DATE NOT NULL,
                    ultima_facturacion DATE NOT NULL,
                    ultimo_pago INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (identificacion, servicio),
                    FOREIGN KEY (identificacion) REFERENCES clientes(identificacion)
                )
            ''')
            conn.commit()

    init_db()

    @app.route('/clientes', methods=['POST'])
    def create_cliente():
        data = request.get_json()
        
        tipos_identificacion_permitidos = ['CC', 'TI', 'CE', 'RC']
        if data['tipoIdentificacion'] not in tipos_identificacion_permitidos:
            return jsonify({"message": "Tipo de identificación no permitido. Valores permitidos: CC, TI, CE, RC"}), 400

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM clientes WHERE identificacion = ?
            ''', (data['identificacion'],))
            cliente_existente = cursor.fetchone()

            if cliente_existente:
                return jsonify({"message": "El registro ya existe"}), 409

            cursor.execute('''
                INSERT INTO clientes (identificacion, nombres, apellidos, tipo_identificacion, fecha_nacimiento, numero_celular, correo_electronico)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['identificacion'],
                data['nombres'],
                data['apellidos'],
                data['tipoIdentificacion'],
                data['fechaNacimiento'],
                data['numeroCelular'],
                data['correoElectronico']
            ))
            conn.commit()
        return jsonify({"message": "Cliente creado con éxito"}), 201


    @app.route('/servicios', methods=['POST'])
    def create_servicio():
        data = request.get_json()
        
        tipos_servicio_permitidos = [
            'Internet 200 MB', 'Internet 400 MB', 'Internet 600 MB', 
            'Directv Go', 'Paramount+', 'Win+'
        ]
        if data['servicio'] not in tipos_servicio_permitidos:
            return jsonify({"message": "Tipo de servicio no permitido. Valores permitidos: Internet 200 MB, Internet 400 MB, Internet 600 MB, Directv Go, Paramount+, Win+"}), 400

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM servicios WHERE identificacion = ? AND servicio = ?
            ''', (data['identificacion'], data['servicio']))
            servicio_existente = cursor.fetchone()

            if servicio_existente:
                return jsonify({"message": "El servicio ya existe para este cliente"}), 409

            cursor.execute('''
                INSERT INTO servicios (identificacion, servicio, fecha_inicio, ultima_facturacion, ultimo_pago)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data['identificacion'],
                data['servicio'],
                data['fechaInicio'],
                data['ultimaFacturacion'],
                data.get('ultimoPago', 0)
            ))
            conn.commit()
        return jsonify({"message": "Servicio creado con éxito"}), 201


    @app.route('/clientes/<identificacion>', methods=['GET'])
    def get_cliente(identificacion):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM clientes WHERE identificacion = ?
            ''', (identificacion,))
            cliente = cursor.fetchone()

            if not cliente:
                return jsonify({"message": "Cliente no encontrado"}), 404

            cursor.execute('''
                SELECT servicio, fecha_inicio, ultima_facturacion, ultimo_pago
                FROM servicios WHERE identificacion = ?
            ''', (identificacion,))
            servicios = cursor.fetchall()

            cliente_data = {
                "identificacion": cliente[0],
                "nombres": cliente[1],
                "apellidos": cliente[2],
                "tipo_identificacion": cliente[3],
                "fecha_nacimiento": cliente[4],
                "numero_celular": cliente[5],
                "correo_electronico": cliente[6],
                "servicios": [
                    {
                        "servicio": s[0],
                        "fecha_inicio": s[1],
                        "ultima_facturacion": s[2],
                        "ultimo_pago": s[3]
                    }
                    for s in servicios
                ]
            }
            logger.info("Endpoint /clientes fue llamado")
            return jsonify(cliente_data), 200

    @app.route('/clientes/<identificacion>', methods=['PUT'])
    def update_cliente(identificacion):
        data = request.get_json()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE clientes
                SET nombres = ?, apellidos = ?, correo_electronico = ?
                WHERE identificacion = ?
            ''', (
                data['nombres'],
                data['apellidos'],
                data['correoElectronico'],
                identificacion
            ))
            conn.commit()
        return jsonify({"message": "Cliente actualizado con éxito"}), 200

    @app.route('/clientes/<identificacion>', methods=['DELETE'])
    def delete_cliente(identificacion):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM clientes WHERE identificacion = ?
            ''', (identificacion,))
            conn.commit()
        return jsonify({"message": "Cliente eliminado con éxito"}), 200

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)