from dataclasses import dataclass

from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import RadioButton, RadioSet
from ragctl.screens.api_key_input_screen import ApiKeyInputScreen


class ProviderRadioButton(RadioButton):
    def __init__(self, provider: str, label: str, value: bool = False) -> None:
        super().__init__(label, value)
        self.provider = provider  # attach the provider id to the button, same as Elia's ModelRadioButton attaching `model`


class ProviderPicker(Widget):
    BORDER_TITLE = "Choose a Provider"
    PROVIDERS = [
        ("Groq", "groq"),
        ("Anthropic", "anthropic"),
        ("OpenAI", "openai"),
    ]

    @dataclass
    class ProviderChosen(Message):
        provider: str

    def compose(self) -> ComposeResult:
        with RadioSet(id="provider-radio-set") as rs:
            rs.border_title = "Choose a Provider"
            for provider_id, label in self.PROVIDERS:
                yield ProviderRadioButton(provider=provider_id, label=label)

    @on(RadioSet.Changed)
    def handle_selection(self, event: RadioSet.Changed) -> None:
        button = event.pressed  # the RadioButton that was just selected
        provider_id = (
            button.provider
        )  # our custom attribute, since it's a ProviderRadioButton
        self.post_message(self.ProviderChosen(provider=provider_id))
