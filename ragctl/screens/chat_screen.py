import os
from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, LoadingIndicator
from textual.widgets import Static

from ragctl.rag import (
    build_llm,
    build_vectorstore,
    load_documents,
    build_agent,
    split_documents,
)
from ragctl.widgets.chat import Chat


class ChatScreen(Screen):
    def __init__(self, provider: str, api_key: str) -> None:
        self.provider = provider.lower()
        self.api_key = api_key
        self.docs_folder = str(Path.cwd())
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator(id="loading")
        yield Footer()

    def on_mount(self) -> None:
        self.run_worker(self._setup, thread=True)

    def _setup(self) -> None:
        os.environ[f"{self.provider.upper()}_API_KEY"] = self.api_key
        try:
            llm = build_llm(self.provider)
            docs = load_documents(self.docs_folder)
            splits = split_documents(docs)
            vectorstore = build_vectorstore(splits)
            agent = build_agent(vectorstore, llm)
            self.app.call_from_thread(self._on_ready, agent)
        except Exception as e:
            self.app.call_from_thread(self._on_error, str(e))

    def _on_ready(self, chain) -> None:
        self.query_one("#loading").remove()
        self.mount(Chat(chain))

    def _on_error(self, error_message: str) -> None:
        self.query_one("#loading").remove()
        self.mount(Static(f"[red]Error: {error_message}[/red]"))
