from app.tools import search_products, get_order_status

print(search_products.invoke({"query": "wireless headphones", "max_price": 50}))
print()
print(get_order_status.invoke({"order_id": "1025"}))
print()
print(get_order_status.invoke({"order_id": "9999"}))