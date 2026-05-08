import pytest
from app import create_app
from app import data


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        data.cart.clear()
        yield client

# Tests para la API de productos
class TestProducts:
    def test_get_all_products_returns_200(self, client):
        res = client.get("/api/products")
        assert res.status_code == 200

    def test_get_all_products_returns_list(self, client):
        res = client.get("/api/products")
        body = res.get_json()
        assert isinstance(body, list)
        assert len(body) == 9

    def test_products_have_required_fields(self, client):
        res = client.get("/api/products")
        for product in res.get_json():
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "gluten_free" in product
            assert "category" in product

    def test_filter_by_gluten_free(self, client):
        res = client.get("/api/products?gluten_free=true")
        products = res.get_json()
        assert all(p["gluten_free"] for p in products)
        assert len(products) == 2

    def test_filter_by_category(self, client):
        res = client.get("/api/products?category=pie")
        products = res.get_json()
        assert all(p["category"] == "pie" for p in products)
        assert len(products) == 3

    def test_get_product_by_id(self, client):
        res = client.get("/api/products/1")
        assert res.status_code == 200
        body = res.get_json()
        assert body["id"] == 1
        assert body["name"] == "Cheesecake de Frutos Rojos"

    def test_get_product_not_found(self, client):
        res = client.get("/api/products/999")
        assert res.status_code == 404

    def test_product_price_is_correct(self, client):
        res = client.get("/api/products/1")
        body = res.get_json()
        assert body["price"] == 11800

# Tests para el carrito de compras
class TestCart:
    def test_empty_cart_returns_200(self, client):
        res = client.get("/api/cart")
        assert res.status_code == 200

    def test_empty_cart_has_zero_total(self, client):
        res = client.get("/api/cart")
        body = res.get_json()
        assert body["total"] == 0
        assert body["item_count"] == 0
        assert body["items"] == []

    def test_add_product_to_cart(self, client):
        res = client.post("/api/cart", json={"product_id": 1})
        assert res.status_code == 201

    def test_add_product_increases_item_count(self, client):
        client.post("/api/cart", json={"product_id": 1})
        res = client.get("/api/cart")
        body = res.get_json()
        assert body["item_count"] == 1

    def test_add_same_product_twice_updates_quantity(self, client):
        client.post("/api/cart", json={"product_id": 1})
        res = client.post("/api/cart", json={"product_id": 1})
        assert res.status_code == 200
        cart_res = client.get("/api/cart")
        body = cart_res.get_json()
        assert body["item_count"] == 2

    def test_add_product_with_quantity(self, client):
        client.post("/api/cart", json={"product_id": 2, "quantity": 3})
        res = client.get("/api/cart")
        body = res.get_json()
        assert body["item_count"] == 3

    def test_add_nonexistent_product(self, client):
        res = client.post("/api/cart", json={"product_id": 999})
        assert res.status_code == 404

    def test_add_without_product_id(self, client):
        res = client.post("/api/cart", json={})
        assert res.status_code == 400

    def test_add_invalid_quantity(self, client):
        res = client.post("/api/cart", json={"product_id": 1, "quantity": 0})
        assert res.status_code == 400

    def test_remove_product_from_cart(self, client):
        client.post("/api/cart", json={"product_id": 1})
        res = client.delete("/api/cart/1")
        assert res.status_code == 200
        cart_res = client.get("/api/cart")
        assert cart_res.get_json()["item_count"] == 0

    def test_remove_nonexistent_cart_item(self, client):
        res = client.delete("/api/cart/1")
        assert res.status_code == 404

    def test_remove_partial_quantity(self, client):
        client.post("/api/cart", json={"product_id": 1, "quantity": 3})
        client.delete("/api/cart/1?quantity=2")
        res = client.get("/api/cart")
        body = res.get_json()
        assert body["item_count"] == 1

    def test_clear_cart(self, client):
        client.post("/api/cart", json={"product_id": 1})
        client.post("/api/cart", json={"product_id": 2})
        res = client.delete("/api/cart")
        assert res.status_code == 200
        cart_res = client.get("/api/cart")
        assert cart_res.get_json()["item_count"] == 0

# Tests para ver el total de la compra
class TestTotal:
    def test_total_empty_cart(self, client):
        res = client.get("/api/cart/total")
        body = res.get_json()
        assert body["total"] == 0

    def test_total_with_one_item(self, client):
        client.post("/api/cart", json={"product_id": 1, "quantity": 1})
        res = client.get("/api/cart/total")
        body = res.get_json()
        assert body["total"] == 11800

    def test_total_with_multiple_items(self, client):
        client.post("/api/cart", json={"product_id": 1, "quantity": 2})
        client.post("/api/cart", json={"product_id": 2, "quantity": 1})
        res = client.get("/api/cart/total")
        body = res.get_json()
        assert body["total"] == 11800 * 3

    def test_total_breakdown_contains_items(self, client):
        client.post("/api/cart", json={"product_id": 1})
        res = client.get("/api/cart/total")
        body = res.get_json()
        assert len(body["breakdown"]) == 1
        assert body["breakdown"][0]["name"] == "Cheesecake de Frutos Rojos"
