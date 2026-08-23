from ragctl.models import build_llm
from ragctl.rag import load_documents, build_vectorstore, build_rag_chain
from pathlib import Path
import os


class ChatScreen(Screen):
    def __init__(self, provider: str, api_key: str) -> None:
        self.provider = provider
        self.api_key = api_key
        self.docs_folder = str(Path.cwd())
        super().__init__()

    def on_mount(self) -> None:

        os.environ[f"{self.provider.upper()}_API_KEY"] = self.api_key

        llm = build_llm(self.provider)
        docs = load_documents(self.docs_folder)
        vectorstore = build_vectorstore(docs)
        self.rag_chain = build_rag_chain(vectorstore, llm)
