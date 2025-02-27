"""
Rutas para la gestión de clientes.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.business.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')
customer_service = CustomerService()

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del cliente."""
    # Implementación básica
    return "Dashboard del cliente"

@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil del cliente."""
    # Implementación básica
    return "Perfil del cliente"