# app/persistence/repositories/menu_repository.py
from app.persistence.database import db
from app.persistence.models.restaurant import Restaurant
from app.persistence.models.menu_item import MenuCategory, MenuItem

class MenuRepository:
    """Repositorio para operaciones relacionadas con el menú."""
    
    def get_restaurant(self, restaurant_id):
        """Obtiene un restaurante por su ID."""
        return Restaurant.query.get(restaurant_id)
    
    def get_menu_categories(self, restaurant_id):
        """Obtiene todas las categorías del menú de un restaurante."""
        return MenuCategory.query.filter_by(
            restaurant_id=restaurant_id, 
            is_active=True
        ).order_by(MenuCategory.order).all()
    
    def get_category(self, category_id):
        """Obtiene una categoría por su ID."""
        return MenuCategory.query.get(category_id)
    
    def create_category(self, restaurant_id, name, description=None, order=0):
        """Crea una nueva categoría en el menú."""
        category = MenuCategory(
            restaurant_id=restaurant_id,
            name=name,
            description=description,
            order=order
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category
    
    def update_category(self, category_id, name=None, description=None, order=None, is_active=None):
        """Actualiza una categoría del menú."""
        category = self.get_category(category_id)
        if not category:
            return None
        
        if name:
            category.name = name
        if description is not None:
            category.description = description
        if order is not None:
            category.order = order
        if is_active is not None:
            category.is_active = is_active
        
        db.session.commit()
        return category
    
    def delete_category(self, category_id):
        """Elimina una categoría (marcándola como inactiva)."""
        category = self.get_category(category_id)
        if not category:
            return False
        
        category.is_active = False
        db.session.commit()
        return True
    
    def get_menu_items(self, restaurant_id, category_id=None, only_available=True):
        """
        Obtiene los ítems del menú de un restaurante.
        
        Args:
            restaurant_id: ID del restaurante
            category_id: ID de la categoría (opcional)
            only_available: Si es True, solo devuelve ítems disponibles
            
        Returns:
            List: Lista de ítems del menú
        """
        query = MenuItem.query.filter_by(restaurant_id=restaurant_id)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if only_available:
            query = query.filter_by(is_available=True)
        
        return query.all()
    
    def get_menu_item(self, item_id):
        """Obtiene un ítem del menú por su ID."""
        return MenuItem.query.get(item_id)
    
    def create_menu_item(self, restaurant_id, category_id, name, price, description=None, 
                        image_url=None, is_featured=False):
        """Crea un nuevo ítem en el menú."""
        item = MenuItem(
            restaurant_id=restaurant_id,
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            is_featured=is_featured
        )
        
        db.session.add(item)
        db.session.commit()
        
        return item
    
    def update_menu_item(self, item_id, **kwargs):
        """Actualiza un ítem del menú."""
        item = self.get_menu_item(item_id)
        if not item:
            return None
        
        # Actualizar solo los campos proporcionados
        for key, value in kwargs.items():
            if hasattr(item, key) and value is not None:
                setattr(item, key, value)
        
        db.session.commit()
        return item
    
    def delete_menu_item(self, item_id):
        """Elimina un ítem del menú."""
        item = self.get_menu_item(item_id)
        if not item:
            return False
        
        db.session.delete(item)
        db.session.commit()
        return True
