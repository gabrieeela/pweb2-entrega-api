# Persistencia en memoria

PRODUCTS = [
    {
        "id": 1,
        "name": "Cheesecake de Frutos Rojos",
        "description": "Masa sablée, crema a base de tofu y queso crema cubierto de mermelada casera de frutos rojos.",
        "price": 11800,
        "gluten_free": False,
        "category": "cheesecake",
    },
    {
        "id": 2,
        "name": "Torta de Maracuyá",
        "description": "Base realizada en frutas secas, mousse de maracuyá. Decorada con mermelada casera de maracuyá, copos de crema y praline de nueces.",
        "price": 11800,
        "gluten_free": True,
        "category": "torta",
    },
    {
        "id": 3,
        "name": "Dulce Pistacho",
        "description": "Base de frutas secas, crema de yogurt de soja, queso crema de castañas y ralladura de limón. Segunda capa con pasta de pistachos y fideos kataifi. Cubierta con ganache de chocolate amargo.",
        "price": 11800,
        "gluten_free": True,
        "category": "torta",
    },
    {
        "id": 4,
        "name": "Lemon Pie",
        "description": "Masa sablée rellena de crema pastelera de limón decorada con copos de crema.",
        "price": 11800,
        "gluten_free": False,
        "category": "pie",
    },
    {
        "id": 5,
        "name": "Orange Pie",
        "description": "Masa sablée rellena de crema pastelera de naranja decorada con copos de crema.",
        "price": 11800,
        "gluten_free": False,
        "category": "pie",
    },
    {
        "id": 6,
        "name": "Torta Oreo",
        "description": "Bizcochos de chocolate rellenos de mousse de chocolate y crema con galletitas Oreo. Superficie cubierta por una ganache de chocolate semi amargo.",
        "price": 11800,
        "gluten_free": False,
        "category": "torta",
    },
    {
        "id": 7,
        "name": "Torta Matilda",
        "description": "Bizcochos de chocolate rellenos de mousse de chocolate. Superficie cubierta por una ganache de chocolate semi amargo.",
        "price": 11800,
        "gluten_free": False,
        "category": "torta",
    },
    {
        "id": 8,
        "name": "Torta Brownie",
        "description": "Brownie de chocolate semi amargo con copos de dulce de leche de almendras y corazón de frutos rojos. Superficie decorada con crema.",
        "price": 11800,
        "gluten_free": False,
        "category": "torta",
    },
    {
        "id": 9,
        "name": "Key Lime",
        "description": "Base realizada en frutos secos, crema de limas decorada con crema chantilly y limas en mitades.",
        "price": 11800,
        "gluten_free": False,
        "category": "pie",
    },
]

# Carrito: lista de { product_id, quantity }
cart = []
