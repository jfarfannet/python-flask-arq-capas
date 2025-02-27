"""
Rutas para la gestión de pedidos.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.business.order_service import OrderService
from app.utils.exceptions import OrderNotFoundError, InvalidOrderStateError

order_bp = Blueprint('orders', __name__, url_prefix='/orders')
order_service = OrderService()

@order_bp.route('/')
@login_required
def list_orders():
    """Lista los pedidos del usuario actual."""
    # Implementación básica
    return "Lista de pedidos"

@order_bp.route('/<int:order_id>')
@login_required
def order_details(order_id):
    """Muestra los detalles de un pedido."""
    # Implementación básica
    return f"Detalles del pedido {order_id}"