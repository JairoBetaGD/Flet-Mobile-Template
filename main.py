import flet as ft
from src.views.pages.home_view import HomeView

# ----------------------------------------
# Main entrypoint
# ----------------------------------------

async def main(page: ft.Page):
    # Configuración básica de página
    page.padding = 20

    # Barra de navegación fija en la parte superior
    page.appbar = ft.AppBar(
        title=ft.Text("Flet App"),
        center_title=True
    )

    # Instancia la vista principal con su lógica CRUD y overlays
    home = HomeView(page)
    page.add(home.build())

# Ejecuta la app apuntando al directorio de assets
ft.run(
    main,
    assets_dir="assets"
)
