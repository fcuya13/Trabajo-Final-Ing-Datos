

        var clienteSelect = document.getElementById("cliente");
        var direccionesSelect = document.getElementById("direccion");
        var direcciones = clienteSelect.options[clienteSelect.selectedIndex].getAttribute("data-direcciones").split(',');
        console.log(clienteSelect)
        // Limpia las opciones anteriores
        direccionesSelect.innerHTML = "";

        // Llena el campo de direcciones con las opciones obtenidas
        for (var i = 0; i < direcciones.length; i++) {
            var option = document.createElement("option");
            option.value = direcciones[i];
            option.text = direcciones[i];
            direccionesSelect.appendChild(option);
        }