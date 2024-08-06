from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.chat_engine.types import ChatMode

from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from tools.duplicate_postprocessing import DuplicateRemoverNodePostprocessor
from llama_index.embeddings.openai import OpenAIEmbedding

import streamlit as st
import os

load_dotenv()


@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pinecone_index = pc.Index(name=os.environ["PINECONE_INDEX_NAME"])
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


index = get_index()

if "chat_engine" not in st.session_state.keys():
    postprocessor = SentenceEmbeddingOptimizer(
        embed_model=OpenAIEmbedding(), percentile_cutoff=0.5, threshold_cutoff=0.7
    )

    st.session_state["chat_engine"] = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=True,
        node_postprocessors=[postprocessor, DuplicateRemoverNodePostprocessor()],
    )


st.set_page_config(
    page_title="Llamaindex Chat 💬 🦙",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("LlamaIndex Chat 💬 🦙")

if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Você tem alguma duvida sobre o Llamaindex? Pergunte-me!",
        }
    ]

if prompt := st.chat_input("Your question"):
    st.session_state["messages"].append({"role": "user", "content": prompt})

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state["messages"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state["chat_engine"].chat(message=prompt)
            st.write(response.response)

            nodes = [node for node in response.source_nodes]
            for i, node in enumerate(nodes):
                with st.expander(f"Source Node {i + 1}: score= {node.score}"):
                    st.write(node.text)

            message = {"role": "assistant", "content": response.response}
            st.session_state["messages"].append(message)
