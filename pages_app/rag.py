import os
import time
import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex, Document
from utils.pdf_reader import PDFReader

openai.api_key = st.secrets.openai_key

def clear_cache():
    if "cache_key" in st.session_state:
        del st.session_state["cache_key"]

def generate_cache_key(chunk_size, overlap_size):
    return f"cache_{chunk_size}_{overlap_size}"

@st.cache_resource(show_spinner=False)
def load_data_with_chunk_size(chunk_size, overlap_size, cache_key):
    start_time = time.time()
    with st.spinner(text="Loading and indexing the docs – hang tight! This should take 1-2 minutes."):
        reader = PDFReader(input_dir="./pdfs", chunk_size=chunk_size, overlap_size=overlap_size)
        docs = reader.load_data()

        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5,
                              system_prompt="You are an expert on university document library. Answer questions based on the provided information.")
        index = VectorStoreIndex.from_documents(docs)

        end_time = time.time()
        processing_time = end_time - start_time
        st.write(f"Processing time: {processing_time:.2f} seconds")

        return index, docs

def rag():
    precision = st.radio("Select precision level:", ["Low", "Medium", "High"])

    if precision == "Low":
        chunk_size, overlap_size = 200, 20
    elif precision == "Medium":
        chunk_size, overlap_size = 100, 10
    else:  # High precision
        chunk_size, overlap_size = 50, 5

    cache_key = generate_cache_key(chunk_size, overlap_size)

    if "cache_key" not in st.session_state or st.session_state.cache_key != cache_key:
        clear_cache()
    st.session_state.cache_key = cache_key

    index, docs = load_data_with_chunk_size(chunk_size, overlap_size, cache_key)

    if "chat_engine" not in st.session_state or st.session_state.chunk_size != chunk_size:
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
        st.session_state.chunk_size = chunk_size
        st.session_state.docs = docs

    if prompt := st.text_input("Your question"):
        st.session_state.messages = [{"role": "user", "content": prompt}]

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(st.session_state.messages[-1]["content"])
            source_nodes = response.source_nodes
            if source_nodes:
                sources = []
                context_snippets = []
                for node in source_nodes:
                    source_path = node.node.extra_info.get('file_path', "Unknown source")
                    source_file = os.path.basename(source_path)
                    if source_file not in sources:
                        sources.append(source_file)
                    context_snippets.append((source_file, node.node.text))

                st.session_state.messages.append(
                    {"role": "assistant", "content": response.response, "sources": sources, "contexts": context_snippets})
            else:
                st.session_state.messages.append({"role": "assistant", "content": response.response})

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.session_state.messages[-1]["role"] == "assistant" and "sources" in st.session_state.messages[-1]:
            sources = st.session_state.messages[-1]["sources"]
            if sources:
                st.markdown(
                    f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">'
                    f'**Sources:**'
                    f'<ul>'
                    f'{"".join([f"<li>{source}</li>" for source in sources])}'
                    f'</ul>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                def download_files():
                    for i, source in enumerate(sources):
                        source_path = os.path.join("pdfs", source)
                        with open(source_path, "rb") as f:
                            contents = f.read()
                        st.download_button(label=f"Download {source}", data=contents, file_name=source,
                                           mime="application/pdf", key=f"download_{i}")

                download_files()

    with col2:
        st.markdown(
            '<div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">'
            f'{st.session_state.messages[-1]["content"]}'
            '</div>',
            unsafe_allow_html=True
        )

        if "contexts" in st.session_state.messages[-1]:
            st.markdown(
                '<div style="background-color: #e9e9e9; padding: 10px; border-radius: 5px;">'
                '<strong>Context Snippets:</strong>'
                '<ul>'
                f'{"".join([f"<li><strong>{source}:</strong> {context}</li>" for source, context in st.session_state.messages[-1]["contexts"]])}'
                '</ul>'
                '</div>',
                unsafe_allow_html=True
            )

if __name__ == '__main__':
    rag()
