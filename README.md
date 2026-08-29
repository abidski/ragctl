# ragctl


## Introduction

`ragctl` is a TUI that allows LLMs to answer questions based on your documents. The application implements the RAG pattern using Python and libraries such as LangChain, ChromaDB, and Textual. It applies RAG pipeline techniques such as document chunking, vector embedding, and semantic retrieval.

## Installation

Install ragctl with [pipx](https://github.com/pypa/pipx):

```bash
git clone https://github.com/abidski/ragctl.git
cd ragctl
pipx install .
```

## Quickstart

Go to your directory with your documents and launch ragctl from the command line:

```bash
cd ./project
ragctl
```
