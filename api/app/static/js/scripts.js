function showForm(formType) {
    const formContainer = document.getElementById('formContainer');
    let formHTML = '';

    switch (formType) {
        case 'crearCliente':
            formHTML = `
                <h2>Registrar Cliente</h2>
                <form id="clienteForm">
                    <!-- Formulario de registro de clientes -->
                    <label for="identificacion">Identificación:</label>
                    <input type="text" id="identificacion" name="identificacion" required>
                    <label for="nombres">Nombres:</label>
                    <input type="text" id="nombres" name="nombres" required>

                    <label for="apellidos">Apellidos:</label>
                    <input type="text" id="apellidos" name="apellidos" required>

                    <label for="tipoIdentificacion">Tipo de Identificación:</label>
                    <select id="tipoIdentificacion" name="tipoIdentificacion" required>
                        <option value="CC">Cédula de Ciudadanía (CC)</option>
                        <option value="TI">Tarjeta de Identidad (TI)</option>
                        <option value="CE">Cédula de Extranjería (CE)</option>
                        <option value="RC">Registro Civil (RC)</option>
                    </select>

                    <label for="fechaNacimiento">Fecha de Nacimiento:</label>
                    <input type="date" id="fechaNacimiento" name="fechaNacimiento" required>

                    <label for="numeroCelular">Número de Celular:</label>
                    <input type="text" id="numeroCelular" name="numeroCelular" required>

                    <label for="correoElectronico">Correo Electrónico:</label>
                    <input type="email" id="correoElectronico" name="correoElectronico" required>

                    <button type="submit">Registrar Cliente</button>
                </form>
                <p id="clienteResult" class="result"></p>
            `;
            break;

        case 'registrarServicio':
            formHTML = `
                <h2>Registrar Servicio</h2>
                <form id="servicioForm">
                    <!-- Formulario de registro de servicios -->
                    <label for="identificacionServicio">Identificación del Cliente:</label>
                    <input type="text" id="identificacionServicio" name="identificacionServicio" required>
                    <label for="servicio">Servicio:</label>
                    <select id="servicio" name="servicio" required>
                        <option value="Internet 200 MB">Internet 200 MB</option>
                        <option value="Internet 400 MB">Internet 400 MB</option>
                        <option value="Internet 600 MB">Internet 600 MB</option>
                        <option value="Directv Go">Directv Go</option>
                        <option value="Paramount+">Paramount+</option>
                        <option value="Win+">Win+</option>
                    </select>

                    <label for="fechaInicio">Fecha de Inicio:</label>
                    <input type="date" id="fechaInicio" name="fechaInicio" required>

                    <label for="ultimaFacturacion">Última Facturación:</label>
                    <input type="date" id="ultimaFacturacion" name="ultimaFacturacion" required>

                    <label for="ultimoPago">Último Pago:</label>
                    <input type="number" id="ultimoPago" name="ultimoPago" required>

                    <button type="submit">Registrar Servicio</button>
                </form>
                <p id="servicioResult" class="result"></p>
            `;
            break;

        case 'consultarCliente':
            formHTML = `
                <h2>Consultar Cliente</h2>
                <form id="consultaForm">
                    <!-- Formulario de consulta de clientes -->
                    <label for="consultaIdentificacion">Identificación del Cliente:</label>
                    <input type="text" id="consultaIdentificacion" name="consultaIdentificacion" required>
                    <button type="submit">Consultar Cliente</button>
                </form>
                <div id="consultaResult" class="result"></div>
            `;
            break;

        case 'actualizarCliente':
            formHTML = `
                <h2>Actualizar Cliente</h2>
                <form id="buscarClienteForm">
                    <label for="updateIdentificacion">Identificación del Cliente:</label>
                    <input type="text" id="updateIdentificacion" name="updateIdentificacion" required>
                    <button type="submit">Buscar Cliente</button>
                </form>
                <div id="clienteActualizarFormContainer" style="display:none;">
                    <form id="actualizarClienteForm">
                        <label for="updateNombres">Nuevos Nombres:</label>
                        <input type="text" id="updateNombres" name="updateNombres" required>
                        <small id="oldNombres" style="font-style: italic;"></small>

                        <label for="updateApellidos">Nuevos Apellidos:</label>
                        <input type="text" id="updateApellidos" name="updateApellidos" required>
                        <small id="oldApellidos" style="font-style: italic;"></small>

                        <label for="updateCorreoElectronico">Nuevo Correo Electrónico:</label>
                        <input type="email" id="updateCorreoElectronico" name="updateCorreoElectronico" required>
                        <small id="oldCorreoElectronico" style="font-style: italic;"></small>

                        <button type="submit">Actualizar Cliente</button>
                    </form>
                    <p id="updateClienteResult" class="result"></p>
                </div>
            `;
            break;

        case 'eliminarCliente':
            formHTML = `
                <h2>Eliminar Cliente</h2>
                <form id="eliminarClienteForm">
                    <!-- Formulario de eliminación de clientes -->
                    <label for="deleteIdentificacion">Identificación del Cliente:</label>
                    <input type="text" id="deleteIdentificacion" name="deleteIdentificacion" required>
                    <button type="submit">Eliminar Cliente</button>
                </form>
                <p id="deleteClienteResult" class="result"></p>
            `;
            break;
    }

    formContainer.innerHTML = formHTML;
    formContainer.style.display = 'block';
}


