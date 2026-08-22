from textual.screen import Screen
from textual.widgets import Footer
from ragctl.widgets.welcome import Welcome
from textual.app import ComposeResult
from ragctl.widgets.provider_picker import ProviderPicker
from textual import on
from ragctl.screens.api_key_input_screen import ApiKeyInputScreen


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Welcome()
        yield ProviderPicker()

    def on_mount(self) -> None:
        self.query_one(ProviderPicker).focus()

    @on(ProviderPicker.ProviderChosen)
    def handle_provider_chosen(self, event: ProviderPicker.ProviderChosen) -> None:
        self.app.selected_provider = event.provider
        self.app.push_screen(ApiKeyInputScreen(provider=event.provider))
