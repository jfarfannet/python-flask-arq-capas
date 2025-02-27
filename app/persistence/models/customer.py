# app/persistence/models/customer.py
from app.persistence.database import db
from datetime import datetime

class Customer(db.Model):
    """Modelo para la tabla de clientes."""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    orders = db.relationship('Order', backref='customer', lazy=True)
    favorite_restaurants = db.relationship('Restaurant', secondary='customer_favorites', 
                                           backref=db.backref('favorited_by', lazy='dynamic'))
    reviews = db.relationship('Review', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'
    
    def is_profile_complete(self):
        """Verifica si el perfil del cliente está completo."""
        return bool(self.name and self.phone and self.address)


# Tabla de relación muchos a muchos para favoritos
customer_favorites = db.Table('customer_favorites',
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)
