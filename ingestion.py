from dotenv import load_dotenv
import os
from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

# https://llamahub.ai/l/readers/llama-index-readers-file?from=readers
from llama_index.readers.file import UnstructuredReader
from pinecone import Pinecone
import nltk

load_dotenv()

nltk.download("averaged_perceptron_tagger")

if __name__ == "__main__":
    print("Going to ingest pinecone documentation...")

    # criando leitor de diretório
    dir_reader = SimpleDirectoryReader(
        input_dir="./llamaindex-docs-tmp",
        file_extractor={".html": UnstructuredReader()},
    )

    # Lista com os documentados gerados apartir dos .html
    documents = dir_reader.load_data()

    # Criando nós
    node_parser = SimpleNodeParser().from_defaults(chunk_size=500, chunk_overlap=20)
    nodes = node_parser.get_nodes_from_documents(documents=documents)
    pass
