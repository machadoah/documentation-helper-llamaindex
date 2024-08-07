import os

import nltk
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
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

    dir_reader = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        file_extractor={".html": UnstructuredReader()},
    )

    documents = dir_reader.load_data()
    node_parser = SimpleNodeParser().from_defaults(chunk_size=500, chunk_overlap=20)
    nodes = node_parser.get_nodes_from_documents(documents=documents)

    llm = Groq(model="llama-3.1-70b-versatile", temperature=0)
    embedding_model = HuggingFaceEmbedding(
        model_name="intfloat/multilingual-e5-large", embed_batch_size=100
    )

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pinecone_index = pc.Index(name=os.environ["PINECONE_INDEX_NAME"])
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        embed_model=embedding_model,
        show_progress=True,
    )

    print("finished ingesting...")
