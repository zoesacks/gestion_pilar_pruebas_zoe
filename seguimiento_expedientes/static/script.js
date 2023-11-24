let cantDocumentosEnTransito = 0
let cantDocumentosPendientes = 0
let usuario;
let documentos;

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
}

function mostrarDocumentos(documentos){
    const container = document.querySelector('.documentos-tabla')
    const filtrados = documentos.filter((documento) => documento.propietario.usuario.id === usuario.id || documento.destinatario == usuario.id)
    agregarCantidadDocumentos(filtrados.length)
    filtrados.forEach(documento => {
        let esPropio = usuario.id === documento.propietario.usuario.id && !documento.enTransito
        let enviadoPorUsuario = usuario.id === documento.propietario.usuario.id && documento.enTransito
        let pendienteDeAceptar = usuario.id === documento.destinatario && documento.enTransito
 
        enviadoPorUsuario ? cantDocumentosEnTransito++ : cantDocumentosPendientes++
        const row = container.insertRow();

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
            <button type="button" id ="${documento.id}" class="btn btn-primary ver-documento-boton" data-toggle="modal" data-target="#verDocumentoModal">
            <i class="fa fa-eye" aria-hidden="true"></i>
            </button>`;
        
    })
    agregarCantidadDocumentosEnTransitoYPendientes()
    agregarEventListenerBotones() 
}



function agregarCantidadDocumentosEnTransitoYPendientes(){
    document.querySelector("#documentos-en-transito").innerHTML = cantDocumentosEnTransito;
    document.querySelector("#documentos-pendientes").innerHTML = cantDocumentosPendientes;
}
function agregarCantidadDocumentos(cantidad) {
    document.querySelector("#cant-documentos").innerHTML = cantidad;
}

/*ver datos del documento*/

function agregarEventListenerBotones() {
    [...document.querySelectorAll('.ver-documento-boton')].forEach(function(item) {
    item.addEventListener('click', function() {
        obtenerDocumento(item.id)
    });
});
}

async function obtenerDocumento(id) {
    const response = await fetch(`http://127.0.0.1:8000/expedientes/api/documentos/${id}`)
    const documento = await response.json()
    console.log(documento)
    mostrarDatos(documento)
}

function mostrarDatos(documento){
    const modal = document.querySelector('#modal-ver-documento')
    modal.innerHTML = `
    <div class="container mt-4">
    <div class="card border-0">
        <div class="card-body">
            <div class="section">
                        <p><b class="text-primary text-uppercase">Propietario: </b> ${documento.propietario.usuario.first_name + " " + documento.propietario.usuario.last_name}</p>
                        <p><b class="text-primary text-uppercase">Usuario: </b> ${documento.propietario.usuario.username}</p>
                        ${ documento.destinatario ? ' <p><b class="text-primary text-uppercase">Destinatario: </b>${documento.destinatario}</p>' : '' }
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

/*Transferir documento*/ 






document.addEventListener('DOMContentLoaded', function() {
    if (window.location.hash == '#clearCache') {
        location.reload(true)
    }
})

/*
document.addEventListener('DOMContentLoaded', function() {

    //para que cuando 
    var transferirDocumentoBtns = document.querySelectorAll('.transferirDocumentoBtn');
    var modalDocumentoSelect = document.getElementById('documento');

    transferirDocumentoBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var tipoDocumento = btn.getAttribute('data-doc-tipo');
            var numeroDocumento = btn.getAttribute('data-doc-numero');
            var ejercicioDocumento = btn.getAttribute('data-doc-ejercicio');

            // Actualizar el modal con la información del documento seleccionado
            modalDocumentoSelect.value = btn.value;
            document.getElementById('tipoDocumento').innerText = tipoDocumento;
            document.getElementById('numeroDocumento').innerText = numeroDocumento;
            document.getElementById('ejercicioDocumento').innerText = ejercicioDocumento;

            // Actualizar también el valor seleccionado en el select del modal (si estás usando Bootstrap Select)
            $('#documento').selectpicker('val', btn.value);
        });
    });
});

*/