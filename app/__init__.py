"""
Inicialización del paquete principal de la aplicación.
Este archivo crea y configura la aplicación Flask.
"""

import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from datetime import datetime

from app.config import config_dict
from app.persistence.database import db
from app.utils.helpers import get_status_label, get_status_color, get_payment_method_label


def create_app(config_name=None):
    """
    Crea y configura la aplicación Flask.
    
    Args:
        config_name (str, optional): Nombre de la configuración a utilizar.
            Puede ser 'development', 'production', 'testing' o 'default'.
            Si no se especifica, se tomará de la variable de entorno FLASK_CONFIG.

    Returns:
        Flask: Aplicación configurada
    """
    if not config_name:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__, 
                template_folder='presentation/templates',
                static_folder='presentation/static')
    
    # Aplicar configuración
    app.config.from_object(config_dict[config_name])
    config_dict[config_name].init_app(app)

    # Inicializar extensiones
    db.init_app(app)
    
    migrate = Migrate()
    migrate.init_app(app, db)
    
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    babel = Babel()
    babel.init_app(app)
    
    # Configurar login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    # Importar blueprints aquí para evitar importaciones circulares
    from app.presentation.routes.auth_routes import auth_bp
    from app.presentation.routes.customer_routes import customer_bp
    from app.presentation.routes.restaurant_routes import restaurant_bp
    from app.presentation.routes.menu_routes import menu_bp
    from app.presentation.routes.order_routes import order_bp
    from app.presentation.routes.cart_routes import cart_bp
    from app.presentation.routes.review_routes import review_bp
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(review_bp)

    # Importar modelos aquí para evitar importaciones circulares
    from app.persistence.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """Carga un usuario desde la base de datos."""
        return User.query.get(int(user_id))

    # Página principal
    @app.route('/')
    def index():
        """Página de inicio."""
        from app.business.restaurant_service import RestaurantService
        
        restaurant_service = RestaurantService()
        popular_restaurants = restaurant_service.get_popular_restaurants(limit=6)
        
        cuisines = [
            {'name': 'Italiana', 'icon': 'fas fa-pizza-slice'},
            {'name': 'Mexicana', 'icon': 'fas fa-pepper-hot'},
            {'name': 'China', 'icon': 'fas fa-utensils'},
            {'name': 'Hamburguesas', 'icon': 'fas fa-hamburger'},
            {'name': 'Vegetariana', 'icon': 'fas fa-seedling'},
            {'name': 'Postres', 'icon': 'fas fa-ice-cream'},
            {'name': 'Sushi', 'icon': 'fas fa-fish'},
            {'name': 'Pollo', 'icon': 'fas fa-drumstick-bite'}
        ]
        
        return render_template('index.html', 
                              popular_restaurants=popular_restaurants, 
                              cuisines=cuisines)

    # Listar restaurantes
    @app.route('/restaurantes')
    def restaurants():
        """Página de listado de restaurantes."""
        from app.business.restaurant_service import RestaurantService
        from flask import request
        from flask_login import current_user
        from app.business.customer_service import CustomerService
        
        restaurant_service = RestaurantService()
        
        page = request.args.get('page', 1, type=int)
        query = request.args.get('q', '')
        cuisine = request.args.get('cuisine', '')
        
        if query or cuisine:
            restaurants = restaurant_service.search_restaurants(
                query=query, 
                cuisine_type=cuisine, 
                page=page
            )
        else:
            restaurants = restaurant_service.get_all_restaurants(page=page)
        
        # Obtener los IDs de restaurantes favoritos para el cliente actual
        favorite_restaurant_ids = []
        if current_user.is_authenticated and current_user.role == 'customer':
            customer_service = CustomerService()
            favorites = customer_service.get_favorite_restaurants(current_user.customer.id)
            favorite_restaurant_ids = [r.id for r in favorites]
        
        return render_template('restaurants.html', 
                              restaurants=restaurants,
                              query=query,
                              cuisine=cuisine,
                              favorite_restaurant_ids=favorite_restaurant_ids)

    # Contexto global para templates
    @app.context_processor
    def inject_globals():
        """Inyecta variables globales en los templates."""
        return {
            'now': datetime.utcnow(),
            'status_labels': {
                'pending': 'Pendiente',
                'preparing': 'Preparando',
                'ready': 'Listo para entrega',
                'delivering': 'En camino',
                'delivered': 'Entregado',
                'cancelled': 'Cancelado'
            },
            'status_colors': {
                'pending': 'warning',
                'preparing': 'info',
                'ready': 'primary',
                'delivering': 'secondary',
                'delivered': 'success',
                'cancelled': 'danger'
            },
            'payment_methods': {
                'cash': 'Efectivo',
                'card': 'Tarjeta al entregar',
                'online': 'Pago en línea'
            },
            'get_status_label': get_status_label,
            'get_status_color': get_status_color,
            'get_payment_method_label': get_payment_method_label
        }

    # Manejadores de errores
    @app.errorhandler(404)
    def page_not_found(e):
        """Maneja errores 404."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """Maneja errores 500."""
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        """Maneja errores 403."""
        return render_template('errors/403.html'), 403

    # Crear tablas si no existen (solo para desarrollo)
    with app.app_context():
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            db.create_all()

    return app