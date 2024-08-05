from dotenv import load_dotenv
import os
from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    VectorStoreIndex,
    StorageContext
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(
        api_key=os.environ["PINECONE_API_KEY"]
    )

print(pc.list_indexes().names())

if __name__ == '__main__':
    print('Going to ingest pinecone documentation...')
    from llama_index.readers.file import UnstructuredReader

    dir_reader = SimpleDirectoryReader(
        input_dir="./llamaindex-docs-tmp",
        file_extractor={".html": UnstructuredReader()},
    )
    documents = dir_reader.load_data()

    pass
