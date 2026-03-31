import flet as ft

class OverlayBase:
    def __init__(self, page: ft.Page, content: ft.Control):
        self.page = page

        self.container = ft.Container(
            expand=True,
            visible=False,
            bgcolor=ft.Colors.BLACK_54,
            alignment=ft.Alignment.CENTER,
            content=ft.Container(
                width=350,
                padding=20,
                bgcolor=ft.Colors.BLACK,
                border_radius=12,
                content=content  # 🔥 aquí va cualquier UI
            )
        )

    def show(self):
        self.container.visible = True
        self.page.update()

    def hide(self, e=None):
        self.container.visible = False
        self.page.update()

    def build(self):
        return self.container