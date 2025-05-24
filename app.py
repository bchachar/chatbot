import streamlit as st
from chatbot import Chatbot
import json
import os

# Constants
CHAT_HISTORY_FILE = "chat_history.json"

def save_chat_history(messages):
    """Save chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(messages, f)

def load_chat_history():
    """Load chat history from JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def initialize_session_state():
    """Initialize session state variables."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = Chatbot()
    if "messages" not in st.session_state:
        # Load previous messages from file
        st.session_state.messages = load_chat_history()
        # Rebuild conversation memory from loaded messages
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.session_state.chatbot.get_response(msg["content"])

def main():
    st.title("Multi-Turn Chatbot with Memory")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get chatbot response
        with st.chat_message("assistant"):
            response = st.session_state.chatbot.get_response(prompt)
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)
    
    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_memory()
        # Clear the saved chat history
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
        st.rerun()

if __name__ == "__main__":
    main() 