from flask import Flask, jsonify, request
from flasgger import Swagger
from data import PRODUCTS
from cart import cart, get_cart_total

app = Flask(__name__)

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
    "info": {
        "title": "El Patio Vegan API",
        "description": "API REST para gestionar el carrito de compras de El Patio Vegan 🌱",
        "version": "1.0.0",
    },
    "basePath": "/",
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


# Lista de productos disponibles.
# Cada uno cuenta con un ID, nombre, descripción, precio, y si es apto para celíacos o no.
@app.route("/products", methods=["GET"])
def list_products():
    """
    Listar todos los productos disponibles.
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de tortas y postres disponibles.
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
    """
    return jsonify(PRODUCTS), 200

# Obtener un producto por ID:
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Obtener un producto por ID.
    ---
    tags:
      - Productos
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID del producto
    responses:
      200:
        description: Producto encontrado.
      404:
        description: Producto no encontrado.
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(product), 200


# Carrito de compras:
# Acá se va a poder ver el contenido del carrito, agregar o eliminar productos, y ver el total acumulado.
@app.route("/cart", methods=["GET"])
def get_cart():
    """
    Ver el contenido actual del carrito.
    ---
    tags:
      - Carrito
    responses:
      200:
        description: Contenido del carrito con total.
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                  name:
                    type: string
                  quantity:
                    type: integer
                  unit_price:
                    type: number
                  subtotal:
                    type: number
            total:
              type: number
              example: 23600
    """
    return jsonify({"items": cart, "total": get_cart_total()}), 200

# Agregar productos al carrito:
@app.route("/cart", methods=["POST"])
def add_to_cart():
    """
    Agregar un producto al carrito.
    ---
    tags:
      - Carrito
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - product_id
          properties:
            product_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 2
              default: 1
    responses:
      200:
        description: Producto agregado al carrito.
      400:
        description: Datos inválidos.
      404:
        description: Producto no encontrado.
    """
    body = request.get_json()
    if not body or "product_id" not in body:
        return jsonify({"error": "Se requiere product_id"}), 400

    product_id = body["product_id"]
    quantity = body.get("quantity", 1)

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "La cantidad debe ser un entero positivo"}), 400

    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    existing = next((item for item in cart if item["product_id"] == product_id), None)
    if existing:
        existing["quantity"] += quantity
        existing["subtotal"] = existing["quantity"] * existing["unit_price"]
    else:
        cart.append({
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "subtotal": quantity * product["price"],
        })

    return jsonify({"message": "Producto agregado", "cart": cart, "total": get_cart_total()}), 200

# Eliminar productos del carrito:
@app.route("/cart/<int:product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    """
    Eliminar un producto del carrito.
    ---
    tags:
      - Carrito
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
    responses:
      200:
        description: Producto eliminado del carrito.
      404:
        description: Producto no encontrado en el carrito.
    """
    item = next((i for i in cart if i["product_id"] == product_id), None)
    if not item:
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404

    cart.remove(item)
    return jsonify({"message": "Producto eliminado", "cart": cart, "total": get_cart_total()}), 200

# Ver el total de la compra:
@app.route("/cart/total", methods=["GET"])
def cart_total():
    """
    Obtener el total del carrito.
    ---
    tags:
      - Carrito
    responses:
      200:
        description: Total calculado del carrito.
        schema:
          type: object
          properties:
            item_count:
              type: integer
            total:
              type: number
    """
    item_count = sum(i["quantity"] for i in cart)
    return jsonify({"item_count": item_count, "total": get_cart_total()}), 200

# Vaciar todo el carrito:
@app.route("/cart", methods=["DELETE"])
def clear_cart():
    """
    Vaciar el carrito completo.
    ---
    tags:
      - Carrito
    responses:
      200:
        description: Carrito vaciado.
    """
    cart.clear()
    return jsonify({"message": "Carrito vaciado", "cart": [], "total": 0}), 200


if __name__ == "__main__":
    app.run(debug=True)
