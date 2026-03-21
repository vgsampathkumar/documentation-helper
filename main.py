from typing import Any, Dict, List
import streamlit as st
from backend.core import run_llm

def _format_sources(context_docs: List[Any]) -> List[str]:
    return [
        str((meta.get("source") or "Unknown"))
        for doc in (context_docs or [])
        if (meta := (getattr(doc, "metadata", None) or {})) is not None
    ]

def handle_query(query: str):
    """Consolidated logic to handle both text input and button clicks."""
    # 1. Append user message to state
    st.session_state.messages.append({"role": "user", "content": query, "sources": []})
    
    # 2. Trigger the response generation
    with st.chat_message("assistant"):
        try:
            with st.spinner("Retrieving docs and generating answer…"):
                result: Dict[str, Any] = run_llm(query)
                answer = str(result.get("answer", "")).strip() or "(No answer returned.)"
                sources = _format_sources(result.get("context", []))

                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for s in sources:
                            st.markdown(f"- {s}")

                # 3. Append assistant message to state
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
        except Exception as e:
            st.error("Failed to generate a response.")
            st.exception(e)
    
    # Rerun to ensure UI stays in sync
    st.rerun()

st.set_page_config(page_title="LangChain Documentation Helper", layout="centered")
st.title("LangChain Documentation Helper")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me anything about LangChain docs. I’ll retrieve relevant context and cite sources.",
            "sources": [],
        }
    ]

# Sidebar Logic
with st.sidebar:
    st.subheader("Session")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

    st.subheader("Sample Questions")
    sample_questions = [
        "What is LangChain?",
        "How do I create a vector store in LangChain?",
        "What are the main features of LangChain?",
        "How can I use LangChain for RAG applications?",
        "What language models does LangChain support?",
    ]
    for q in sample_questions:
        # Check if button is clicked and call the handler
        if st.button(q, use_container_width=True):
            handle_query(q)

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- {s}")

# Chat Input Logic
prompt = st.chat_input("Ask a question about LangChain…")
if prompt:
    # Display the user's input immediately before the spinner
    with st.chat_message("user"):
        st.markdown(prompt)
    # Process the query
    handle_query(prompt)