from textual.widgets import OptionList
from textual.widgets.option_list import Option
from ragctl.screens.api_key_input_screen import ApiKeyInputScreen
from textual import on


class ModelPicker(OptionList):
    BORDER_TITLE = "Choose a Provider"
    PROVIDERS = [
        ("Groq", "groq"),
        ("Anthropic", "anthropic"),
        ("OpenAI", "openai"),
    ]

    @on(OptionList.OptionSelected)
    def handle_selection(self, event: OptionList.OptionSelected) -> None:
        selected_id = event.option.id
        self.app.push_screen(ApiKeyInputScreen())

    def on_mount(self) -> None:
        options = [Option(name, id=value) for name, value in self.PROVIDERS]
        self.add_options(options)
