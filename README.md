# El Patio Vegan API 🌿

API REST para gestionar el carrito de compras de **El Patio Vegan**, una cafetería vegana ubicada en la localidad de Ramos Mejía, Buenos Aires. 
Su especialización es la pastelería, ya que ofrecen opciones aptas para veganos y celíacos.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
python run.py
```

El servidor corre en `http://localhost:5000`

## Documentación (Swagger UI)

Una vez levantado el servidor, accedé a:

```
http://localhost:5000/docs/
```

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/products` | Listar todos los productos |
| GET | `/api/products?gluten_free=true` | Filtrar productos sin gluten |
| GET | `/api/products?category=pie` | Filtrar por categoría |
| GET | `/api/products/{id}` | Obtener un producto por ID |
| GET | `/api/cart` | Ver el carrito con totales |
| POST | `/api/cart` | Agregar producto al carrito |
| DELETE | `/api/cart/{product_id}` | Eliminar producto del carrito |
| DELETE | `/api/cart/{product_id}?quantity=N` | Reducir cantidad |
| DELETE | `/api/cart` | Vaciar el carrito |
| GET | `/api/cart/total` | Calcular total del carrito |

## Ejemplo de uso

```bash
# Listar productos
curl http://localhost:5000/api/products

# Agregar Cheesecake al carrito
curl -X POST http://localhost:5000/api/cart \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# Ver carrito
curl http://localhost:5000/api/cart

# Ver total
curl http://localhost:5000/api/cart/total

# Eliminar producto
curl -X DELETE http://localhost:5000/api/cart/1
```

## Tests

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
entrega/
├── app/
│   ├── __init__.py       # Factory de la app Flask + Swagger
│   ├── data.py           # Persistencia en memoria (productos y carrito)
│   └── routes/
│       ├── products.py   # Endpoints de productos
│       └── cart.py       # Endpoints del carrito
├── tests/
│   └── test_api.py       # Tests unitarios (pytest)
├── run.py                # Punto de entrada
├── requirements.txt
└── README.md
```
