document.getElementById('btnSiguienteRemitente').addEventListener('click', function() {
    document.getElementById('remitenteFormulario').style.display = 'none';
    document.getElementById('destinatarioFormulario').style.display = 'block';
});

document.getElementById('btnSiguienteDestinatario').addEventListener('click', function() {
    document.getElementById('destinatarioFormulario').style.display = 'none';
    document.getElementById('envioFormulario').style.display = 'block';
});

//consume el api de region y se le asigna las comuna dependiendo del id de la region
const comunasPorRegion = {
1: ["Arica", "Camarones", "Putre", "General Lagos"],
2: ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
3: ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama"],
4: ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"],
5: ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
6: ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví", "Casablanca", "Quilpué", "Villa Alemana", "Limache", "Olmué", "Quillota", "La Cruz", "La Calera", "Nogales", "Hijuelas", "San Antonio", "Cartagena", "El Tabo", "El Quisco", "Algarrobo", "Santo Domingo", "San Felipe", "Llaillay", "Catemu", "Putaendo", "Panquehue", "Santa María", "Los Andes", "Calle Larga", "Rinconada", "San Esteban", "Petorca", "La Ligua", "Cabildo", "Zapallar", "Papudo"],
7: ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"],
8: ["Rancagua", "Machalí", "Graneros", "Mostazal", "Requínoa", "Rengo", "Malloa", "San Vicente", "Pichidegua", "Las Cabras", "Peumo", "Coltauco", "Doñihue", "Coinco", "Olivar", "Gultro", "San Fernando", "Santa Cruz", "Chimbarongo", "Placilla", "Nancagua", "Palmilla", "Peralillo", "Pumanque", "Marchigüe", "Lolol", "Paredones", "Pichilemu", "Navidad", "La Estrella", "Litueche"],
9: ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"],
10: ["Chillán", "Chillán Viejo", "Quirihue", "Cobquecura", "Ninhue", "Trehuaco", "Coelemu", "Portezuelo", "Ránquil", "Bulnes", "Quillón", "San Ignacio", "El Carmen", "Pemuco", "Yungay", "Pinto", "San Carlos", "Ñiquén", "San Fabián", "San Nicolás"],
11: ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"],
12: ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"],
13: ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"],
14: ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"],
15: ["Coyhaique", "Lago Verde", "Aysén", "Cisnes", "Guaitecas", "Cochrane", "O'Higgins", "Tortel", "Chile Chico", "Río Ibáñez"],
16: ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos", "Antártica", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"]
};


function obtenerComunas() {
    var regionId = document.getElementById("region").value;
    var comunaSelect = document.getElementById("comuna");
    comunaSelect.innerHTML = '<option value="" selected>Seleccione una comuna</option>'; // Resetear las comunas

    if (regionId && comunasPorRegion[regionId]) {
        comunasPorRegion[regionId].forEach(comuna => {
            var option = document.createElement("option");
            option.text = comuna;
            option.value = comuna;
            comunaSelect.appendChild(option);
        });
    }
}




    
document.getElementById('btnCalcular').addEventListener('click', function() {
    var region = document.getElementById('region').value;
    var tipoPaquete = document.getElementById('tipoPaquete').value;
    var tipoEnvio = document.getElementById('tipoEnvio').value;

    console.log("Región seleccionada:", region);
    console.log("Tipo de paquete:", tipoPaquete);

    // Obtener el costo base del paquete según su tamaño
    var costoBasePorPaquete;
    switch (tipoPaquete) {
        case 'xs':
            costoBasePorPaquete = 3000;
            break;
        case 's':
            costoBasePorPaquete = 3900;
            break;
        case 'm':
            costoBasePorPaquete = 4800;
            break;
        case 'l':
            costoBasePorPaquete = 5700;
            break;
        case 'xl':
            costoBasePorPaquete = 6800;
            break;
        default:
            costoBasePorPaquete = 0;
    }

    console.log("Costo base del paquete:", costoBasePorPaquete);

    // Obtener el costo adicional por la región de destino
    var costoAdicionalPorRegion;
    switch (region) {
        case '7':
            costoAdicionalPorRegion = 500;
            break;
        case '6':
        case "8":
            costoAdicionalPorRegion = 700;
            break;
        case '5':
        case '9':
            costoAdicionalPorRegion = 950;
            break;
        case '4':
        case '10':
            costoAdicionalPorRegion = 1250;
            break;
        case '3':
        case '11':
            costoAdicionalPorRegion = 1600;
            break;
        case '2':
        case '12':
            costoAdicionalPorRegion = 2000;
            break;
        case '1':
            costoAdicionalPorRegion = 2450;
            break;
        case '13':
            costoAdicionalPorRegion = 2500;
            break;
        case '14':
            costoAdicionalPorRegion = 3000;
            break;
        case '15':
            costoAdicionalPorRegion = 3550;
            break;
        case '16':
            costoAdicionalPorRegion = 4150;
            break;
        default:
            costoAdicionalPorRegion = 0;
    }

    console.log("Costo adicional por región:", costoAdicionalPorRegion);

    // Calcular el costo total del envío
    var costoTotal = costoBasePorPaquete + costoAdicionalPorRegion;

    console.log("Costo total del envío:", costoTotal);

    // Aplicar el descuento si es envío express
    if (tipoEnvio === 'express') {
        costoTotal += 500; //costo adicional fijo por envío express
    }

    console.log("Costo total después del envío express:", costoTotal);

    // Actualizar el valor en el input 'amount'
    document.getElementById('totalAmount').value = costoTotal;
});

    
// Realizar una solicitud a la API para obtener las regiones
/*
fetch('https://dev.matiivilla.cl/duoc/location/region')
    .then(response => response.json())
    .then(data => {
        var regionSelect = document.getElementById("region");
        data.data.forEach(region => {
            var option = document.createElement("option");
            option.text = region.region;
            option.value = region.id;
            regionSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error obteniendo regiones:', error));

*/