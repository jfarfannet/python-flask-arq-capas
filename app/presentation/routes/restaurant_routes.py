"""
Rutas para la gestión de restaurantes.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.business.restaurant_service import RestaurantService

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')
restaurant_service = RestaurantService()

@restaurant_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del restaurante."""
    # Implementación básica
    return "Dashboard del restaurante"

@restaurant_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil del restaurante."""
    # Implementación básica
    return "Perfil del restaurante"