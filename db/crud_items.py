# ----------------------------------------
# Funciones CRUD SQL directas
# ----------------------------------------

def create_item(conn, name, description):
    # Inserta item en tabla items
    cursor = conn.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (name, description)
    )
    conn.commit()
    return cursor.lastrowid


def read_all_items(conn):
    # Lee todos los items ordenados por id DESC para mostrar recientes primero
    cursor = conn.execute(
        "SELECT id, name, description FROM items ORDER BY id DESC"
    )
    return cursor.fetchall()


def update_item(conn, item_id, name, description):
    # Actualiza un registro de item
    conn.execute(
        "UPDATE items SET name = ?, description = ? WHERE id = ?",
        (name, description, item_id)
    )
    conn.commit()


def delete_item(conn, item_id):
    # Elimina ítem por id
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
