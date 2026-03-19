import flet as ft
from src.components.image_picker_service import ImagePickerService
from src.components.bottom_nav import BottomNav
from src.components.overlay_base import OverlayBase


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.navigation_bar = BottomNav(self.page).build()
#-------------------------------------------------------------------------------------
        # Crear overlays 
        self.overlay_info = OverlayBase(page, None)
        self.overlay_image = OverlayBase(page, None)

        # Construir el contenido con el Hide
        self.overlay_info.container.content = self.build_info_overlay(
            self.overlay_info.hide
        )

        self.overlay_image.container.content = self.build_image_overlay(
            self.overlay_image.hide
        )
#-------------------------------------------------------------------------------------
        # Servicio de selección de imagen
        self.image_service = ImagePickerService(page)

        # Vista previa de imagen seleccionada
        self.img_preview = ft.Image(
            src="",
            width=300,
            height=300,
            fit="contain",
            visible=False
        )
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
    # 🔹 Overlay 1
    def build_info_overlay(self, close_callback):
        return ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Información",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Text(
                    "Este es un overlay reutilizable.",
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "Cerrar",
                    on_click=close_callback
                )
            ]
        )

    # 🔹 Overlay 2
    def build_image_overlay(self, close_callback):
        return ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Imagen",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Image(
                    src="assets/imagendeejemplo.png",
                    width=250
                ),
                ft.ElevatedButton(
                    "Cerrar",
                    on_click=close_callback
                )
            ]
        )
#-------------------------------------------------------------------------------------
    # 🔹 Función para seleccionar imagen
    async def pick_image(self, e):
        result = await self.image_service.pick_image()

        if result:
            self.img_preview.src = result
            self.img_preview.visible = True

            print("Nombre:", self.image_service.file_name)
            print("Base64 listo para guardar")

            self.page.update()
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
    # 🔹 Vista principal
    def build(self):
        main_content = ft.Container(
            expand=True,
            content=ft.Column( #Main Column
                scroll="auto",
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Inicio", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.ElevatedButton(
                                "Mostrar Info",
                                on_click=lambda e: self.overlay_info.show()
                            ),
                            ft.ElevatedButton(
                                "Mostrar Imagen",
                                on_click=lambda e: self.overlay_image.show()
                            ),
                        ]
                    ),
                    ft.ElevatedButton(
                        "Seleccionar Imagen",
                        on_click=self.pick_image
                    ),
                    self.img_preview
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
