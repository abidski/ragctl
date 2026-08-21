"""Show a welcome box on the home page when the user has
no chat history.
"""

from rich.console import RenderableType
from textual.widgets import Static


class Welcome(Static):
    MESSAGE = """

You can now ask your LLM anything about your files
"""

    BORDER_TITLE = "Welcome to ragctl!"

    def render(self) -> RenderableType:
        return self.MESSAGE

    def _action_open_repo(self) -> None:
        import webbrowser

        webbrowser.open("https://github.com/darrenburns/elia")

    def _action_open_issues(self) -> None:
        import webbrowser

        webbrowser.open("https://github.com/darrenburns/elia/issues")
