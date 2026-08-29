from pathlib import Path

from textual.app import App

from ragctl.screens.welcome_screen import WelcomeScreen


class Ragctl(App):
    ANSI_COLOR_NAMES = True  # (setting name may vary slightly by Textual version — check `textual --version` docs)
    CSS_PATH = Path(__file__).parent / "ragctl.scss"

    def __init__(self) -> None:
        self.selected_provider: str | None = None
        super().__init__()
        self.theme = "ansi-dark"

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())
