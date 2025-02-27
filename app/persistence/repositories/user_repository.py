# app/persistence/repositories/user_repository.py
from app.persistence.database import db
from app.persistence.models.user import User
from app.persistence.models.customer import Customer
from app.persistence.models.restaurant import Restaurant
from datetime import datetime

class UserRepository:
    """Repositorio para operaciones relacionadas con los usuarios."""
    
    def create_user(self, username, email, password, role='customer'):
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario único
            email: Email único
            password: Contraseña sin encriptar
            role: Rol del usuario (customer, restaurant)
            
        Returns:
            User: Usuario creado
        """
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID."""
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        """Obtiene un usuario por su nombre de usuario."""
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        """Obtiene un usuario por su email."""
        return User.query.filter_by(email=email).first()
    
    def update_last_login(self, user_id):
        """Actualiza la fecha del último login."""
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            db.session.commit()
    
    def create_customer_profile(self, user_id, name, phone, address):
        """Crea un perfil de cliente para un usuario."""
        customer = Customer(
            user_id=user_id,
            name=name,
            phone=phone,
            address=address
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return customer
    
    def create_restaurant_profile(self, user_id, name, description, address, phone, cuisine_type, 
                                 opening_hours=None, logo_url=None):
        """Crea un perfil de restaurante para un usuario."""
        restaurant = Restaurant(
            user_id=user_id,
            name=name,
            description=description,
            address=address,
            phone=phone,
            cuisine_type=cuisine_type,
            opening_hours=opening_hours,
            logo_url=logo_url
        )
        
        db.session.add(restaurant)
        db.session.commit()
        
        return restaurant
    
    def update_customer_profile(self, customer_id, name=None, phone=None, address=None):
        """Actualiza el perfil de un cliente."""
        customer = Customer.query.get(customer_id)
        if not customer:
            return None
        
        if name:
            customer.name = name
        if phone:
            customer.phone = phone
        if address:
            customer.address = address
        
        db.session.commit()
        return customer
    
    def update_restaurant_profile(self, restaurant_id, **kwargs):
        """Actualiza el perfil de un restaurante."""
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None
        
        # Actualizar solo los campos proporcionados
        for key, value in kwargs.items():
            if hasattr(restaurant, key) and value is not None:
                setattr(restaurant, key, value)
        
        db.session.commit()
        return restaurant
    
    def update_restaurant_status(self, restaurant_id, is_active):
        """Actualiza el estado de un restaurante (activo/inactivo)."""
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None
        
        restaurant.is_active = is_active
        db.session.commit()
        return restaurant
    
    def change_password(self, user_id, new_password):
        """Cambia la contraseña de un usuario."""
        user = self.get_user_by_id(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return True
        return False
