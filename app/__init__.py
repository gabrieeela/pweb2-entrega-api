from flask import Flask
from flasgger import Swagger
from .routes.products import products_bp
from .routes.cart import cart_bp

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "El Patio Vegan API",
        "description": "API REST para gestionar el carrito de compras de El Patio Vegan 🌿",
        "version": "1.0.0",
        "contact": {
            "name": "El Patio Vegan"
        }
    },
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {"name": "productos", "description": "Listado de tortas y postres disponibles"},
        {"name": "carrito", "description": "Gestión del carrito de compras"},
    ]
}


def create_app():
    app = Flask(__name__)
    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")

    return app
