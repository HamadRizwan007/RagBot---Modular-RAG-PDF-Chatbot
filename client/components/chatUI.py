import streamlit as st
from utils.api import ask_question, clear_db_api

def render_chat():
    st.subheader("💬 Chat with your documents")

    # Add a clear button to the sidebar
    with st.sidebar:
        if st.button("🗑️ Clear All Documents & Chat"):
            response = clear_db_api()
            if response.status_code == 200:
                st.session_state.messages = [] # Clear the chat UI
                st.success("Memory wiped successfully!")
            else:
                st.error("Failed to clear database.")
                    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Input and response
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = ask_question(user_input)
        if response.status_code == 200:
            data = response.json()
            answer_data = data.get("answer", {})
            answer = answer_data["response"]
            sources = answer_data.get("sources", [])
            st.chat_message("assistant").markdown(answer)
            if sources:
                st.markdown("📄 **Sources:**")
                for src in sources:
                    st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.text}")