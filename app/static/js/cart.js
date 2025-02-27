/* app/presentation/static/js/cart.js */

function initializeCart() {
    // Obtener carrito del localStorage
    let cart = JSON.parse(localStorage.getItem('food_delivery_cart')) || {
        restaurant_id: null,
        items: []
    };
    
    // Actualizar contador del carrito en el navbar
    updateCartCounter();
    
    // Función para actualizar contador del carrito
    function updateCartCounter() {
        const totalItems = cart.items.reduce((total, item) => total + item.quantity, 0);
        $('#cart-count').text(totalItems);
    }
    
    // Función para actualizar el total del carrito
    function updateCartTotal() {
        const total = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        $('#cart-total').text(`$${total.toFixed(2)}`);
        
        // Actualizar botón de checkout
        if (cart.items.length > 0) {
            $('#checkout-btn').prop('disabled', false);
        } else {
            $('#checkout-btn').prop('disabled', true);
        }
    }
    
    // Función para renderizar los items del carrito
    function renderCartItems() {
        const $cartItems = $('#cart-items');
        $cartItems.empty();
        
        if (cart.items.length === 0) {
            $cartItems.html('<tr><td colspan="5" class="text-center py-4">Tu carrito está vacío</td></tr>');
            return;
        }
        
        cart.items.forEach(item => {
            const subtotal = item.price * item.quantity;
            const itemHtml = `
                <tr>
                    <td>${item.name}</td>
                    <td class="text-right">$${item.price.toFixed(2)}</td>
                    <td>
                        <div class="input-group input-group-sm quantity-control">
                            <div class="input-group-prepend">
                                <button class="btn btn-outline-secondary decrease-quantity" data-id="${item.id}" type="button">-</button>
                            </div>
                            <input type="text" class="form-control text-center item-quantity" value="${item.quantity}" readonly>
                            <div class="input-group-append">
                                <button class="btn btn-outline-secondary increase-quantity" data-id="${item.id}" type="button">+</button>
                            </div>
                        </div>
                    </td>
                    <td class="text-right">$${subtotal.toFixed(2)}</td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-danger remove-item" data-id="${item.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            $cartItems.append(itemHtml);
        });
        
        // Eventos para los botones de cantidad
        $('.increase-quantity').click(function() {
            const itemId = $(this).data('id');
            const item = cart.items.find(i => i.id === itemId);
            if (item) {
                item.quantity += 1;
                localStorage.setItem('food_delivery_cart', JSON.stringify(cart));
                renderCartItems();
                updateCartTotal();
                updateCartCounter();
            }
        });
        
        $('.decrease-quantity').click(function() {
            const itemId = $(this).data('id');
            const item = cart.items.find(i => i.id === itemId);
            if (item && item.quantity > 1) {
                item.quantity -= 1;
                localStorage.setItem('food_delivery_cart', JSON.stringify(cart));
                renderCartItems();
                updateCartTotal();
                updateCartCounter();
            }
        });
        
        $('.remove-item').click(function() {
            const itemId = $(this).data('id');
            cart.items = cart.items.filter(i => i.id !== itemId);
            
            // Si el carrito queda vacío, eliminar el restaurant_id
            if (cart.items.length === 0) {
                cart.restaurant_id = null;
            }
            
            localStorage.setItem('food_delivery_cart', JSON.stringify(cart));
            renderCartItems();
            updateCartTotal();
            updateCartCounter();
        });
    }
    
    // Inicializar vista del carrito si estamos en esa página
    if ($('#cart-items').length > 0) {
        renderCartItems();
        updateCartTotal();
        
        // Botón para vaciar carrito
        $('#clear-cart-btn').click(function() {
            if (confirm('¿Estás seguro de que deseas vaciar el carrito?')) {
                cart = {
                    restaurant_id: null,
                    items: []
                };
                localStorage.setItem('food_delivery_cart', JSON.stringify(cart));
                renderCartItems();
                updateCartTotal();
                updateCartCounter();
            }
        });
        
        // Checkout
        $('#checkout-form').submit(function(e) {
            // Los datos del carrito se enviarán en el procesamiento del formulario
            $('#cart-data').val(JSON.stringify(cart));
        });
    }
    
    // Botón de añadir al carrito desde la página de detalles
    $('.add-to-cart-btn').click(function() {
        const itemId = $(this).data('id');
        const itemName = $(this).data('name');
        const itemPrice = $(this).data('price');
        const restaurantId = $(this).data('restaurant');
        
        // Si el carrito tiene items de otro restaurante
        if (cart.restaurant_id !== null && cart.restaurant_id !== restaurantId) {
            if (!confirm('Tu carrito contiene items de otro restaurante. ¿Deseas vaciarlo para ordenar de este restaurante?')) {
                return;
            }
            
            // Vaciar carrito
            cart = {
                restaurant_id: null,
                items: []
            };
        }
        
        // Establecer restaurant_id si el carrito está vacío
        if (cart.restaurant_id === null) {
            cart.restaurant_id = restaurantId;
        }
        
        // Buscar si el item ya está en el carrito
        const existingItem = cart.items.find(item => item.id === itemId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.items.push({
                id: itemId,
                name: itemName,
                price: itemPrice,
                quantity: 1
            });
        }
        
        // Guardar carrito en localStorage
        localStorage.setItem('food_delivery_cart', JSON.stringify(cart));
        
        // Actualizar contador
        updateCartCounter();
        
        // Mostrar notificación
        showNotification(`${itemName} añadido al carrito`);
    });
    
    // Mostrar notificación
    function showNotification(message) {
        // Eliminar notificaciones anteriores
        $('.notification').remove();
        
        // Crear notificación
        const notification = $('<div class="notification"></div>')
            .text(message)
            .appendTo('body');
        
        // Mostrar y ocultar después de 3 segundos
        setTimeout(() => notification.addClass('show'), 100);
        setTimeout(() => {
            notification.removeClass('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}