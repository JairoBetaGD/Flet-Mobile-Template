import flet as ft

class BottomNav:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.NavigationBar(
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    label="Inicio"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON,
                    label="Perfil"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS,
                    label="Ajustes"
                ),
            ],
            on_change=self.on_change
        )

    def on_change(self, e):
        self.page.controls.clear()

        if e.control.selected_index == 0:
            from src.views.pages.home_view import HomeView
            self.page.add(HomeView(self.page).build())

        elif e.control.selected_index == 1:
            self.page.add(
                ft.Text("Perfil", size=22)
            )

        elif e.control.selected_index == 2:
            self.page.add(
                ft.Text("Ajustes", size=22)
            )

        self.page.update()