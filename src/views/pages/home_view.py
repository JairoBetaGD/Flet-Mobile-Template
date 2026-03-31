import flet as ft
from src.models.item_model import ItemModel
from src.controllers.item_controller import ItemController
from src.views.components.image_picker_service import ImagePickerService
from src.views.components.bottom_nav import BottomNav
from src.views.components.overlay_base import OverlayBase


class HomeView:
    # ----------------------------------------
    # Clase de vista principal (UI + eventos)
    # ----------------------------------------

    def __init__(self, page: ft.Page):
        # ----------------------------------------
        # Inicialización de la vista principal
        # ----------------------------------------
        self.page = page
        self.page.navigation_bar = BottomNav(self.page).build()

        # ----------------------------------------
        # BD (Modelo y Controlador) - MVC
        # ----------------------------------------
        self.item_model = ItemModel("items.db")
        self.item_controller = ItemController(self.item_model)

        # ID seleccionado para edición (None = crear nuevo)
        self.selected_id = None

        # ----------------------------------------
        # Overlays / Filepicker / UI global
        # ----------------------------------------
        self.overlay_info = OverlayBase(page, None)
        self.overlay_image = OverlayBase(page, None)

        # Asignar contenido inicial de overlays
        self.overlay_info.container.content = self.build_info_overlay(self.overlay_info.hide)
        self.overlay_image.container.content = self.build_image_overlay(self.overlay_image.hide)

        # Servicio de elegir imagen y vista previa
        self.image_service = ImagePickerService(page)
        self.img_preview = ft.Image(src="", width=300, height=300, fit="contain", visible=False)

    # ----------------------------------------
    # CRUD - Tabla y datos
    # ----------------------------------------
    def _refresh_table(self, data_table, field_name, field_description):
        # Actualiza el contenido de la tabla con los datos actuales de la base
        items = self.item_controller.get_items()
        rows = []
        for item_id, name, description in items:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(item_id))),
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(description or "")),
                        ft.DataCell(
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.Icons.EDIT,
                                        tooltip="Editar",
                                        on_click=lambda e, i=item_id, n=name, d=description: self._start_edit(i, n, d, field_name, field_description)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.Icons.DELETE,
                                        tooltip="Eliminar",
                                        on_click=lambda e, i=item_id: self._delete_item(i, data_table, field_name, field_description)
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        data_table.rows = rows
        self.page.update()

    def _clear_form(self, field_name, field_description):
        # Limpia los campos del formulario y restablece el modo de edición
        field_name.value = ""
        field_description.value = ""
        self.selected_id = None

    def _save_item(self, e, field_name, field_description, data_table):
        # Maneja el evento Guardar del formulario (crear o actualizar item)
        name = (field_name.value or "").strip()
        description = (field_description.value or "").strip()

        if not name:
            self.page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.selected_id:
            self.item_controller.edit_item(self.selected_id, name, description)
            mensaje = "Item actualizado"
        else:
            self.item_controller.add_item(name, description)
            mensaje = "Item agregado"

        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True

        self._clear_form(field_name, field_description)
        self._refresh_table(data_table, field_name, field_description)

    def _start_edit(self, item_id, name, description, field_name, field_description):
        # Pone el formulario en modo edición cargando un registro existente
        self.selected_id = item_id
        field_name.value = name
        field_description.value = description
        self.page.update()

    def _delete_item(self, item_id, data_table, field_name, field_description):
        # Elimina un registro y actualiza la tabla y el formulario
        self.item_controller.remove_item(item_id)
        self.page.snack_bar = ft.SnackBar(ft.Text("Item eliminado"))
        self.page.snack_bar.open = True
        self._clear_form(field_name, field_description)
        self._refresh_table(data_table, field_name, field_description)

    # ----------------------------------------
    # Overlays
    # ----------------------------------------

    def build_info_overlay(self, close_callback):
        # Crea el contenido del overlay de información
        return ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Información", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Este es un overlay reutilizable.", color=ft.Colors.WHITE),
                ft.ElevatedButton("Cerrar", on_click=close_callback)
            ]
        )

    def build_image_overlay(self, close_callback):
        # Crea el contenido del overlay que muestra una imagen estática del asset
        return ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Imagen", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Image(src="imagendeejemplo.png", width=250),
                ft.ElevatedButton("Cerrar", on_click=close_callback)
            ]
        )

    # ----------------------------------------
    # Filepicker y manejo de imágenes
    # ----------------------------------------

    async def pick_image(self, e):
        # Lanza el selector de imagen y actualiza la vista previa si el usuario selecciona una imagen
        result = await self.image_service.pick_image()
        if result:
            self.img_preview.src = result
            self.img_preview.visible = True
            self.page.update()

    # ----------------------------------------
    # Construcción de UI principal
    # ----------------------------------------

    def build(self):
        # Construye la interfaz principal, inicializa controles y devuelve la página completa
        # Variables locales para el formulario y la tabla, necesarias para refrescar datos y limpiar campos.
        field_name = ft.TextField(label="Nombre", width=300)
        field_description = ft.TextField(label="Descripción", width=300)
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[],
            width=800
        )
        # Carga inicial de datos en la tabla
        self._refresh_table(data_table, field_name, field_description)
        # Card que contiene el formulario y la tabla, para mejor organización visual.
        form_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=20,
                content=ft.Column( #layout vertical dentro de la card
                    spacing=10,
                    controls=[ 
                        ft.Text("CRUD items (SQLite)", size=18, weight=ft.FontWeight.BOLD),
                        field_name,
                        field_description,
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.ElevatedButton("Guardar", on_click=lambda e: self._save_item(e, field_name, field_description, data_table)),
                                ft.ElevatedButton("Limpiar", on_click=lambda e: (self._clear_form(field_name, field_description), self.page.update()))
                            ]
                        ),
                        data_table
                    ]
                )
            )
        )
# El contenido principal de la vista, con un título, un divider y el card que contiene el CRUD.
        main_content = ft.Container(
            expand=True,
            content=ft.Column(
                scroll="auto",
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Inicio", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.ElevatedButton("Mostrar Info", on_click=lambda e: self.overlay_info.show()),
                            ft.ElevatedButton("Mostrar Imagen", on_click=lambda e: self.overlay_image.show())
                        ]
                    ),
                    ft.ElevatedButton("Seleccionar Imagen", on_click=self.pick_image),
                    self.img_preview,
                    form_card
                ]
            )
        )

        return ft.Stack(
            expand=True,
            controls=[
                main_content,
                self.overlay_info.build(),
                self.overlay_image.build()
            ]
        )
