from langchain.tools import tool
from src.database import get_db_connection

conn = get_db_connection()

@tool
def check_product(search_term: str) -> str:
    """ Search for products in the store catalog by name, brand, or category. Returns price and available stock. """
    cursor = conn.cursor()
    query = """
        SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE name LIKE ? OR c.name LIKE ?
    """
    param = f"%{search_term}%"
    cursor.execute(query, (param, param))
    rows = cursor.fetchall()

    if not rows:
        return "No products found matching your search."

    result = []
    for row in rows:
        result.append(f"ID: {row[0]}, Name: {row[1]}, Price: ${row[2]:.2f}, Stock: {row[3]}, Category: {row[4]}")
    return "\n".join(result)

    @tool
    def check_order_status(order_id: str) -> str:
        """ Check the status of an order by its ID. Returns the current status and estimated delivery date. """
        cursor = conn.cursor()
        query = """
            SELECT o.id, o.order_date, o.status, o.total_amount, c.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        """
        cursor.execute(query, (order_id,))
        row = cursor.fetchone()

        if not row:
            return f"Order with ID {order_id} not found."

       return f"Order #{row[0]} | Client: {row[4]} | Date: {row[1]} | Status: {row[2]} | Total: ${row[3]:.2f}"