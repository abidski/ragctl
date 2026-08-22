from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.screen import ModalScreen
from ragctl.widgets.api_input import ApiInputForm


class ApiKeyInputScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield ApiInputForm()
