import flet as ft
import base64
from pathlib import Path
from src.events import generate_presed

class PockedFoneyaApp:
    def __init__(self, page: ft.Page):
        """Иницализация основы"""
        self.page = page
        self.image_path = Path("D:/Projects/Pocked Foneya app/image.png")
        self.setup_ui()
        self.generating_images = False

    def setup_ui(self):
        """Настройка элементов интерфейса приложения."""
        self.page.title = "Pocked Foneya"
        self.page.bgcolor = "#2F3136"
        self.page.appbar = ft.AppBar(
            title=ft.Text("Pocked Foneya"),
            center_title=False,
            bgcolor="#36393E",
        )

        self.prompt = ft.TextField(
            label="Prompt",
            hint_text="Enter prompt",
            multiline=False,
            min_lines=1,
            max_lines=2,
        )

        self.negative_prompt = ft.TextField(
            label="Negative prompt",
            hint_text="Enter negative prompt",
            multiline=False,
            min_lines=1,
            max_lines=2,
        )

        self.style_select = ft.Dropdown(
            options=[
                ft.dropdown.Option("Falkon(Default)"),
                ft.dropdown.Option("AbyssOrange"),
                ft.dropdown.Option("PicReal"),
            ],
            width=2000,
            value="Falkon(Default)"
        )

        self.steps = ft.Slider(
            min=10, max=40, divisions=10, label="{value}"
        )

        self.image_display = ft.Image(
            src=self.get_encoded_image(),
            width= 350,
            height= 350 
        )

        """ Используем GestureDetector для отслеживания кликов на изображение """
        image_container = ft.GestureDetector(
            content=self.image_display,
            on_tap=self.on_image_click,
        )

        generate_button = ft.TextButton(
            text="Generate Image",
            width=2000,
            on_click=self.generate_image,
        )

        self.page.add(
            self.prompt,
            self.negative_prompt,
            self.style_select,
            ft.Container(content=ft.Text("Sampling steps"), alignment=ft.alignment.center),
            self.steps,
            generate_button,
            ft.Container(content=image_container, alignment=ft.alignment.center)
        )

    def get_encoded_image(self) -> str:
        """Читает и кодирует изображение в Base64"""
        try:
            with open(self.image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/png;base64,{encoded_image}"
        except FileNotFoundError:
            print(f"Error: File not found at {self.image_path}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Image not found at {self.image_path}"))
            self.page.snack_bar.open = True
            return ""

    def generate_image(self, e):
        """Генерация и обновление изображения"""
        if not self.generating_images:
            self.generating_images = True
            generate_presed(
                e,
                self.prompt.value,
                self.negative_prompt.value,
                self.steps.value,
                self.style_select.value
            )
            """Обновляем изображение после генерации """
            self.image_display.src = self.get_encoded_image()
            self.image_display.update()
            self.generating_images = False

    def on_image_click(self, e):
        """Обработчик клика на изображение"""
        print("Image clicked!") 

def main(page: ft.Page):
    PockedFoneyaApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="D:/Projects/Pocked Foneya app")
