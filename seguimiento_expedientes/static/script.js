let cantDocumentosEnTransito = 0
let cantDocumentosPendientes = 0
let usuario;
let documentos;
let opcionesDocumento;

/*obtener usuario*/

document.addEventListener('DOMContentLoaded', obtenerUsuario)

async function obtenerUsuario() {
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/usuarioLogueado")
    usuario = await response.json()
    
}

/*mostrar tabla con documentos*/
document.addEventListener('DOMContentLoaded', obtenerDocumentos)

async function obtenerDocumentos() {
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/documentos")
    documentos = await response.json()
    mostrarDocumentos(documentos)
    listarDocumentosFormulario()
    
}

function mostrarDocumentos(documentos) {
    const container = document.querySelector('.documentos-tabla')
    const filtrados = documentos.filter((documento) => documento.propietario.usuario.id === usuario.id || documento.destinatario == usuario.id)
    agregarCantidadDocumentos(filtrados.length)
    filtrados.forEach(documento => {
        let esPropio = usuario.id === documento.propietario.usuario.id && !documento.enTransito
        let enviadoPorUsuario = usuario.id === documento.propietario.usuario.id && documento.enTransito
        let pendienteDeAceptar = usuario.id === documento.destinatario && documento.enTransito

        enviadoPorUsuario ? cantDocumentosEnTransito++ : cantDocumentosPendientes++
        const row = container.insertRow();
        row.id = documento.id;
        const tipoDescripcionCell = row.insertCell(0);
        tipoDescripcionCell.textContent = documento.tipo.descripcion;
        const tipoNumeroCell = row.insertCell(1);
        tipoNumeroCell.textContent = documento.tipo.numero + '-' + documento.numero;
        const ejercicioCell = row.insertCell(2);
        ejercicioCell.textContent = documento.ejercicio;
        const estadoCell = row.insertCell(3);

        if (pendienteDeAceptar) {
            estadoCell.textContent = 'Pendiente de recepcion';
        } else if (enviadoPorUsuario) {
            estadoCell.textContent = 'Enviado por mi'
        } else if (esPropio) {
            estadoCell.textContent = 'En posesion'
        }
        const accionesCell = row.insertCell(4);

        if (documento.en_transito) {
            accionesCell.innerHTML += `<button type="button" class="btn btn-success">
                <i class="fa fa-check-circle" aria-hidden="true"></i>
                </button>`
        }

        accionesCell.innerHTML += `
            <button type="button" class="btn btn-primary ver-documento-boton" data-toggle="modal" data-target="#verDocumentoModal">
            <i class="fa fa-eye" aria-hidden="true"></i>
            </button>
            <button type="button" class="btn btn-primary transferir-documento-boton" data-toggle="modal" data-target="#transferirDocumentoModal">
            <i class="fa fa-paper-plane" aria-hidden="true"></i>
            </button>`
            

    })
    agregarCantidadDocumentosEnTransitoYPendientes()
    agregarEventListenerBotones()
}



function agregarCantidadDocumentosEnTransitoYPendientes() {
    document.querySelector("#documentos-en-transito").innerHTML = cantDocumentosEnTransito;
    document.querySelector("#documentos-pendientes").innerHTML = cantDocumentosPendientes;
}
function agregarCantidadDocumentos(cantidad) {
    document.querySelector("#cant-documentos").innerHTML = cantidad;
}

/*ver datos del documento*/

function agregarEventListenerBotones() {
    [...document.querySelectorAll('.ver-documento-boton')].forEach(function (item) {
        item.addEventListener('click', function () {    
          obtenerDocumento(item.parentElement.parentElement.id)
        });
    });

    [...document.querySelectorAll('.transferir-documento-boton')].forEach(function (item) {
        item.addEventListener('click', function () {    
          filtrarDocumentoFormulario(item.parentElement.parentElement.id)
        });
    });
}

async function obtenerDocumento(id) {
    const response = await fetch(`http://127.0.0.1:8000/expedientes/api/documentos/${id}`)
    const documento = await response.json()
    mostrarDatos(documento)
    return documento
}

function mostrarDatos(documento) {
    const modal = document.querySelector('#modal-ver-documento')
    modal.innerHTML = `
    <div class="container mt-4">
    <div class="card border-0">
        <div class="card-body">
            <div class="section">
                        <p><b class="text-primary text-uppercase">Propietario: </b> ${documento.propietario.usuario.first_name + " " + documento.propietario.usuario.last_name}</p>
                        <p><b class="text-primary text-uppercase">Usuario: </b> ${documento.propietario.usuario.username}</p>
                        ${documento.destinatario ? ' <p><b class="text-primary text-uppercase">Destinatario: </b>${documento.destinatario}</p>' : ''}
                        <p><b class="text-primary text-uppercase">Observaciones: </b>${documento.observaciones ? documento.observacion : 'No hay observaciones'}
                        <p><b class="text-primary text-uppercase">Sector: </b>${documento.propietario.sector.nombre}</p>
                        <p><b class="text-primary text-uppercase">Fecha de alta: </b>${documento.fecha_alta}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 30px;"></div>
</div>
    `
}

