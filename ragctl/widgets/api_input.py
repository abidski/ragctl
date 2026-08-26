from dataclasses import dataclass

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Static


class ApiInputForm(Widget):
    @dataclass
    class KeySubmitted(Message):
        key: str

    def compose(self) -> ComposeResult:

        yield Static("Enter your API key:", id="form-title")
        yield Vertical(
            Center(
                Input(placeholder="Enter your API key...", id="api-key-input"),
            ),
            Center(
                Button("Continue", id="submit-btn", variant="primary"),
            ),
        )

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    @on(Button.Pressed)
    def handle_submit_button(self) -> None:
        self._submit()

    @on(Input.Submitted)
    def handle_input_submit(self) -> None:
        self._submit()

    def _submit(self) -> None:
        key = self.query_one("#api-key-input", Input).value
        if key:
            self.post_message(self.KeySubmitted(key=key))
