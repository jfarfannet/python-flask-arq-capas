"""
Excepciones personalizadas para la aplicación.
"""

class AppError(Exception):
    """Excepción base para la aplicación."""
    pass


class OrderNotFoundError(AppError):
    """Excepción cuando no se encuentra un pedido."""
    pass


class InvalidOrderStateError(AppError):
    """Excepción cuando se intenta una transición de estado inválida."""
    pass


class ReviewError(AppError):
    """Excepción para errores relacionados con reseñas."""
    pass


class CartError(AppError):
    """Excepción para errores relacionados con el carrito."""
    pass