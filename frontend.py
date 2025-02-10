# import streamlit as st
# import requests

# # FastAPI Backend URL
# FASTAPI_URL = "http://127.0.0.1:8000"

# st.title("💬 AI Chatbot with Context")

# # Store conversation history
# if "user_id" not in st.session_state:
#     st.session_state.user_id = "user123"  # Static user_id for now
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# # User input
# query = st.chat_input("Type your message...")

# if query:
#     # Append user message to chat history
#     st.session_state.messages.append({"role": "user", "content": query})
#     with st.chat_message("user"):
#         st.write(query)

#     # Send request to FastAPI backend
#     response = requests.post(
#         f"{FASTAPI_URL}/chat",
#         json={"user_id": st.session_state.user_id, "query": query}
#     )

#     # Process response
#     if response.status_code == 200:
#         bot_reply = response.json().get("response", "I'm not sure how to respond.")
#         st.session_state.messages.append({"role": "assistant", "content": bot_reply})

#         # Display bot response
#         with st.chat_message("assistant"):
#             st.write(bot_reply)
#     else:
#         st.error("Error: Could not get a response from the server.")

# # Reset button
# if st.button("Reset Chat"):
#     requests.post(f"{FASTAPI_URL}/reset_chat", json={"user_id": st.session_state.user_id})
#     st.session_state.messages = []
#     st.experimental_rerun()

import streamlit as st
import requests
import json
import base64
import os

BACKEND_URL = "https://chatbot-1-hh3z.onrender.com"

response = requests.post(f"{BACKEND_URL}/api", json={"message": user_input})


st.title("💬 AI Chatbot with Context")

# Store conversation history
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"  # Static user_id for now
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add buttons in a horizontal layout
col1, col2 = st.columns(2)

with col1:
    if st.button("Download Chat History"):
        try:
            response = requests.get(f"{FASTAPI_URL}/download_history/{st.session_state.user_id}")
            
            if response.status_code == 200:
                # Create a download link for the JSON file
                chat_history = response.json()
                json_str = json.dumps(chat_history, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="chat_history.json">Click to download chat history</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("Failed to download chat history")
        except Exception as e:
            st.error(f"Error downloading chat history: {str(e)}")

with col2:
    if st.button("Reset Chat"):
        requests.post(f"{FASTAPI_URL}/reset_chat", params={"user_id": st.session_state.user_id})
        st.session_state.messages = []
        st.rerun()


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
query = st.chat_input("Type your message...")

if query:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # Send request to FastAPI backend
    response = requests.post(
        f"{FASTAPI_URL}/chat",
        json={"user_id": st.session_state.user_id, "query": query}
    )

    # Process response
    if response.status_code == 200:
        bot_reply = response.json().get("response", "I'm not sure how to respond.")
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # Display bot response
        with st.chat_message("assistant"):
            st.write(bot_reply)
    else:
        st.error("Error: Could not get a response from the server.")

