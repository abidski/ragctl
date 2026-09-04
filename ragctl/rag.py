import os

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import contextlib

import tqdm

tqdm.tqdm.set_lock(contextlib.nullcontext())
import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
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

    elif provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model)
    elif provider == "ollama":
        from langchain_ollama import OllamaLLM

        return OllamaLLM(model=model)

    else:
        raise ValueError(f"Unknown provider: {provider}")


# Load documents
def load_documents(cwd: str) -> list[Document]:

    pdf_loader = DirectoryLoader(cwd, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(cwd, glob="**/*.docx", loader_cls=Docx2txtLoader)
    md_loader = DirectoryLoader(cwd, glob="**/*.md", loader_cls=TextLoader)
    return pdf_loader.load() + docx_loader.load() + md_loader.load()


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


def build_search_tool(vectorstore: Chroma):
    @tool
    def search_documents(query: str) -> str:
        """Search the indexed documents for content relevant to the query.
        Use this whenever you need information from the documents to answer
        the user's question. You can call this multiple times with different
        queries if the first search doesn't return enough information."""
        retriever = vectorstore.as_retriever()
        results = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in results)

    return search_documents


def build_agent(vectorstore: Chroma, llm):

    search_tool = build_search_tool(vectorstore)
    tools = [search_tool]

    agent_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful assistant that answers questions using
            the search_documents tool to find relevant information. Search as many times
            as needed with different queries to fully answer the question.

            FORMATTING RULES - displayed in a plain terminal:
            - No LaTeX, no markdown bold/bullets. Use Unicode math symbols (², √, ∂, etc.)
              and plain dashes for lists.""",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# result = rag_chain.invoke("What subjects do I have to study")
# print(result)
