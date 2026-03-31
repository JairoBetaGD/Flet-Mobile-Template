import flet as ft
import base64

class ImagePickerService:
    def __init__(self, page: ft.Page):
        self.page = page
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)

        self.image_base64 = None
        self.file_name = None

    async def pick_image(self):
        result = await self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"],
            with_data=True
        )

        if result:
            file = result[0]

            # convertir a base64
            base64_str = base64.b64encode(file.bytes).decode("utf-8")

            ext = file.name.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"

            # guardar estado
            self.image_base64 = f"data:{mime};base64,{base64_str}"
            self.file_name = file.name

            return self.image_base64

        return None