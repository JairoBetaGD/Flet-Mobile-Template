import flet as ft
from src.views.home_view import HomeView

async def main(page: ft.Page):
    # Padding Recomendado
    page.padding = 20

    # Barra superior
    page.appbar = ft.AppBar(
        title=ft.Text("Flet Mobile"),
        center_title=True
    )

    # Vista inicial
    home = HomeView(page)
    page.add(home.build())

ft.run(
    main,
    assets_dir="assets"

)

