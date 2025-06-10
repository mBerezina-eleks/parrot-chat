import streamlit as st
from src.loader import upload_files, extract_text
from src.rag_engine import documents_count
from src.ai_engine import generate_response, detect_pii

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Parrot Chat 🦜")
st.success("Use 🦜 as a multiplier")

with st.sidebar:    
    st.subheader("Context")
    uploaded_context = st.file_uploader(
        "Provide context files", type=["txt", "pdf"], accept_multiple_files=True
    )
    st.info(f"Uploaded files: {documents_count()}")
    st.divider()
    st.subheader("PII check")
    uploaded_file = st.file_uploader("Provide files for PII check", type=["txt", "pdf"])

if uploaded_context:
    upload_files(uploaded_context)
    
for q, a in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("ai"):
        st.write(a)

if uploaded_file:
    st.chat_message("user").write(f"Uploaded `{uploaded_file.name}` file")
    text = extract_text(uploaded_file)
    pii_result = detect_pii(text)
    st.chat_message("assistant").write(pii_result)
    st.session_state.chat_history.append((f"Uploaded `{uploaded_file.name}` file", pii_result))

prompt = st.chat_input("Say something")
if prompt:
    st.chat_message("user").write(prompt)
    response = generate_response(prompt)
    st.chat_message("assistant").write(response)
                