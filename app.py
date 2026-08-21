from pathlib import Path
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, RichLog
from textual.containers import Vertical, Center
from ragctl.screens.welcome_screen import WelcomeScreen


class Ragctl(App):
    CSS_PATH = Path(__file__).parent / "ragctl.scss"

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    app = Ragctl()
    app.run()
