async function obtenerDocumentos() {
    const response = await fetch("http://127.0.0.1:8000/expedientes/api/documentos")
    const documentos = await response.json()
    mostrarDocumentos(documentos)
  }

document.addEventListener('DOMContentLoaded', obtenerDocumentos)

function mostrarDocumentos(documentos){
    const container = document.querySelector('.documentos-container')
    documentos.map(documento => {
        let li= document.createElement("li")
        li.textContent += `${documento.tipo} - ${documento.numero} - ${documento.numero} -${documento.ejercicio}`
        container.appendChild(li)
        
        console.log(documento)
        
    })
}


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

