from src.models.item_model import ItemModel

# ----------------------------------------
# Controlador de negocio (MVC)
# ----------------------------------------

# ItemController: lógica de negocio entre la vista y el modelo.
# Encapsula operaciones CRUD y puede aplicar filtros/validaciones
# antes de delegar al ItemModel (acceso a base de datos).
class ItemController:
    def __init__(self, model: ItemModel):
        self.model = model

    def get_items(self):
        # Devuelve todos los items para la vista
        return self.model.read_all()

    def add_item(self, name, description):
        # Añade un nuevo item a través del modelo
        return self.model.create(name, description)

    def edit_item(self, item_id, name, description):
        # Edita item existente en la base
        self.model.update(item_id, name, description)

    def remove_item(self, item_id):
        self.model.delete(item_id)
