console.log("prueba");
$(document).ready(function(){
    
})

$.validator.setDefaults({
    messages: {
      required: "Este campo es obligatorio."
    }
});

//validacion de formulario de agregar producto
$(function() {
    $("#agregarProductoForm").validate({
        rules: {
            txtSku: {
                required: true,
                minlength: 1
            },
            txtNombre: {
                required: true,
                minlength: 1,
                maxlength: 50
            },
            txtStock: {
                required: true,
                minlength: 1
            },
            txtPrecio: {
                required: true,
                minlength: 4
            },
            cmbCategoria: {
                required: true,
                minlength: 1
            },
            txtDescripcion: {
                required: true,
                minlength: 1
            },
            txtImg: {
                required: true,
                minlength: 1
            }
        },
        messages: {
            txtSku: {
                required: "Por favor, ingresa un SKU válido."
            },
            txtNombre: {
                required: "Por favor, ingresa un nombre válido."
            },
            txtStock: {
                required: "Por favor, ingresa un stock válido."
            },
            txtPrecio: {
                required: "Por favor, ingresa un precio válido."
            },
            cmbCategoria: {
                required: "Por favor, selecciona una categoría."
            },
            txtDescripcion: {
                required: "Por favor, ingresa una descripción válida."
            },
            txtImg: {
                required: "Por favor, ingresa una imagen."
            }
        }
    });
});

//validacion editar producto
$(function() {
    $("#editarProductoForm").validate({
        rules: {
            txtSku: {
                required: true,
                minlength: 1
            },
            txtNombre: {
                required: true,
                minlength: 1,
                maxlength: 50
            },
            txtStock: {
                required: true,
                minlength: 1
            },
            txtPrecio: {
                required: true,
                minlength: 4
            },
            cmbCategoria: {
                required: true,
                minlength: 1
            },
            txtDescripcion: {
                required: true,
                minlength: 1
            },
            
        },
        messages: {
            txtSku: {
                required: "Por favor, ingresa un SKU válido."
            },
            txtNombre: {
                required: "Por favor, ingresa un nombre válido."
            },
            txtStock: {
                required: "Por favor, ingresa un stock válido."
            },
            txtPrecio: {
                required: "Por favor, ingresa un precio válido."
            },
            cmbCategoria: {
                required: "Por favor, selecciona una categoría."
            },
            txtDescripcion: {
                required: "Por favor, ingresa una descripción válida."
            },
            txtImg: {
                required: "Por favor, ingresa una imagen."
            }
        }
    });
});


//validacion de login
$(document).ready(function() {
    $('#login-form').submit(function(event) {
      //event.preventDefault(); // Evita el envío del formulario

      var username = $('#username').val();
      var password = $('#password').val();

      if (username === '' || password === '') {
        // Muestra un toast de Bootstrap 5 con el mensaje de error
        $('.toast').toast('dispose'); // Cierra cualquier toast previo
        $('.toast').toast({
          delay: 3000,
          position: 'top-end' // Establece la posición del toast en la parte superior derecha
        });
        $('.toast .toast-body').text('Por favor, ingresa tanto el usuario como la contraseña');
        $('.toast').toast('show');
      } else {
        // Realiza alguna acción si la validación es exitosa
        // Aquí puedes enviar el formulario, hacer una petición AJAX, etc.
      }
    });
  });





//validacion de registro
$(document).ready(function() {
    $('#registration-formaa').submit(function(event) {
      //event.preventDefault(); // Evita el envío del formulario

      var username = $('#username').val();
      var password1 = $('#password1').val();
      var password2 = $('#password2').val();

      if (username === '' || password1 === '' || password2 === '') {
        // Muestra un toast de Bootstrap 5 con el mensaje de error
        $('.toast').toast('dispose'); // Cierra cualquier toast previo
        $('.toast').toast({
          delay: 3000,
          position: 'top-end' // Establece la posición del toast en la parte superior derecha
        });
        $('.toast .toast-body').text('Por favor, completa todos los campos');
        $('.toast').toast('show');
      } else if (password1 !== password2) {
        // Muestra un toast de Bootstrap 5 con el mensaje de error
        $('.toast').toast('dispose'); // Cierra cualquier toast previo
        $('.toast').toast({
          delay: 3000,
          position: 'top-end' // Establece la posición del toast en la parte superior derecha
        });
        $('.toast .toast-body').text('Las contraseñas no coinciden');
        $('.toast').toast('show');
      } else {
        // Realiza alguna acción si la validación es exitosa
        // Aquí puedes enviar el formulario, hacer una petición AJAX, etc.
      }
    });
  });








// Cambiar el color de fondo del elemento
$("#reloj").css("background-color", "#585858");

// Cambiar el color del texto del elemento
$("#reloj").css("color", "#ffffff");

// Cambiar el tamaño de fuente del elemento
$("#reloj").css("font-size", "18px");

// Cambiar el margen derecho del elemento
$("#reloj").css("margin-right", "50px");

$("#botonReloj").click(function() {
    $("#reloj").toggle();
  });