# app/persistence/repositories/review_repository.py
from app.persistence.database import db
from app.persistence.models.review import Review
from app.persistence.models.order import Order
from app.persistence.models.restaurant import Restaurant

class ReviewRepository:
    """Repositorio para operaciones relacionadas con las reseñas."""
    
    def create_review(self, customer_id, restaurant_id, order_id, rating, comment=None, 
                     food_rating=None, delivery_rating=None):
        """
        Crea una nueva reseña.
        
        Args:
            customer_id: ID del cliente
            restaurant_id: ID del restaurante
            order_id: ID del pedido
            rating: Calificación general (1-5)
            comment: Comentario opcional
            food_rating: Calificación de la comida (1-5)
            delivery_rating: Calificación de la entrega (1-5)
            
        Returns:
            Review: Reseña creada
        """
        # Verificar si el pedido existe y es del cliente y restaurante indicados
        order = Order.query.get(order_id)
        if not order or order.customer_id != customer_id or order.restaurant_id != restaurant_id:
            raise ValueError("Pedido no válido para esta reseña")
        
        # Verificar si ya existe una reseña para este pedido
        existing_review = Review.query.filter_by(order_id=order_id).first()
        if existing_review:
            raise ValueError("Ya existe una reseña para este pedido")
        
        # Crear la reseña
        review = Review(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            order_id=order_id,
            rating=rating,
            comment=comment,
            food_rating=food_rating,
            delivery_rating=delivery_rating
        )
        
        db.session.add(review)
        db.session.commit()
        
        # Actualizar estadísticas de calificación del restaurante
        restaurant = Restaurant.query.get(restaurant_id)
        restaurant.update_rating_stats()
        db.session.commit()
        
        return review
    
    def get_review(self, review_id):
        """Obtiene una reseña por su ID."""
        return Review.query.get(review_id)
    
    def get_reviews_by_restaurant(self, restaurant_id, page=1, per_page=10):
        """Obtiene las reseñas de un restaurante paginadas."""
        return Review.query.filter_by(restaurant_id=restaurant_id)\
            .order_by(Review.created_at.desc())\
            .paginate(page=page, per_page=per_page)
    
    def get_reviews_by_customer(self, customer_id):
        """Obtiene las reseñas realizadas por un cliente."""
        return Review.query.filter_by(customer_id=customer_id)\
            .order_by(Review.created_at.desc()).all()
    
    def get_review_by_order(self, order_id):
        """Obtiene la reseña asociada a un pedido."""
        return Review.query.filter_by(order_id=order_id).first()
    
    def update_review(self, review_id, rating=None, comment=None, food_rating=None, delivery_rating=None):
        """Actualiza una reseña existente."""
        review = self.get_review(review_id)
        if not review:
            return None
        
        if rating:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        if food_rating:
            review.food_rating = food_rating
        if delivery_rating:
            review.delivery_rating = delivery_rating
            
        review.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Actualizar estadísticas de calificación del restaurante
        restaurant = Restaurant.query.get(review.restaurant_id)
        restaurant.update_rating_stats()
        db.session.commit()
        
        return review
    
    def delete_review(self, review_id):
        """Elimina una reseña."""
        review = self.get_review(review_id)
        if not review:
            return False
        
        restaurant_id = review.restaurant_id
        
        db.session.delete(review)
        db.session.commit()
        
        # Actualizar estadísticas de calificación del restaurante
        restaurant = Restaurant.query.get(restaurant_id)
        restaurant.update_rating_stats()
        db.session.commit()
        
        return True