# app/persistence/models/__init__.py
"""
Inicialización del paquete de modelos.

Este archivo permite que los modelos sean importados directamente desde app.persistence.models,
por ejemplo: from app.persistence.models import User, Customer
"""

# Para evitar importaciones circulares, importamos los modelos cuando se utilice
# este paquete, no durante la inicialización

__all__ = [
    'User', 
    'Customer', 
    'customer_favorites',
    'Restaurant', 
    'MenuCategory', 
    'MenuItem', 
    'Order', 
    'OrderItem', 
    'Review'
]

# Estas importaciones se harán bajo demanda
# from app.persistence.models.user import User
# from app.persistence.models.customer import Customer, customer_favorites
# from app.persistence.models.restaurant import Restaurant
# from app.persistence.models.menu_item import MenuCategory, MenuItem
# from app.persistence.models.order import Order, OrderItem
# from app.persistence.models.review import Review