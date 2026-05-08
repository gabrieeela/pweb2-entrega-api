from flask import Blueprint, jsonify, request
from ..data import PRODUCTS

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def get_products():
    """
    Listar todos los productos disponibles
    ---
    tags:
      - productos
    parameters:
      - name: gluten_free
        in: query
        type: boolean
        required: false
        description: Filtrar solo productos sin gluten
      - name: category
        in: query
        type: string
        required: false
        description: Filtrar por categoría (torta, pie, cheesecake)
    responses:
      200:
        description: Lista de productos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Cheesecake de Frutos Rojos
              description:
                type: string
              price:
                type: number
                example: 11800
              gluten_free:
                type: boolean
              category:
                type: string
                example: cheesecake
    """
    products = PRODUCTS

    gluten_free = request.args.get("gluten_free")
    if gluten_free is not None:
        is_gf = gluten_free.lower() == "true"
        products = [p for p in products if p["gluten_free"] == is_gf]

    category = request.args.get("category")
    if category:
        products = [p for p in products if p["category"] == category.lower()]

    return jsonify(products), 200


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Obtener un producto por ID
    ---
    tags:
      - productos
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID del producto
    responses:
      200:
        description: Producto encontrado
      404:
        description: Producto no encontrado
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": f"Producto con id {product_id} no encontrado"}), 404
    return jsonify(product), 200
