import tiktoken
from langchain_huggingface import HuggingFaceEmbeddings
import getpass
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter Groq API key: ")


# Initialize the model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


# Load documents
cwd = os.getcwd()
pdf_loader = DirectoryLoader(cwd, glob="**/*.pdf", loader_cls=PyPDFLoader)

docs = pdf_loader.load()

# Split documents

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

# Split loaded document pages (e.g. from a PDF loader)
all_splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)

retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke("What subjects do I have to study")
print(result)
