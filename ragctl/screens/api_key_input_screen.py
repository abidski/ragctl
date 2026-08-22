from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.screen import ModalScreen
from ragctl.widgets.api_input import ApiInputForm
from textual import on
from ragctl.api_key import save_key


class ApiKeyInputScreen(ModalScreen):
    def __init__(self, provider: str) -> None:
        self.provider = provider
        super().__init__()

    def compose(self) -> ComposeResult:
        yield ApiInputForm()

    @on(ApiInputForm.KeySubmitted)
    def handle_key_submitted(self, event: ApiInputForm.KeySubmitted) -> None:
        save_key(self.provider, event.key)
        self.dismiss()
