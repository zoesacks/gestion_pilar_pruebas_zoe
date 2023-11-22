let cantDocumentosEnTransito = 0
let cantDocumentosPendientes = 0
let usuario;

async function obtenerDocumentos() {
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/documentos")
    const documentos = await response.json()
    mostrarDocumentos(documentos)
    agregarCantidadDocumentos(documentos.length)
}

async function obtenerUsuario() {
    /*const response = await fetch("http://127.0.0.1:8000/expedientes/api/usuarioLogueado")
    usuario = await response.json()
    mostrarDocumentos(documentos)
    agregarCantidadDocumentos(documentos.length)*/
    console.log("dgfkjgfkjd")
}

document.addEventListener('DOMContentLoaded', obtenerUsuario)
document.addEventListener('DOMContentLoaded', obtenerDocumentos)

function mostrarDocumentos(documentos){
    
    const container = document.querySelector('.documentos-tabla')
    documentos.forEach(documento => {
        let esPropio = usuario === documento.propietario.id && !documento.enTransito
        let enviadoPorUsuario = usuario === documento.propietario.id && documento.enTransito
        let pendienteDeAceptar = usuario === documento.destinatario && documento.enTransito

        documento.en_transito ? cantDocumentosEnTransito++ : cantDocumentosPendientes++
        const row = container.insertRow();

                // Insert cells into the row
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
                    <button type="button" class="btn btn-primary">
                        <i class="fa fa-eye" aria-hidden="true"></i>
                    </button>
                `;
        console.log(documento)
        
    })
    agregarCantidadDocumentosEnTransitoYPendientes()
}


function agregarCantidadDocumentosEnTransitoYPendientes(){
    document.querySelector("#documentos-en-transito").innerHTML = cantDocumentosEnTransito;
    document.querySelector("#documentos-pendientes").innerHTML = cantDocumentosPendientes;
}

function agregarCantidadDocumentos(cantidad) {
    document.querySelector("#cant-documentos").innerHTML = cantidad;
}

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