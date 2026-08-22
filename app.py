from pathlib import Path

from textual.app import App

from ragctl.screens.welcome_screen import WelcomeScreen


class Ragctl(App):
    CSS_PATH = Path(__file__).parent / "ragctl.scss"

    def __init__(self) -> None:
        self.selected_provider: str | None = None
        super().__init__()

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    app = Ragctl()
    app.run()