/*Llenar formulario con datos*/

let botonFormulario
let usuarios
let selectDocumentos
let datosDocumentoFormulario

document.addEventListener('DOMContentLoaded', funcionesAlCargarDOM)

function funcionesAlCargarDOM() {
    botonFormulario = document.getElementById('nuevaTransferenciaBoton')
    obtenerUsuarios()
    selectDocumentos = document.querySelector('#seleccionar-documento')
    selectDocumentos.addEventListener("change", completarDatosDocumento)
    datosDocumentoFormulario = document.querySelectorAll('#tipoDocumento, #numeroDocumento, #ejercicioDocumento')
    formularioTransferirDocumento = document.querySelector('.enviar-transferencia-formulario')
    formularioTransferirDocumento.addEventListener("submit", (e) => {
        e.preventDefault()
        e.stopPropagation()
        transferirDocumento(capturarDatos()) 
    })
}

function completarDatosDocumento() {
    let elegido = this.options[this.selectedIndex]
    const doc = obtenerDocumento(elegido.value)
    doc.then(res => {
        datosDocumentoFormulario[0].textContent = res.tipo.descripcion
        datosDocumentoFormulario[1].textContent = res.numero
        datosDocumentoFormulario[2].textContent = res.ejercicio
    })

}

async function obtenerUsuarios() {
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/usuarios")
    usuarios = await response.json()
    listarUsuariosFormulario()
}

function listar() {
    listarDocumentosFormulario()
    listarUsuariosFormulario()
}

function listarUsuariosFormulario() {
    const selectUsuarios = document.querySelector('#seleccionar-usuario')
    usuarios.forEach((usuario) => {
        const option = document.createElement('option')
        option.setAttribute("value", `${usuario.usuario.id}`)
        option.append(document.createTextNode(`${usuario.usuario.username} - Sector: ${usuario.sector.nombre}`))
        selectUsuarios.appendChild(option)
    })
}

function listarDocumentosFormulario(id) {
    
    documentos.filter(doc => usuario.id === doc.propietario.usuario.id && !doc.enTransito).forEach((doc) => {
        const option = document.createElement('option')
        option.setAttribute("value", `${doc.id}`)
        option.append(document.createTextNode(`${doc.tipo.numero} - ${doc.numero}`))
        selectDocumentos.appendChild(option)
    })
}

/*Transferir documento*/

let formularioTransferirDocumento

function capturarDatos() {
    let data = new FormData(formularioTransferirDocumento)
    data = Array.from(data)
    const idDocumento = parseInt(data[1][1])
    const idDestinatario = parseInt(data[2][1])
    const observaciones = data[3][1]
    return {id_documento: idDocumento, id_usuario: idDestinatario, observacion: observaciones}
    
}

function transferirDocumento(data) {

    console.log(JSON.stringify(data))
    // Obtener el valor del token CSRF del documento
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    
    fetch("http://127.0.0.1:8000/expedientes/api/transferencia/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Agregar el token CSRF al encabezado
        }, 
        body: JSON.stringify({
            id_documento: 4,
            id_usuario: 2,
            observacion: ""
        })
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
    });

}


/*Transferir documento boton*/

function filtrarDocumentoFormulario(id){
    selectDocumentos.style.display = 'none';
    const doc = obtenerDocumento(id)
    doc.then(res => {
        document.querySelector('.texto-documento-form').innerHTML = `Documento seleccionado: ${res.tipo.numero} - ${res.numero}`
        datosDocumentoFormulario[0].textContent = res.tipo.descripcion
        datosDocumentoFormulario[1].textContent = res.numero
        datosDocumentoFormulario[2].textContent = res.ejercicio
    })

    const botonCerrarTransferencia = document.querySelector('.boton-cerrar-transferencia')
    
    //cuando se cierra, vuelven a aparecer las transferencias
    botonCerrarTransferencia.addEventListener('click', reestablecerElementosOption)

}

function reestablecerElementosOption() {
    document.querySelector('.texto-documento-form').innerHTML = "Documento: "
    selectDocumentos.style.display = 'block';
    datosDocumentoFormulario[0].textContent = ""
    datosDocumentoFormulario[1].textContent = ""
    datosDocumentoFormulario[2].textContent = ""
}


document.addEventListener('DOMContentLoaded', function () {
    if (window.location.hash == '#clearCache') {
        location.reload(true)
    }
})
