# app/persistence/models/restaurant.py
from app.persistence.database import db
from datetime import datetime

class Restaurant(db.Model):
    """Modelo para la tabla de restaurantes."""
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False, index=True)
    logo_url = db.Column(db.String(255))
    opening_hours = db.Column(db.String(255))
    delivery_radius = db.Column(db.Float, default=5.0)  # km
    average_delivery_time = db.Column(db.Integer, default=30)  # minutos
    minimum_order = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos calculados (actualizados periódicamente)
    average_rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)
    
    # Relaciones
    menu_categories = db.relationship('MenuCategory', backref='restaurant', lazy=True, cascade="all, delete-orphan")
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
    def is_profile_complete(self):
        """Verifica si el perfil del restaurante está completo."""
        return bool(self.name and self.address and self.phone and self.cuisine_type)
    
    def update_rating_stats(self):
        """Actualiza las estadísticas de calificación."""
        if self.reviews:
            ratings = [review.rating for review in self.reviews]
            self.average_rating = sum(ratings) / len(ratings)
            self.total_ratings = len(ratings)
        else:
            self.average_rating = 0
            self.total_ratings = 0
