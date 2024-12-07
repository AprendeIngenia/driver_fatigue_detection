from flet import *
from gui.pages.start_page import Start
from gui.pages.selection_interface_page import SelectionInterface
from gui.pages.drowsiness_page import Drowsiness


class MainApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Educare ia"
        self.page.bgcolor = "#fffffe"
        self.page.window.resizable = False
        self.page.padding = 0
        self.page.window.width = 1920
        self.page.window.height = 1080
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"

        self.page.theme = Theme(
            page_transitions=PageTransitionsTheme(
                android=PageTransitionTheme.FADE_UPWARDS,
                ios=PageTransitionTheme.CUPERTINO,
                macos=PageTransitionTheme.ZOOM,
                linux=PageTransitionTheme.ZOOM,
                windows=PageTransitionTheme.FADE_UPWARDS,
            ),
        )

        self.start_page = Start(page)
        self.selection_interface_page = SelectionInterface(page)
        self.drowsiness_page = Drowsiness(page)

        self.page.on_route_change = self.route_change
        self.page.go("/")

    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/":
            self.page.views.append(
                View(
                    route="/",
                    controls=[self.start_page.main()],
                )
            )

        elif self.page.route == "/selection_interface_page":
            self.selection_interface_page.main()
            self.page.views.append(
                View(
                    route="/selection_interface_page",
                    controls=[self.selection_interface_page.main()],
                )
            )

        elif self.page.route == "/drowsiness_page":
            self.page.views.append(
                View(route="/drowsiness_page", controls=[self.drowsiness_page.main()])
            )

        self.page.update()


def main(page: Page):
    MainApp(page)


if __name__ == "__main__":
    app(target=main)
