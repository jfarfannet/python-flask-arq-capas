import os

# Directorios a crear
directories = [
    'app/presentation/templates/errors',
    'app/presentation/templates/auth',
    'app/presentation/templates/customer',
    'app/presentation/templates/restaurant',
    'app/presentation/templates/menu',
    'app/presentation/templates/orders',
    'app/presentation/templates/cart',
    'app/presentation/static/css',
    'app/presentation/static/js',
    'app/presentation/static/images',
    'app/presentation/static/uploads'
]

# Crear directorios si no existen
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Creado directorio: {directory}")

# Archivos para crear
files = {
    'app/presentation/templates/errors/404.html': '{% extends "layout.html" %}\n\n{% block title %}Página no encontrada (404) - Food Delivery App{% endblock %}\n\n{% block content %}\n<div class="text-center py-5">\n    <h1 class="display-1 text-muted">404</h1>\n    <h2 class="mb-4">Página no encontrada</h2>\n    <p class="lead mb-5">Lo sentimos, la página que estás buscando no existe o ha sido movida.</p>\n    <a href="/" class="btn btn-primary">\n        <i class="fas fa-home"></i> Volver al Inicio\n    </a>\n</div>\n{% endblock %}',
    'app/presentation/templates/errors/403.html': '{% extends "layout.html" %}\n\n{% block title %}Acceso Prohibido (403) - Food Delivery App{% endblock %}\n\n{% block content %}\n<div class="text-center py-5">\n    <h1 class="display-1 text-muted">403</h1>\n    <h2 class="mb-4">Acceso Prohibido</h2>\n    <p class="lead mb-5">No tienes permisos para acceder a esta página.</p>\n    <a href="/" class="btn btn-primary">\n        <i class="fas fa-home"></i> Volver al Inicio\n    </a>\n</div>\n{% endblock %}',
    'app/presentation/templates/errors/500.html': '{% extends "layout.html" %}\n\n{% block title %}Error del Servidor (500) - Food Delivery App{% endblock %}\n\n{% block content %}\n<div class="text-center py-5">\n    <h1 class="display-1 text-muted">500</h1>\n    <h2 class="mb-4">Error Interno del Servidor</h2>\n    <p class="lead mb-5">Lo sentimos, ha ocurrido un error en nuestro servidor. Por favor, inténtalo de nuevo más tarde.</p>\n    <a href="/" class="btn btn-primary">\n        <i class="fas fa-home"></i> Volver al Inicio\n    </a>\n</div>\n{% endblock %}'
}

# Crear archivos si no existen
for file_path, content in files.items():
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Creado archivo: {file_path}")
    else:
        print(f"El archivo ya existe: {file_path}")

print("Estructura de directorios y archivos creada correctamente.")