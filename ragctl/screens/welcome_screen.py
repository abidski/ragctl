from textual import on
from textual.app import ComposeResult
from textual.screen import Screen

from ragctl.api_key import get_api_key
from ragctl.screens.api_key_input_screen import ApiKeyInputScreen
from ragctl.screens.chat_screen import ChatScreen
from ragctl.widgets.provider_picker import ProviderPicker
from ragctl.widgets.welcome import Welcome


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Welcome()
        yield ProviderPicker()

    def on_mount(self) -> None:
        self.query_one(ProviderPicker).focus()

    @on(ProviderPicker.ProviderChosen)
    def handle_provider_chosen(self, event: ProviderPicker.ProviderChosen) -> None:
        self.app.selected_provider = event.provider
        api_key = get_api_key(self.app.selected_provider)
        if api_key:
            self.app.push_screen(ChatScreen(self.app.selected_provider, api_key))
        else:
            self.app.push_screen(ApiKeyInputScreen(provider=event.provider))
