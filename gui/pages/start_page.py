from flet import *
from gui.resources.resources_path import (ImagePaths, FontsPath)


class Start:
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
        welcome_button = ElevatedButton(
            text="Welcome",
            on_click=self.start,
            bgcolor='#2a2a2a',
            color='#FFFFFF',
            width=180,
            height=40,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            )
        )

        stack_text = Stack(
            [
                Text('Educare', font_family='Brittany', size=60, weight='bold', color='#7fc3e9'),
                Text('IA', font_family='Cardo', size=60, weight='bold', color='#2a2a2a', offset=Offset(1.2, 0.45))
            ]
        )

        banner_image = Image(src=self.images.image_1, fit=ImageFit.COVER)

        center_column = Column(
            controls=[
                Container(height=30),
                stack_text,
                Container(height=100),
                welcome_button,
                Container(height=80),
                banner_image
            ],
            alignment='center',
            horizontal_alignment='center',
            spacing=20,
            expand=True
        )

        elements = Container(
            content=Row(
                controls=[
                    center_column
                ],
                alignment='spaceEvenly',
                vertical_alignment='center',
            ),
            bgcolor="#fffffe",
            padding=0,
            expand=True
        )
        return elements

    def start(self, e):
        self.page.go("/selection_interface_page")
