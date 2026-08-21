from textual.screen import Screen
from textual.widgets import Footer
from ragctl.widgets.welcome import Welcome
from textual.app import ComposeResult
from ragctl.widgets.model_picker import ModelPicker


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Welcome()
        yield ModelPicker()

    def on_mount(self) -> None:
        self.query_one(ModelPicker).focus()
