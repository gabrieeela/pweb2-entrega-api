from flask import Blueprint, jsonify, request
from .. import data
from ..data import PRODUCTS

cart_bp = Blueprint("cart", __name__)


def find_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def find_cart_item(product_id):
    return next((item for item in data.cart if item["product_id"] == product_id), None)


@cart_bp.route("/cart", methods=["GET"])
def get_cart():
    """
    Ver el contenido del carrito
    ---
    tags:
      - carrito
    responses:
      200:
        description: Contenido actual del carrito con detalle de cada ítem
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
              example: 35400
            item_count:
              type: integer
              example: 3
    """
    enriched = []
    total = 0

    for item in data.cart:
        product = find_product(item["product_id"])
        subtotal = product["price"] * item["quantity"]
        total += subtotal
        enriched.append({
            "product_id": item["product_id"],
            "name": product["name"],
            "quantity": item["quantity"],
            "unit_price": product["price"],
            "subtotal": subtotal,
        })

    return jsonify({
        "items": enriched,
        "total": total,
        "item_count": sum(i["quantity"] for i in data.cart),
    }), 200


@cart_bp.route("/cart", methods=["POST"])
def add_to_cart():
    """
    Agregar un producto al carrito
    ---
    tags:
      - carrito
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
              description: Cantidad a agregar (por defecto 1)
    responses:
      200:
        description: Producto ya estaba en el carrito, cantidad actualizada
      201:
        description: Producto agregado al carrito exitosamente
      400:
        description: Datos inválidos
      404:
        description: Producto no encontrado
    """
    body = request.get_json()
    if not body or "product_id" not in body:
        return jsonify({"error": "Se requiere product_id en el cuerpo de la petición"}), 400

    product_id = body["product_id"]
    quantity = body.get("quantity", 1)

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "La cantidad debe ser un entero mayor a 0"}), 400

    product = find_product(product_id)
    if not product:
        return jsonify({"error": f"Producto con id {product_id} no encontrado"}), 404

    existing = find_cart_item(product_id)
    if existing:
        existing["quantity"] += quantity
        return jsonify({
            "message": f"Cantidad actualizada para '{product['name']}'",
            "product_id": product_id,
            "quantity": existing["quantity"],
        }), 200

    data.cart.append({"product_id": product_id, "quantity": quantity})
    return jsonify({
        "message": f"'{product['name']}' agregado al carrito",
        "product_id": product_id,
        "quantity": quantity,
    }), 201


@cart_bp.route("/cart/<int:product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    """
    Eliminar un producto del carrito
    ---
    tags:
      - carrito
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
      - name: quantity
        in: query
        type: integer
        required: false
        description: Cantidad a eliminar. Si no se indica, se elimina el ítem completo.
    responses:
      200:
        description: Producto eliminado o cantidad reducida
      404:
        description: Producto no encontrado en el carrito
    """
    item = find_cart_item(product_id)
    if not item:
        return jsonify({"error": f"Producto con id {product_id} no está en el carrito"}), 404

    quantity = request.args.get("quantity", type=int)
    product = find_product(product_id)

    if quantity and quantity < item["quantity"]:
        item["quantity"] -= quantity
        return jsonify({
            "message": f"Cantidad reducida para '{product['name']}'",
            "product_id": product_id,
            "quantity": item["quantity"],
        }), 200

    data.cart.remove(item)
    return jsonify({
        "message": f"'{product['name']}' eliminado del carrito",
        "product_id": product_id,
    }), 200


@cart_bp.route("/cart", methods=["DELETE"])
def clear_cart():
    """
    Vaciar el carrito completo
    ---
    tags:
      - carrito
    responses:
      200:
        description: Carrito vaciado exitosamente
    """
    data.cart.clear()
    return jsonify({"message": "Carrito vaciado exitosamente"}), 200


@cart_bp.route("/cart/total", methods=["GET"])
def get_total():
    """
    Calcular el total del carrito
    ---
    tags:
      - carrito
    responses:
      200:
        description: Total calculado
        schema:
          type: object
          properties:
            total:
              type: number
              example: 35400
            item_count:
              type: integer
              example: 3
            breakdown:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  quantity:
                    type: integer
                  subtotal:
                    type: number
    """
    breakdown = []
    total = 0

    for item in data.cart:
        product = find_product(item["product_id"])
        subtotal = product["price"] * item["quantity"]
        total += subtotal
        breakdown.append({
            "name": product["name"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

    return jsonify({
        "total": total,
        "item_count": sum(i["quantity"] for i in data.cart),
        "breakdown": breakdown,
    }), 200
