"""
Funciones de ayuda para la aplicación.
"""

def get_status_label(status):
    """
    Obtiene la etiqueta para un estado de pedido.
    
    Args:
        status (str): Estado del pedido
        
    Returns:
        str: Etiqueta del estado
    """
    status_labels = {
        'pending': 'Pendiente',
        'preparing': 'Preparando',
        'ready': 'Listo para entrega',
        'delivering': 'En camino',
        'delivered': 'Entregado',
        'cancelled': 'Cancelado'
    }
    
    return status_labels.get(status, status)


def get_status_color(status):
    """
    Obtiene el color de bootstrap para un estado de pedido.
    
    Args:
        status (str): Estado del pedido
        
    Returns:
        str: Clase de color de bootstrap
    """
    status_colors = {
        'pending': 'warning',
        'preparing': 'info',
        'ready': 'primary',
        'delivering': 'secondary',
        'delivered': 'success',
        'cancelled': 'danger'
    }
    
    return status_colors.get(status, 'secondary')


def get_payment_method_label(method):
    """
    Obtiene la etiqueta para un método de pago.
    
    Args:
        method (str): Método de pago
        
    Returns:
        str: Etiqueta del método
    """
    payment_methods = {
        'cash': 'Efectivo',
        'card': 'Tarjeta al entregar',
        'online': 'Pago en línea'
    }
    
    return payment_methods.get(method, method)