// Registrar Cliente
document.getElementById('clienteForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        identificacion: document.getElementById('identificacion').value,
        nombres: document.getElementById('nombres').value,
        apellidos: document.getElementById('apellidos').value,
        tipoIdentificacion: document.getElementById('tipoIdentificacion').value,
        fechaNacimiento: document.getElementById('fechaNacimiento').value,
        numeroCelular: document.getElementById('numeroCelular').value,
        correoElectronico: document.getElementById('correoElectronico').value,
    };

    fetch('http://localhost:5001/clientes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => document.getElementById('clienteResult').textContent = data.message)
      .catch(error => console.error('Error:', error));
});

// Registrar Servicio
document.getElementById('servicioForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        identificacion: document.getElementById('identificacionServicio').value,
        servicio: document.getElementById('servicio').value,
        fechaInicio: document.getElementById('fechaInicio').value,
        ultimaFacturacion: document.getElementById('ultimaFacturacion').value,
        ultimoPago: document.getElementById('ultimoPago').value,
    };

    fetch('http://localhost:5001/servicios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => document.getElementById('servicioResult').textContent = data.message)
      .catch(error => console.error('Error:', error));
});

// Consultar Cliente
document.getElementById('consultaForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const identificacion = document.getElementById('consultaIdentificacion').value;

    fetch(`http://localhost:5001/clientes/${identificacion}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          const resultDiv = document.getElementById('consultaResult');
          if (data.message) {
              resultDiv.textContent = data.message;
          } else {
              resultDiv.innerHTML = `
                <h3>Información del Cliente</h3>
                <p>Nombre: ${data.nombres} ${data.apellidos}</p>
                <p>Identificación: ${data.identificacion}</p>
                <p>Tipo de Identificación: ${data.tipo_identificacion}</p>
                <p>Fecha de Nacimiento: ${data.fecha_nacimiento}</p>
                <p>Teléfono: ${data.numero_celular}</p>
                <p>Correo: ${data.correo_electronico}</p>
                <h4>Servicios Contratados</h4>
                <ul>
                    ${data.servicios.map(s => `<li>${s.servicio} - Último Pago: ${s.ultimo_pago}</li>`).join('')}
                </ul>
              `;
          }
      })
      .catch(error => console.error('Error:', error));
});

// Actualizar Cliente 
document.getElementById('actualizarClienteForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        nombres: document.getElementById('updateNombres').value,
        apellidos: document.getElementById('updateApellidos').value,
        correoElectronico: document.getElementById('updateCorreoElectronico').value
    };

    const identificacion = document.getElementById('updateIdentificacion').value;

    console.log('Haciendo solicitud PUT para actualizar cliente:', identificacion);
    console.log('Datos enviados:', data);

    fetch(`http://localhost:5001/clientes/${identificacion}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
          console.log('Respuesta del servidor:', data);
          document.getElementById('updateClienteResult').textContent = data.message;
      })
      .catch(error => console.error('Error:', error));
});

// Eliminar Cliente 
document.getElementById('eliminarClienteForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const identificacion = document.getElementById('deleteIdentificacion').value;

    console.log('Haciendo solicitud DELETE para eliminar cliente:', identificacion);

    fetch(`http://localhost:5001/clientes/${identificacion}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          console.log('Respuesta del servidor:', data);
          document.getElementById('deleteClienteResult').textContent = data.message;
      })
      .catch(error => console.error('Error:', error));
});

// Buscar Cliente 
document.getElementById('buscarClienteForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const identificacion = document.getElementById('updateIdentificacion').value;

    console.log('Haciendo solicitud GET para buscar cliente:', identificacion);

    fetch(`http://localhost:5001/clientes/${identificacion}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          console.log('Respuesta del servidor:', data);
          if (data.message) {
              alert(data.message);
          } else {
              document.getElementById('oldNombres').textContent = `Valor actual: ${data.nombres}`;
              document.getElementById('oldApellidos').textContent = `Valor actual: ${data.apellidos}`;
              document.getElementById('oldCorreoElectronico').textContent = `Valor actual: ${data.correo_electronico}`;
              document.getElementById('clienteActualizarFormContainer').style.display = 'block';
          }
      })
      .catch(error => console.error('Error:', error));
});