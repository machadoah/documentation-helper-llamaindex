import os

import nltk
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.groq import Groq
from llama_index.readers.file import UnstructuredReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pinecone import Pinecone

load_dotenv()

nltk.download("averaged_perceptron_tagger")


if __name__ == "__main__":
    print("Going to ingest pinecone documentation...")

    # Cria um leitor de diretório para ler arquivos HTML
    dir_reader = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        file_extractor={".html": UnstructuredReader()},
    )

    # Lista com os documentos gerados a partir dos arquivos .html
    documents = dir_reader.load_data()

    # Cria nós a partir dos documentos
    node_parser = SimpleNodeParser().from_defaults(chunk_size=500, chunk_overlap=20)
    nodes = node_parser.get_nodes_from_documents(documents=documents)

    # Configura o modelo LLM e o modelo de embeddings
    Settings.llm = Groq(model="llama-3.1-70b-versatile", temperature=0)
    Settings.embedding = HuggingFaceEmbedding(
        model_name="intfloat/multilingual-e5-large", embed_batch_size=100
    )

    # Inicializa o cliente Pinecone com a chave de API
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    # Obtém o índice Pinecone pelo nome
    pinecone_index = pc.Index(name=os.environ['PINECONE_INDEX_NAME'])

    # Cria um armazenamento de vetores usando Pinecone
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Cria um contexto de armazenamento a partir do armazenamento de vetores
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Cria um índice de armazenamento de vetores a partir dos documentos
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        show_progress=True,
    )

    print("finished ingesting...")
