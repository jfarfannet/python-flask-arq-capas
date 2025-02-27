/* app/presentation/static/js/main.js */

$(document).ready(function() {
    // Activar tooltips de Bootstrap
    $('[data-toggle="tooltip"]').tooltip();
    
    // Activar popovers de Bootstrap
    $('[data-toggle="popover"]').popover();
    
    // Cerrar alertas automáticamente
    $('.alert').not('.alert-permanent').delay(5000).fadeOut(500);
    
    // Activar validación de formularios de Bootstrap
    const forms = document.getElementsByClassName('needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Contador de caracteres para textareas
    $('textarea[maxlength]').each(function() {
        const $textarea = $(this);
        const maxLength = $textarea.attr('maxlength');
        
        // Crear contador
        const $counter = $('<small class="form-text text-muted character-counter"></small>')
            .insertAfter($textarea);
        
        // Función para actualizar contador
        function updateCounter() {
            const remaining = maxLength - $textarea.val().length;
            $counter.text(`${remaining} caracteres restantes`);
        }
        
        // Evento para actualizar contador
        $textarea.on('input', updateCounter);
        
        // Inicializar contador
        updateCounter();
    });
    
    // Función para mostrar mensajes de error de validación personalizados
    function displayValidationErrors(errors, formId) {
        // Limpiar errores previos
        $(`#${formId} .invalid-feedback`).remove();
        $(`#${formId} .is-invalid`).removeClass('is-invalid');
        
        // Mostrar nuevos errores
        for (const field in errors) {
            const errorMessage = errors[field];
            const $field = $(`#${formId} [name="${field}"]`);
            
            $field.addClass('is-invalid');
            $field.after(`<div class="invalid-feedback">${errorMessage}</div>`);
        }
    }
    
    // Formularios AJAX
    $('.ajax-form').submit(function(e) {
        e.preventDefault();
        
        const $form = $(this);
        const formId = $form.attr('id');
        const url = $form.attr('action');
        const method = $form.attr('method');
        const formData = new FormData(this);
        
        $.ajax({
            url: url,
            type: method,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Verificar si se recibió una redirección
                if (response.redirect) {
                    window.location.href = response.redirect;
                    return;
                }
                
                // Verificar si se recibió un mensaje de éxito
                if (response.message) {
                    // Mostrar mensaje de éxito
                    const $alert = $('<div class="alert alert-success alert-dismissible fade show"></div>')
                        .text(response.message)
                        .append('<button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>')
                        .prependTo($form.closest('.card').find('.card-body'));
                    
                    // Ocultar después de 5 segundos
                    $alert.delay(5000).fadeOut(500);
                    
                    // Limpiar formulario si se indica
                    if (response.clear_form) {
                        $form[0].reset();
                    }
                }
                
                // Ejecutar callback personalizado si existe
                if (window[`${formId}_success`] && typeof window[`${formId}_success`] === 'function') {
                    window[`${formId}_success`](response);
                }
            },
            error: function(xhr) {
                let errorMessage = 'Ha ocurrido un error al procesar la solicitud.';
                
                // Verificar si se recibió un JSON con errores
                if (xhr.responseJSON) {
                    // Si hay errores de validación
                    if (xhr.responseJSON.errors) {
                        displayValidationErrors(xhr.responseJSON.errors, formId);
                    }
                    
                    // Si hay un mensaje de error general
                    if (xhr.responseJSON.error) {
                        errorMessage = xhr.responseJSON.error;
                    }
                }
                
                // Mostrar mensaje de error
                const $alert = $('<div class="alert alert-danger alert-dismissible fade show"></div>')
                    .text(errorMessage)
                    .append('<button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>')
                    .prependTo($form.closest('.card').find('.card-body'));
                
                // Ocultar después de 5 segundos
                $alert.delay(5000).fadeOut(500);
                
                // Ejecutar callback personalizado si existe
                if (window[`${formId}_error`] && typeof window[`${formId}_error`] === 'function') {
                    window[`${formId}_error`](xhr);
                }
            }
        });
    });
    
    // Funciones para el carrito
    if (typeof initializeCart === 'function') {
        initializeCart();
    }
});
