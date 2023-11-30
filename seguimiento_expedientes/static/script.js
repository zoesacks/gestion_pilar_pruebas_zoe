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
    eliminarDocumentosDelDOM()
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/documentos")
    documentos = await response.json()
    mostrarDocumentos(documentos)
    listarDocumentosFormulario()
}

function eliminarDocumentosDelDOM() {
    const container = document.querySelector('.documentos-tabla')
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
}

function mostrarDocumentos(documentos) {
    const container = document.querySelector('.documentos-tabla')
    const filtrados = documentos.filter((documento) => documento.propietario.usuario.id === usuario.id || documento.en_transito && documento.destinatario.usuario.id === usuario.id)
    agregarCantidadDocumentos(filtrados.length)
    cantDocumentosEnTransito =0
    cantDocumentosPendientes =0
    filtrados.forEach(documento => {
        let esPropio = usuario.id === documento.propietario.usuario.id && !documento.en_transito
        let enviadoPorUsuario = usuario.id === documento.propietario.usuario.id && documento.en_transito
        let pendienteDeAceptar = documento.en_transito && documento.destinatario.usuario.id === usuario.id

        enviadoPorUsuario ? cantDocumentosEnTransito++ : cantDocumentosPendientes++
        
        let row
        //si esta pendiente de aceptar se inserta primera
        if (pendienteDeAceptar) {
            row = container.insertRow(0);
        } else {
            row = container.insertRow()
        }
        
        row.classList.add('documento')
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

        if (pendienteDeAceptar) {
            accionesCell.innerHTML += `<button type="button" class="btn btn-success aceptar-transferencia-boton">
                <i class="fa fa-check-circle" aria-hidden="true"></i>
                </button>`
        }

        if (esPropio) {
            accionesCell.innerHTML += `
            <button type="button" class="btn btn-primary transferir-documento-boton" data-toggle="modal" data-target="#transferirDocumentoModal">
            <i class="fa fa-paper-plane" aria-hidden="true"></i>
            </button>`
        }

        accionesCell.innerHTML += `
           <button type="button" class="btn btn-primary ver-documento-boton" data-toggle="modal" data-target="#verDocumentoModal">
            <i class="fa fa-eye" aria-hidden="true"></i>
            </button>
            `
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

    [...document.querySelectorAll('.aceptar-transferencia-boton')].forEach(function (item) {
        item.addEventListener('click', function () {
            aceptarTransferencia(item.parentElement.parentElement.id)
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
    const destinatario = documento.destinatario ? documento.destinatario.usuario.first_name + " " + documento.destinatario.usuario.last_name : "Sos propietario"

    modal.innerHTML = `
    <div class="container">
    <div class="card border-0">
        <div class="card-body">
            <div class="section">
                        <p><b class="text-primary text-uppercase">Propietario: </b> ${documento.propietario.usuario.first_name + " " + documento.propietario.usuario.last_name}</p>
                        <p><b class="text-primary text-uppercase">Usuario: </b> ${documento.propietario.usuario.username}</p>
                        <p><b class="text-primary text-uppercase">Destinatario: </b> ${destinatario} </p>
                        <p><b class="text-primary text-uppercase">Observaciones: </b>${documento.observaciones ? documento.observacion : 'No hay observaciones'}
                        <p><b class="text-primary text-uppercase">Sector: </b>${documento.propietario.sector.nombre}</p>
                        <p><b class="text-primary text-uppercase">Fecha de alta: </b>${documento.fecha_alta}</p>
                        <p><b class="text-primary text-uppercase">Transferencias:&nbsp;&nbsp;</b><span id="transferenciasDocumento">
                                    <ul class="lista-transferencias-doc list-group max-height overflow-auto border-0" style="height: 20vh;"></ul>
                        </span></p>
                </div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 30px;"></div>
</div>
    `
    const lista = document.querySelector(".lista-transferencias-doc")
    lista.innerHTML = ""
    documento.transferencias.forEach(transferencia => {
        lista.innerHTML += `<li class="list-group-item">${transferencia.fecha} - ${transferencia.emisor.usuario.first_name} -> ${transferencia.receptor.usuario.first_name}</li>`
    })
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
    })
    const confirmarTransferenciaBoton = document.querySelector('.confirmar-transferencia-boton')
    const botonEnviarTransferencia = document.getElementById('boton-enviar-transferencia')
    formularioTransferirDocumento.addEventListener("change", (e) => {
        datoss = document.querySelectorAll('#tipoDocumento, #numeroDocumento, #ejercicioDocumento')
        let data = new FormData(formularioTransferirDocumento)
        camposCompletos = Array.from(data).length > 3
        if (camposCompletos) {
            botonEnviarTransferencia.disabled = false;
        }
    })


    confirmarTransferenciaBoton.addEventListener('click', () => {
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
        const lista = document.querySelector(".lista-transferencias")
        lista.innerHTML = ""
        res.transferencias.forEach(transferencia => {
            lista.innerHTML += `<li class="list-group-item">${transferencia.fecha} - ${transferencia.emisor.usuario.first_name} -> ${transferencia.receptor.usuario.first_name}</li>`
        })
        console.log(res)
    })

    console.log(doc)
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
        option.setAttribute("value", `${usuario.id}`)
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
    return { id_documento: idDocumento, id_usuario: idDestinatario, observacion: observaciones }

}

function transferirDocumento(data) {

    // Obtener el valor del token CSRF del documento
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    fetch("http://127.0.0.1:8000/expedientes/api/transferencia/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Agregar el token CSRF al encabezado
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {

            obtenerDocumentos()
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });


}

/*Transferir documento boton*/

function filtrarDocumentoFormulario(id) {

    selectDocumentos.style.display = 'none';
    for (let i = 0; i < selectDocumentos.options.length; i++) {
        if (selectDocumentos.options[i].value === id) {
            selectDocumentos.options[i].selected = true
            break
        }
    }

    const doc = obtenerDocumento(id)
    doc.then(res => {
        document.querySelector('.texto-documento-form').innerHTML = `Documento seleccionado: ${res.tipo.numero} - ${res.numero}`
        datosDocumentoFormulario[0].textContent = res.tipo.descripcion
        datosDocumentoFormulario[1].textContent = res.numero
        datosDocumentoFormulario[2].textContent = res.ejercicio
        const lista = document.querySelector(".lista-transferencias")
        lista.innerHTML = ""
        res.transferencias.forEach(transferencia => {
            lista.innerHTML += `<li class="list-group-item">${transferencia.fecha} - ${transferencia.emisor.usuario.first_name} -> ${transferencia.receptor.usuario.first_name}</li>`
        })
        console.log(res)
    })

    

    const botonCerrarTransferencia = document.querySelector('.boton-cerrar-transferencia')

    //cuando se cierra, vuelven a aparecer las transferencias

    botonCerrarTransferencia.addEventListener('click', reestablecerElementosOption)
}



/*Aceptar transferencia*/

function aceptarTransferencia(id) {
    transferirDocumento({ id_documento: id })
}


function reestablecerElementosOption() {
    document.querySelector('.texto-documento-form').innerHTML = "Documento: "
    selectDocumentos.style.display = 'block';
    datosDocumentoFormulario[0].textContent = ""
    datosDocumentoFormulario[1].textContent = ""
    datosDocumentoFormulario[2].textContent = ""
}

/*Busqueda de documentos*/

document.addEventListener('DOMContentLoaded', function () {
    const formBusqueda = document.querySelector('.form-busqueda')
    formBusqueda.addEventListener('input', (e) => {
        const value = e.target.value
        let tr = document.querySelectorAll('.documento')

        tr.forEach(documento => {

            let incluye = Array.from(documento.childNodes).some(childNode => {
                return childNode.nodeType === 1 && childNode.textContent.toLowerCase().includes(value)
            });

            if (incluye) {
                documento.classList.remove('d-none')
            } else {
                documento.classList.add('d-none')
            }

        })
    })
})



document.addEventListener('DOMContentLoaded', function () {
    if (window.location.hash == '#clearCache') {
        location.reload(true)
    }
})
