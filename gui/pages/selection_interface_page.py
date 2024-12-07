from flet import *
from gui.resources.resources_path import (ImagePaths, FontsPath)


class SelectionInterface:
    def __init__(self, page):
        super().__init__()
        self.images = ImagePaths()
        self.fonts = FontsPath()

        self.page = page

        self.page.fonts = {
            "Brittany": self.fonts.brittany_font,
            "Cardo": self.fonts.cardo_font
        }

    def main(self):
        drowsiness_image = Image(src=self.images.image_2, fit=ImageFit.COVER)
        translate_image = Image(src=self.images.image_3, fit=ImageFit.COVER)
        emotions_image = Image(src=self.images.image_4, fit=ImageFit.COVER)

        drowsiness_button = ElevatedButton(
            text="Somnolencia",
            on_click=self.drowsiness,
            bgcolor='#944adc',
            color='#FFFFFF',
            width=180,
            height=40,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            )
        )

        translate_button = ElevatedButton(
            text="Traductor",
            on_click=self.translate,
            bgcolor='#007dfe',
            color='#FFFFFF',
            width=180,
            height=40,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            )
        )

        emotions_button = ElevatedButton(
            text="Emociones",
            on_click=self.emotions,
            bgcolor='#e03851',
            color='#FFFFFF',
            width=180,
            height=40,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            )
        )

        left_column = Column(
            controls=[
                Container(height=30),
                drowsiness_image,
                drowsiness_button,
            ],
            alignment='center',
            horizontal_alignment='center',
            spacing=20,
            expand=True
        )

        center_column = Column(
            controls=[
                Container(height=30),
                translate_image,
                translate_button,
            ],
            alignment='center',
            horizontal_alignment='center',
            spacing=20,
            expand=True
        )

        right_column = Column(
            controls=[
                Container(height=30),
                emotions_image,
                emotions_button,
            ],
            alignment='center',
            horizontal_alignment='center',
            spacing=20,
            expand=True
        )

        elements = Container(
            content=Row(
                controls=[
                    left_column,
                    center_column,
                    right_column
                ],
                alignment='spaceEvenly',
                vertical_alignment='center',
            ),
            bgcolor="#fffffe",
            padding=0,
            expand=True
        )
        return elements

    def drowsiness(self, e):
        self.page.go("/drowsiness_page")

    def translate(self, e):
        self.page.go("/translate_page")

    def emotions(self, e):
        self.page.go("/emotions_page")
