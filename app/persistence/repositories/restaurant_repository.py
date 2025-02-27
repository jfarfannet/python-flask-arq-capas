# app/persistence/repositories/restaurant_repository.py
from app.persistence.database import db
from app.persistence.models.restaurant import Restaurant
from app.persistence.models.customer import Customer, customer_favorites
from app.persistence.models.order import Order
from app.persistence.models.review import Review
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta

class RestaurantRepository:
    """Repositorio para operaciones relacionadas con los restaurantes."""
    
    def get_restaurant_by_id(self, restaurant_id):
        """Obtiene un restaurante por su ID."""
        return Restaurant.query.get(restaurant_id)
    
    def get_restaurants(self, page=1, per_page=12, only_active=True):
        """Obtiene todos los restaurantes paginados."""
        query = Restaurant.query
        
        if only_active:
            query = query.filter_by(is_active=True)
        
        return query.paginate(page=page, per_page=per_page)
    
    def get_popular_restaurants(self, limit=6):
        """Obtiene los restaurantes más populares basados en calificaciones."""
        return Restaurant.query.filter_by(is_active=True).order_by(
            desc(Restaurant.average_rating), desc(Restaurant.total_ratings)).limit(limit).all()
    
    def search_restaurants(self, query=None, cuisine_type=None, page=1, per_page=12):
        """
        Busca restaurantes por nombre, descripción o tipo de cocina.
        
        Args:
            query: Texto de búsqueda
            cuisine_type: Tipo de cocina
            page: Número de página
            per_page: Resultados por página
            
        Returns:
            Pagination: Resultados paginados
        """
        search_query = Restaurant.query.filter_by(is_active=True)
        
        if query:
            search_terms = [f"%{term}%" for term in query.split()]
            conditions = []
            for term in search_terms:
                conditions.append(or_(
                    Restaurant.name.ilike(term),
                    Restaurant.description.ilike(term),
                    Restaurant.cuisine_type.ilike(term)
                ))
            search_query = search_query.filter(or_(*conditions))
        
        if cuisine_type:
            search_query = search_query.filter(Restaurant.cuisine_type == cuisine_type)
        
        return search_query.paginate(page=page, per_page=per_page)
    
    def get_cuisine_types(self):
        """Obtiene todos los tipos de cocina disponibles."""
        return db.session.query(Restaurant.cuisine_type, func.count(Restaurant.id).label('count'))\
            .filter(Restaurant.is_active == True)\
            .group_by(Restaurant.cuisine_type)\
            .order_by(func.count(Restaurant.id).desc())\
            .all()
    
    def add_to_favorites(self, customer_id, restaurant_id):
        """Añade un restaurante a los favoritos de un cliente."""
        customer = Customer.query.get(customer_id)
        restaurant = Restaurant.query.get(restaurant_id)
        
        if not customer or not restaurant:
            return False
        
        # Verificar si ya está en favoritos
        if restaurant in customer.favorite_restaurants:
            return True
        
        customer.favorite_restaurants.append(restaurant)
        db.session.commit()
        return True
    
    def remove_from_favorites(self, customer_id, restaurant_id):
        """Elimina un restaurante de los favoritos de un cliente."""
        customer = Customer.query.get(customer_id)
        restaurant = Restaurant.query.get(restaurant_id)
        
        if not customer or not restaurant:
            return False
        
        # Verificar si está en favoritos
        if restaurant not in customer.favorite_restaurants:
            return True
        
        customer.favorite_restaurants.remove(restaurant)
        db.session.commit()
        return True
    
    def get_favorites(self, customer_id):
        """Obtiene los restaurantes favoritos de un cliente."""
        customer = Customer.query.get(customer_id)
        if not customer:
            return []
        
        return customer.favorite_restaurants
    
    def is_favorite(self, customer_id, restaurant_id):
        """Verifica si un restaurante es favorito de un cliente."""
        result = db.session.query(customer_favorites).filter_by(
            customer_id=customer_id, restaurant_id=restaurant_id).first()
        return result is not None
    
    def get_restaurant_stats(self, restaurant_id):
        """
        Obtiene estadísticas del restaurante.
        
        Returns:
            Dict: Diccionario con estadísticas (pedidos totales, ingresos totales, etc.)
        """
        restaurant = self.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            return None
        
        # Calcular pedidos totales
        total_orders = Order.query.filter_by(restaurant_id=restaurant_id).count()
        
        # Calcular ingresos totales
        total_revenue = db.session.query(func.sum(Order.total_price)).filter(
            Order.restaurant_id == restaurant_id,
            Order.status.in_(['delivered'])
        ).scalar() or 0
        
        # Calcular pedidos por estado
        orders_by_status = {}
        for status in ['pending', 'preparing', 'ready', 'delivering', 'delivered', 'cancelled']:
            count = Order.query.filter_by(restaurant_id=restaurant_id, status=status).count()
            orders_by_status[status] = count
        
        # Calcular pedidos recientes (últimos 30 días)
        recent_date = datetime.utcnow() - timedelta(days=30)
        recent_orders = Order.query.filter(
            Order.restaurant_id == restaurant_id,
            Order.created_at >= recent_date
        ).count()
        
        # Obtener datos para gráfico de ventas (últimos 7 días)
        sales_data = []
        labels = []
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=6)
        
        for i in range(7):
            day = start_date + timedelta(days=i)
            next_day = day + timedelta(days=1)
            
            # Ingresos del día
            daily_revenue = db.session.query(func.sum(Order.total_price)).filter(
                Order.restaurant_id == restaurant_id,
                Order.status == 'delivered',
                Order.created_at >= day,
                Order.created_at < next_day
            ).scalar() or 0
            
            sales_data.append(float(daily_revenue))
            labels.append(day.strftime('%d/%m'))
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'orders_by_status': orders_by_status,
            'recent_orders': recent_orders,
            'average_rating': restaurant.average_rating,
            'total_ratings': restaurant.total_ratings,
            'chart_data': sales_data,
            'chart_labels': labels
        }
