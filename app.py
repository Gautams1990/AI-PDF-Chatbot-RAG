import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage


# -----------------------------
# Setup
# -----------------------------
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📄", layout="wide")

st.markdown(
    """
    <div style="padding: 0.5rem 0 0.25rem 0;">
        <h1 style="margin-bottom: 0;">AI PDF Chatbot</h1>
        <p style="margin-top: 0; color: gray;">
            Upload a PDF, process it, and ask questions with page-level sources.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state
# -----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Helper functions
# -----------------------------
def save_uploaded_pdf(uploaded_file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name


def extract_documents_from_pdfs(pdf_paths: list[str]) -> list[Document]:
    documents = []

    for path in pdf_paths:
        reader = PdfReader(path)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                documents.append(
                    Document(
                        page_content=page_text,
                        metadata={
                            "source": os.path.basename(path),
                            "page": page_num,
                        },
                    )
                )

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_documents(documents)


def build_vectorstore(chunks: list[Document]):
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    return FAISS.from_documents(chunks, embedding=embeddings)


def answer_question(vectorstore, question: str):
    docs = vectorstore.similarity_search(question, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)

    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2,
    )

    messages = [
        SystemMessage(
            content=(
                "You are a helpful PDF chatbot. "
                "Answer only from the provided context. "
                "If the answer is not in the context, say: "
                "\"answer is not available in the context\"."
            )
        ),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{question}"),
    ]

    response = model.invoke(messages)
    answer = response.content

    if isinstance(answer, list):
        answer = answer[0].get("text", str(answer[0]))

    return answer, docs


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Project controls")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    col1, col2 = st.columns(2)
    process = col1.button("Process")
    clear_chat = col2.button("Clear chat")

    if clear_chat:
        st.session_state.messages = []

    if process:
        if not uploaded_files:
            st.error("Please upload at least one PDF.")
        else:
            temp_paths = [save_uploaded_pdf(file) for file in uploaded_files]

            try:
                documents = extract_documents_from_pdfs(temp_paths)

                if not documents:
                    st.error("Could not extract text from the PDF.")
                else:
                    text_chunks = split_documents(documents)
                    vectorstore = build_vectorstore(text_chunks)

                    st.session_state.vectorstore = vectorstore
                    st.session_state.text_chunks = text_chunks
                    st.session_state.messages = []

                    st.success(f"Processed successfully. Created {len(text_chunks)} chunks.")
            finally:
                for path in temp_paths:
                    try:
                        os.remove(path)
                    except Exception:
                        pass

    st.divider()
    if st.session_state.vectorstore is None:
        st.info("No processed PDF yet.")
    else:
        st.success("PDF ready for questions.")


# -----------------------------
# Main chat area
# -----------------------------
st.subheader("Chat")

if st.session_state.messages:
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.write(content)

user_question = st.chat_input("Ask a question from the PDF")

if user_question:
    if st.session_state.vectorstore is None:
        st.warning("Please upload PDFs and click Process first.")
    else:
        st.session_state.messages.append(("user", user_question))

        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the PDF and generating answer..."):
                reply, sources = answer_question(st.session_state.vectorstore, user_question)

            st.write(reply)

            with st.expander("Retrieved chunks", expanded=False):
                for i, doc in enumerate(sources, start=1):
                    page = doc.metadata.get("page", "Unknown")
                    source_file = doc.metadata.get("source", "Unknown")

                    st.markdown(f"### Retrieved Chunk {i}")
                    st.caption(f"Source: {source_file} | Page: {page}")
                    st.write(doc.page_content)
                    st.divider()

        st.session_state.messages.append(("assistant", reply))