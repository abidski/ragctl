from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.widget import Widget
from textual.widgets import Input, Button, Static


class ApiInputForm(Widget):
    CSS = """
#api-key-input > .input--cursor {
  background: grey;
  color: black;
}
"""

    def compose(self) -> ComposeResult:

        yield Static("Enter your API key:", id="form-title")
        yield Vertical(
            Center(
                Input(placeholder="Enter your API key...", id="api-key-input"),
                Button("Continue", id="submit-btn", variant="primary"),
            ),
        )
