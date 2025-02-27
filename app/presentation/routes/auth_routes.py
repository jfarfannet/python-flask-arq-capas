"""
Rutas para la autenticación de usuarios.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.business.auth_service import AuthService
from app.utils.validators import validate_registration_data, validate_login_data

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registra un nuevo usuario."""
    # Implementación básica
    return "Formulario de registro"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicia sesión de usuario."""
    # Implementación básica
    return "Formulario de login"

@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario."""
    # Implementación básica
    return "Cerrar sesión"