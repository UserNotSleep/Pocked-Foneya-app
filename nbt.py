import flet as ft

def main(page: ft.Page):
    # Заголовок
    page.title = "Image Example"

    # Создание и добавление изображения на страницу
    image = ft.Image(src="image.png", width=300, height=300)
    page.add(image)

ft.app(target=main)
