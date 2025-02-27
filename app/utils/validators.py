"""
Validadores para datos de entrada.
"""

def validate_registration_data(data):
    """
    Valida los datos de registro.
    
    Args:
        data (dict): Datos del formulario de registro
        
    Returns:
        list: Lista de errores encontrados (vacía si no hay errores)
    """
    errors = []
    
    # Validar username
    if not data.get('username'):
        errors.append('El nombre de usuario es obligatorio')
    elif len(data.get('username', '')) < 3:
        errors.append('El nombre de usuario debe tener al menos 3 caracteres')
    
    # Validar email
    if not data.get('email'):
        errors.append('El email es obligatorio')
    
    # Validar contraseña
    if not data.get('password'):
        errors.append('La contraseña es obligatoria')
    elif len(data.get('password', '')) < 8:
        errors.append('La contraseña debe tener al menos 8 caracteres')
    
    # Validar confirmación de contraseña
    if data.get('password') != data.get('confirm_password'):
        errors.append('Las contraseñas no coinciden')
    
    # Validar rol
    if not data.get('role'):
        errors.append('El rol es obligatorio')
    elif data.get('role') not in ['customer', 'restaurant']:
        errors.append('El rol no es válido')
    
    return errors


def validate_login_data(data):
    """
    Valida los datos de inicio de sesión.
    
    Args:
        data (dict): Datos del formulario de login
        
    Returns:
        list: Lista de errores encontrados (vacía si no hay errores)
    """
    errors = []
    
    # Validar email
    if not data.get('email'):
        errors.append('El email es obligatorio')
    
    # Validar contraseña
    if not data.get('password'):
        errors.append('La contraseña es obligatoria')
    
    return errors