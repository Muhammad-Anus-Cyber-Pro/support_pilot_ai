from langchain.tools import tool
from app.data import PRODUCTS, ORDERS

@tool
def search_products(query: str, max_price: float = None) -> str:
    """
    Searches the product catalog by keyword, optionally filtered by max price.
    Use this when a customer asks about products, availability, or pricing
    (e.g., "do you have wireless headphones under $50?").
    """
    query_lower = query.lower()
    matches = []

    for product in PRODUCTS:
        text = f"{product['name']} {product['description']}".lower()
        if any(word in text for word in query_lower.split()):
            if max_price is None or product["price"] <= max_price:
                matches.append(product)

    if not matches:
        return "No matching products found."

    result_lines = [
        f"- {p['name']} (${p['price']}): {p['description']}" for p in matches
    ]
    return "\n".join(result_lines)

@tool
def get_order_status(order_id: str) -> str:
    """
    Looks up the status of an order by its order ID.
    Use this when a customer asks about order status, shipping, or delivery
    (e.g., "where is my order #1025?").
    """
    order = ORDERS.get(order_id.strip())

    if not order:
        return f"No order found with ID {order_id}. Please double-check the order number."

    return (
        f"Order {order_id}: status is '{order['status']}', "
        f"customer: {order['customer']}, expected: {order['expected']}."
    )