# El Patio Vegan API 🌿

API REST para gestionar el carrito de compras de **El Patio Vegan**, una cafetería vegana ubicada en la localidad de Ramos Mejía, Buenos Aires. 
Su especialización es la pastelería, ya que ofrecen opciones aptas para veganos y celíacos.


## Arquitectura elegida
 
Se adoptó una arquitectura **cliente-servidor en capas**, organizando el backend en tres niveles bien diferenciados:
 
- **Capa de presentación (rutas):** los Blueprints de Flask (`products.py` y `cart.py`) reciben las solicitudes HTTP, validan los datos de entrada y devuelven las respuestas JSON correspondientes.
- **Capa de datos:** el módulo `data.py` centraliza la persistencia en memoria, exponiendo las estructuras `PRODUCTS` (catálogo de productos que contienen su nombre, descripción, precio, id, y si es o no libre de gluten) y `cart` (carrito de compras activo).
- **Capa de aplicación:** `app/__init__.py` implementa el patrón **Application Factory**, que instancia Flask, registra los Blueprints y configura Swagger en un único punto de entrada controlado.

### Endpoints disponibles
 
| Método   | URL                          | Descripción                                 |
|----------|------------------------------|---------------------------------------------|
| GET      | `/api/products`              | Listar todos los productos                  |
| GET      | `/api/products?gluten_free=true` | Filtrar productos sin TACC              |
| GET      | `/api/products?category=pie` | Filtrar por categoría                       |
| GET      | `/api/products/{id}`         | Obtener un producto por ID                  |
| GET      | `/api/cart`                  | Ver el carrito con subtotales y total       |
| POST     | `/api/cart`                  | Agregar un producto al carrito              |
| DELETE   | `/api/cart/{product_id}`     | Eliminar un producto (o reducir cantidad)   |
| DELETE   | `/api/cart`                  | Vaciar el carrito completo                  |
| GET      | `/api/cart/total`            | Calcular el total con desglose              |
 
---
 

## Tecnologías utilizadas
 
| Tecnología | Versión | Rol |
|---|---|---|
| **Python** | 3.10+ | Lenguaje principal |
| **Flask** | 3.x | Framework web para construir la API REST |
| **Flasgger** | 0.9.x | Generación automática de documentación Swagger/OpenAPI |
| **pytest** | 8.x | Framework de testing unitario |
 
Se eligió Flask sobre alternativas como FastAPI o Django REST Framework por su **simplicidad y bajo nivel de abstracción**, permitiendo entender el flujo de una solicitud HTTP sin capas de magia implícita. En cuanto al alcance del proyecto resulta la opción más directa y apropiada.
 
---
 

## Dificultades encontradas y cómo se resolvieron
 
### 1. Estado compartido entre módulos en Python
 
**Problema:** al importar `cart` directamente con `from .data import cart`, cada módulo obtenía una **copia local** de la lista. Las modificaciones en un módulo no se reflejaban en los demás, y los tests no podían limpiar el estado correctamente entre ejecuciones.
 
**Solución:** importar el módulo completo (`from .. import data`) y referenciar siempre `data.cart`. De esta forma, todos los módulos apuntan a la misma referencia en memoria y los cambios se propagan correctamente.
 
---
 
### 2. Tests que se afectaban entre sí
 
**Problema:** al correr la suite completa de tests, algunos fallaban dependiendo del orden de ejecución porque el carrito conservaba ítems de tests anteriores.
 
**Solución:** agregar `data.cart.clear()` dentro del fixture `client` de pytest, que se ejecuta antes de cada test individual. Esto garantiza que cada test parte de un carrito vacío, sin importar qué haya ocurrido antes.
 
```python
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        data.cart.clear()  
        yield client
```

---
 
 
## Cómo ejecutar el proyecto
 
### Instalación
 
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```
 
### Levantar el servidor
 
```bash
python run.py
```
 
El servidor corre en `http://localhost:5000`  
La documentación Swagger está disponible en `http://localhost:5000/docs/`
 
### Correr los tests
 
```bash
pytest tests/ -v
```
---
 