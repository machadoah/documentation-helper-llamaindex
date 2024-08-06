from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.chat_engine.types import ChatMode
import streamlit as st
import os


load_dotenv()


@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index_name = "documentation-helper-llamaindex"
    pinecone_index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


index = get_index()

if "chat_engine" not in st.session_state.keys():
    st.session_state["chat_engine"] = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT, verbose=True
    )


st.set_page_config(
    page_title="Chat with LlamaIndex docs, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Chat with LlamaIndex docs 💬 🦙")

if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Ask me a question about LlamaIndex open sorce python library?",
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
            message = {"role": "assistant", "content": response.response}
            st.session_state["messages"].append(message)
