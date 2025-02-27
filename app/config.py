"""
Configuraciones para diferentes entornos de la aplicación.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Configuración base."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-muy-segura-por-defecto'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'presentation/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB (límite para uploads)
    BABEL_DEFAULT_LOCALE = 'es'
    
    @staticmethod
    def init_app(app):
        """Inicialización adicional de la aplicación."""
        # Crear directorio de uploads si no existe
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'food_delivery_dev.db')
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Habilitar barra de depuración en desarrollo
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)


class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'food_delivery_test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuración para producción."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'food_delivery.db')
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Configurar logging en producción
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler(
            'logs/food_delivery.log',
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicación de Food Delivery iniciada')


# Mapeo de nombres de configuración a clases
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}