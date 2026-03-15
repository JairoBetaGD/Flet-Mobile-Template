import flet as ft
from src.components.bottom_nav import BottomNav
from src.components.overlay_base import OverlayBase


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.navigation_bar = BottomNav(self.page).build()

        # Crear overlays 
        self.overlay_info = OverlayBase(page, None)
        self.overlay_image = OverlayBase(page, None)

        # Construir el contenido con el Hide
        self.overlay_info.container.content.content = self.build_info_overlay(
            self.overlay_info.hide
        )

        self.overlay_image.container.content.content = self.build_image_overlay(
            self.overlay_image.hide
        )

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
            scroll="auto",
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

    # 🔹 Vista principal
    def build(self):
        main_content = ft.Container(
            expand=True,
            content=ft.Column( #Main Column
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
