"""
Rutas para la gestión de reseñas.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.business.review_service import ReviewService

review_bp = Blueprint('reviews', __name__, url_prefix='/reviews')
review_service = ReviewService()

@review_bp.route('/add/<int:order_id>', methods=['GET', 'POST'])
@login_required
def add_review(order_id):
    """Añade una reseña a un pedido."""
    # Implementación básica
    return f"Añadir reseña al pedido {order_id}"

@review_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_reviews(restaurant_id):
    """Muestra las reseñas de un restaurante."""
    # Implementación básica
    return f"Reseñas del restaurante {restaurant_id}"