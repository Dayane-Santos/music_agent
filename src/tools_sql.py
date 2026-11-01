from langchain.tools import tool
from src.database import get_db_connection

# A conexão será injetada sob demanda
_db_conn = None

def set_connection(conn):
    global _db_conn
    _db_conn = conn

def get_conn():
    global _db_conn
    if _db_conn is None:
        _db_conn = get_db_connection()
    return _db_conn

@tool
def check_product(termo_busca: str) -> str:
    """Search products in the store catalog by name or category. Returns details like price and stock."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    product_table = next((t for t in tables if "product" in t.lower() or "produto" in t.lower() or "catalogo" in t.lower()), tables[0] if tables else "products")
    
    query = f"SELECT * FROM {product_table} WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?"
    param = f"%{termo_busca.lower()}%"
    
    try:
        cursor.execute(query, (param, param))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
    except Exception:
        cursor.execute(f"SELECT * FROM {product_table}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        rows = [r for r in rows if any(termo_busca.lower() in str(val).lower() for val in r)]

    if not rows:
        return f"No products found matching '{termo_busca}'."

    resultado = []
    for row in rows:
        item_str = ", ".join([f"{col}: {val}" for col, val in zip(columns, row)])
        resultado.append(item_str)
        
    return "\n".join(resultado[:10])

@tool
def check_product_status(pedido_id: str) -> str:
    """Check status and details for a specific order ID or customer name."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    order_table = next((t for t in tables if "order" in t.lower() or "pedido" in t.lower()), "orders")
    
    clean_id = "".join(filter(str.isdigit, str(pedido_id)))
    search_term = clean_id if clean_id else str(pedido_id).strip()

    query = f"SELECT * FROM {order_table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    matching_rows = [
        r for r in rows 
        if any(search_term == str(val).strip() for val in r)
    ]
    
    if not matching_rows:
        available_ids = [str(r[0]) for r in rows[:5]]
        return f"Order '{pedido_id}' was not found. Available sample order IDs in database: {', '.join(available_ids)}"
        
    resultado = []
    for row in matching_rows:
        resultado.append(", ".join([f"{col}: {val}" for col, val in zip(columns, row)]))
        
    return "\n".join(resultado)