# app/business/auth_service.py
from app.persistence.repositories.user_repository import UserRepository
from datetime import datetime

class AuthService:
    """Servicio para gestionar la autenticación de usuarios."""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def register_user(self, username, email, password, role='customer'):
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username (str): Nombre de usuario único
            email (str): Correo electrónico único
            password (str): Contraseña del usuario
            role (str): Rol del usuario ('customer' o 'restaurant')
            
        Returns:
            User: El usuario creado
            
        Raises:
            ValueError: Si el nombre de usuario o email ya están en uso
        """
        # Verificar si el nombre de usuario ya existe
        if self.repository.get_user_by_username(username):
            raise ValueError(f"El nombre de usuario '{username}' ya está en uso")
        
        # Verificar si el email ya existe
        if self.repository.get_user_by_email(email):
            raise ValueError(f"El email '{email}' ya está en uso")
        
        # Verificar rol válido
        valid_roles = ['customer', 'restaurant']
        if role not in valid_roles:
            raise ValueError(f"Rol no válido. Debe ser uno de: {', '.join(valid_roles)}")
        
        # Crear el usuario
        return self.repository.create_user(username, email, password, role)
    
    def authenticate_user(self, email, password):
        """
        Autentica un usuario con sus credenciales.
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña del usuario
            
        Returns:
            User: El usuario autenticado o None si las credenciales son incorrectas
        """
        # Buscar usuario por email
        user = self.repository.get_user_by_email(email)
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.check_password(password):
            # Actualizar último login
            self.repository.update_last_login(user.id)
            return user
            
        return None
    
    def change_password(self, user_id, current_password, new_password):
        """
        Cambia la contraseña de un usuario.
        
        Args:
            user_id (int): ID del usuario
            current_password (str): Contraseña actual
            new_password (str): Nueva contraseña
            
        Returns:
            bool: True si se cambió la contraseña, False en caso contrario
            
        Raises:
            ValueError: Si la contraseña actual es incorrecta o la nueva no cumple los requisitos
        """
        # Verificar que el usuario existe
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Verificar que la contraseña actual es correcta
        if not user.check_password(current_password):
            raise ValueError("La contraseña actual es incorrecta")
        
        # Verificar que la nueva contraseña cumple con los requisitos
        if len(new_password) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres")
        
        # Cambiar la contraseña
        return self.repository.change_password(user_id, new_password)
