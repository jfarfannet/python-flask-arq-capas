"""
Rutas para la gestión del menú.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.business.menu_service import MenuService

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')
menu_service = MenuService()

@menu_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    """Muestra el menú de un restaurante."""
    # Implementación básica
    return f"Menú del restaurante {restaurant_id}"

@menu_bp.route('/manage', methods=['GET'])
@login_required
def manage_menu():
    """Gestiona el menú del restaurante."""
    # Implementación básica
    return "Gestión del menú"