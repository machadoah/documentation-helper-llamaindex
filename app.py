from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
import os


load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

if __name__ == "__main__":
    print("RAG...")

    index_name = "documentation-helper-llamaindex"
    pinecone_index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    query = "What is a LlamaIndex query engine?"
    query_engine = index.as_query_engine()

    response = query_engine.query(query)
    print(response)
