from pathlib import Path
import sqlite3

# ----------------------------------------
# Inicialización de base de datos / migración
# ----------------------------------------

# db_init: inicializa la base de datos, tablas y migraciones de archivo antiguo.
# Se usa `ensure_database` antes de abrir conexión en ItemModel.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT  # Guardar DB en la raíz del proyecto
DB_FILE = DB_DIR / "items.db"
OLD_DB_FILE = PROJECT_ROOT / "db" / "items.db"


def create_items_table(conn):
    # Crea la tabla items si no existe (esquema fijado aquí)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()


def ensure_database(db_path=None):
    # Asegura existencia de archivo DB, directorio y tablas necesarias
    if db_path is None:
        target_path = DB_FILE
    else:
        db_path = Path(db_path)
        if db_path.is_absolute():
            # si se pasa ruta absoluta, úsala tal cual
            target_path = db_path
        else:
            # ruta relativa siempre se mapea al root del proyecto
            target_path = PROJECT_ROOT / db_path.name

    target_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(target_path) as conn:
        create_items_table(conn)

    return str(target_path)
