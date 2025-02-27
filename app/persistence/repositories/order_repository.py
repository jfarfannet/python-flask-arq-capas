# app/persistence/repositories/order_repository.py
from app.persistence.database import db
from app.persistence.models.order import Order, OrderItem
from app.persistence.models.menu_item import MenuItem
from datetime import datetime
from sqlalchemy import desc

class OrderRepository:
    """Repositorio para operaciones relacionadas con los pedidos."""
    
    def create_order(self, customer_id, restaurant_id, total_price, delivery_address, 
                    order_items, delivery_instructions=None, payment_method='cash'):
        """
        Crea un nuevo pedido.
        
        Args:
            customer_id: ID del cliente
            restaurant_id: ID del restaurante
            total_price: Precio total del pedido
            delivery_address: Dirección de entrega
            order_items: Lista de ítems del pedido [{'menu_item_id':1, 'quantity':2, 'item_price':10.5}, ...]
            delivery_instructions: Instrucciones adicionales para la entrega
            payment_method: Método de pago (cash, card, online)
            
        Returns:
            Order: Pedido creado
        """
        # Crear el pedido
        order = Order(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            total_price=total_price,
            delivery_address=delivery_address,
            delivery_instructions=delivery_instructions,
            payment_method=payment_method,
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Para obtener el ID del pedido
        
        # Crear los ítems del pedido
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item_data['menu_item_id'],
                quantity=item_data['quantity'],
                item_price=item_data['item_price'],
                special_instructions=item_data.get('special_instructions')
            )
            db.session.add(order_item)
        
        db.session.commit()
        return order
    
    def get_order_by_id(self, order_id):
        """Obtiene un pedido por su ID."""
        return Order.query.get(order_id)
    
    def get_orders_by_customer(self, customer_id, status=None, page=1, per_page=10):
        """Obtiene todos los pedidos de un cliente."""
        query = Order.query.filter_by(customer_id=customer_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(desc(Order.created_at)).paginate(page=page, per_page=per_page)
    
    def get_orders_by_restaurant(self, restaurant_id, status=None, page=1, per_page=10):
        """Obtiene todos los pedidos de un restaurante."""
        query = Order.query.filter_by(restaurant_id=restaurant_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(desc(Order.created_at)).paginate(page=page, per_page=per_page)
    
    def get_recent_orders(self, restaurant_id, limit=5):
        """Obtiene los pedidos más recientes de un restaurante."""
        return Order.query.filter_by(restaurant_id=restaurant_id).order_by(
            desc(Order.created_at)).limit(limit).all()
    
    def update_order_status(self, order_id, status):
        """Actualiza el estado de un pedido."""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        
        # Validar transiciones de estado válidas
        valid_transitions = {
            'pending': ['preparing', 'cancelled'],
            'preparing': ['ready', 'cancelled'],
            'ready': ['delivering', 'cancelled'],
            'delivering': ['delivered', 'cancelled'],
            'delivered': [],  # Estado final
            'cancelled': []   # Estado final
        }
        
        if status not in valid_transitions.get(order.status, []):
            raise ValueError(f"Transición de estado no válida: {order.status} -> {status}")
        
        order.status = status
        
        # Actualizar timestamps específicos según el estado
        if status == 'delivered':
            order.actual_delivery_time = datetime.utcnow()
        
        db.session.commit()
        return order
    
    def update_payment_status(self, order_id, payment_status):
        """Actualiza el estado de pago de un pedido."""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        
        # Validar estados de pago válidos
        valid_statuses = ['pending', 'completed', 'refunded', 'failed']
        if payment_status not in valid_statuses:
            raise ValueError(f"Estado de pago no válido: {payment_status}")
        
        order.payment_status = payment_status
        db.session.commit()
        return order
    
    def get_menu_item(self, menu_item_id):
        """Obtiene un ítem del menú por su ID."""
        return MenuItem.query.get(menu_item_id)
