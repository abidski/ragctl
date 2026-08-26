from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen

from ragctl.api_key import save_key
from ragctl.screens.chat_screen import ChatScreen
from ragctl.widgets.api_input import ApiInputForm


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
        self.app.push_screen(ChatScreen(self.provider, event.key))
