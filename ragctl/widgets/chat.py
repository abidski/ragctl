from textual.widget import Widget
from dataclasses import dataclass

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Input, RichLog
from langchain_core.utils.uuid import uuid7


class Chat(Widget):
    @dataclass
    class NewUserMessage(Message):
        text: str

    @dataclass
    class AgentResponseComplete(Message):
        answer: str

    def __init__(self, agent) -> None:
        self.agent = agent
        self.allow_input_submit = True
        self.thread_id = str(uuid7())
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Vertical(
            RichLog(id="chat-log", wrap=True, markup=True),
            Input(
                placeholder="Ask a question about your documents...",
                id="question-input",
            ),
        )

    def on_mount(self) -> None:
        self.query_one("#question-input", Input).focus()

    @on(Input.Submitted)
    async def handle_submit(self, event: Input.Submitted) -> None:
        if not self.allow_input_submit or not event.value.strip():
            return

        question = event.value
        log = self.query_one("#chat-log", RichLog)
        input_widget = self.query_one("#question-input", Input)

        log.write(f"[bold cyan]> {question}[/bold cyan]")
        input_widget.value = ""

        result = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            {"configurable": {"thread_id": self.thread_id}},
        )
        answer = result["messages"][-1].content
        log.write(f"{answer}\n")
