//Inicializamos variables de tarjetas
let cantTickets = 0;
let sol_finalizadas = 0;
let proceso = 0;
let solPendientes = 0;

//Declaramos la lista de datos

async function obtenerTickets() {
    const response = await fetch("http://127.0.0.1:8000/mesa-de-ayuda/api")
    tickets = await response.json()
    mostrarTarjetas(tickets)
    mostrarTickets(tickets)
}

obtenerTickets()

function mostrarTickets(tickets) {
    //Tomamos la tabla del dom
    const container = document.querySelector('#dataTable')

    //Recorremos los tickets para agregar las filas de la tabla
    tickets.forEach(ticket => {
        console.log(ticket)
        //Insertamos la fila
        let row = container.insertRow()
        row.classList.add()
        //Insertamos las celdas
        const fechaCell = row.insertCell(0);
        fechaCell.textContent = ticket.fecha.substring(0,10);

        const solicitanteCell = row.insertCell(1);
        solicitanteCell.textContent = ticket.usuario.username;

        const asuntoCell = row.insertCell(2);
        asuntoCell.textContent = ticket.titulo;

        const asignadoCell = row.insertCell(3);
        ticket.desarrollador ? asignadoCell.textContent = ticket.desarrollador : asignadoCell.textContent = "No asignado"
        
        const estadoCell = row.insertCell(4);
        estadoCell.innerHTML = agregarEstado(ticket.estado);

        const comentarioCell = row.insertCell(5)
        ticket.comentarios.length ? comentarioCell.textContent = "Hay comentarios" : comentarioCell.textContent = "No hay comentarios"

        const botonesCell = row.insertCell(6)
        botonesCell.innerHTML+=`
        <button type="button" class="btn btn-primary ver-ticket-boton" data-toggle="modal" data-target="#verTicketModal">
         <i class="fa fa-eye" aria-hidden="true"></i>
         </button>
         `


    })
    
}

function agregarEstado(estado){
    let color = "red"
    if(estado === "Terminado") {
        color = "green"
    } else if (estado === "En proceso"){
        color = "blue"
    }

    return `<span class="badge badge-pill badge-primary" style="background-color: ${color};" >${estado}</span>`
}


function mostrarTarjetas(tickets){
    //Asignamos la cantidad de tickets
    cantTickets = tickets.length

    //Recorremos los tickets y actualizamos variables 
    tickets.forEach(ticket => {

        if(ticket.estado === "Pendiente"){
            solPendientes+=1
        } else if(ticket.estado === "En proceso"){
            proceso +=1
        } else {
            sol_finalizadas += 1
        }

    })

    //Tomamos los elementos del dom
    const divTotalTickets = document.querySelector('#solicitudes-totales')
    const divPendientes = document.querySelector('#sol-pendientes')
    const divproceso = document.querySelector('#proceso')
    const divsol_finalizadas = document.querySelector('#sol_finalizadas')

    //Actualizamos el texto de los divs con la cantidad de tickets y su estado
    divTotalTickets.textContent =cantTickets
    divPendientes.textContent = solPendientes  
    divproceso.textContent = proceso
    divsol_finalizadas.textContent = sol_finalizadas
}

/*Agregar ticket*/

let formularioTransferirTicket = document.querySelector(".enviar-ticket-formulario")

formularioTransferirTicket.addEventListener('submit', (e) => {
    
    e.preventDefault()
    console.log("submit")
    capturarDatos()
})

function capturarDatos() {

    /*let data = new FormData(formularioTransferirTicket)
    data = Array.from(data)
    console.log(data)*/
    const titulo = document.querySelector(".input-asunto").value
    const detalle = document.querySelector(".textarea-descripcion").value
    agregarTicket( { titulo: titulo, detalle: detalle } )
}

function agregarTicket(data) {

    // Obtener el valor del token CSRF del documento
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    
    fetch("http://127.0.0.1:8000/mesa-de-ayuda/api/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Agregar el token CSRF al encabezado
        },
        body: JSON.stringify({ titulo: "nuevo", detalle: "nuevo" })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            obtenerTickets()
            
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
        
        
}