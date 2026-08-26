import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import contextlib

import tqdm

tqdm.tqdm.set_lock(contextlib.nullcontext())
import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
)
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

MODELS_BY_PROVIDER = {
    "groq": "openai/gpt-oss-120b",
    "anthropic": "claude-haiku-4-5-20251001",
    "openai": "gpt-4o-mini",
    "ollama": "llama3.2",
}


def build_llm(provider: str):
    model = MODELS_BY_PROVIDER[provider]

    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=model)

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model)

    elif provider == "ollama":
        from langchain_ollama import OllamaLLM

        return OllamaLLM(model=model)

    else:
        raise ValueError(f"Unknown provider: {provider}")


# Load documents
def load_documents(cwd: str) -> list[Document]:

    pdf_loader = DirectoryLoader(cwd, glob="**/*.pdf", loader_cls=PyPDFLoader)

    return pdf_loader.load()


# Split documents


# Initialize the text splitter
def split_documents(docs: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )

    # Split loaded document pages (e.g. from a PDF loader)
    return text_splitter.split_documents(docs)


def build_vectorstore(all_splits: list[Document]) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(documents=all_splits, embedding=embeddings)


def rag_chain(vectorstore: Chroma, llm) -> Runnable:
    retriever = vectorstore.as_retriever()

    template = """
        Answer the question using only the context below.

        FORMATTING RULES - this is displayed in a plain terminal:
        - For math, use Unicode symbols directly in your text instead of LaTeX:
          - Superscripts: x² x³ (not x^2, x^3) — use ² ³ ⁴ ⁵ ⁿ etc.
          - Subscripts: use ₀ ₁ ₂ ₓ etc. where natural, or write plainly (F_x -> "F sub x")
          - Square root: √x (not \\sqrt{{x}})
          - Fractions: write as "dy/dx" or "(a+b)/c", or use ½ ⅓ ¼ for simple ones
          - Symbols: use ∂ π ∞ ≤ ≥ × ÷ ± ∫ Σ Δ → directly as characters
          - Do NOT use LaTeX commands or backslashes (no \\frac, \\lim, \\sqrt, \\(, \\[, $$, etc.)
        - Do not use markdown formatting (no **bold**, no *italics*, no markdown bullet asterisks).
        - Use plain numbered lists (1. 2. 3.) or simple dashes (-) for lists.
        - Write in plain, complete sentences.

        Context:
        {context}

        Question: {question}
        Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


# result = rag_chain.invoke("What subjects do I have to study")
# print(result)
