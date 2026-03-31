import sqlite3
from db.db_init import ensure_database, create_items_table
from db.crud_items import create_item, read_all_items, update_item, delete_item

# ----------------------------------------
# Modelo / Persistencia SQLite
# ----------------------------------------

# ItemModel gestionando interacción con la base de datos
class ItemModel:
    def __init__(self, db_path="items.db"):
        # Inicializa ruta de base de datos y se asegura de la creación de tablas
        self.db_path = ensure_database(db_path)

    def _get_connection(self):
        # Abre conexión SQLite (llevará commit en funciones externas)
        return sqlite3.connect(self.db_path)

    def create(self, name, description):
        # Inserta nuevo item en la base de datos
        with self._get_connection() as conn:
            return create_item(conn, name, description)

    def read_all(self):
        with self._get_connection() as conn:
            return read_all_items(conn)

    def update(self, item_id, name, description):
        with self._get_connection() as conn:
            update_item(conn, item_id, name, description)

    def delete(self, item_id):
        with self._get_connection() as conn:
            delete_item(conn, item_id)

