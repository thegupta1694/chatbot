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
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BACKEND_URL = "https://chatbot-deploy-2-u8od.onrender.com"

st.title("💬 AI Chatbot with Context")

# Store conversation history
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add buttons in a horizontal layout
col1, col2 = st.columns(2)

with col1:
    if st.button("Download Chat History"):
        try:
            response = requests.get(f"{BACKEND_URL}/download_history/{st.session_state.user_id}")
            logger.debug(f"Download history response: {response.status_code}")
            if response.status_code == 200:
                chat_history = response.json()
                json_str = json.dumps(chat_history, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="chat_history.json">Click to download chat history</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error(f"Failed to download chat history: {response.text}")
        except Exception as e:
            logger.error(f"Error downloading chat history: {str(e)}")
            st.error(f"Error downloading chat history: {str(e)}")

with col2:
    if st.button("Reset Chat"):
        try:
            response = requests.post(f"{BACKEND_URL}/reset_chat", params={"user_id": st.session_state.user_id})
            logger.debug(f"Reset chat response: {response.status_code}")
            if response.status_code == 200:
                st.session_state.messages = []
                st.rerun()
            else:
                st.error(f"Failed to reset chat: {response.text}")
        except Exception as e:
            logger.error(f"Error resetting chat: {str(e)}")
            st.error(f"Error resetting chat: {str(e)}")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
query = st.chat_input("Type your message...")

if query:
    # Log the query attempt
    logger.debug(f"Sending query: {query}")
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    try:
        # Send request to FastAPI backend
        payload = {
            "user_id": st.session_state.user_id,
            "query": query
        }
        logger.debug(f"Sending request to {BACKEND_URL}/chat with payload: {payload}")
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=60  # Increased timeout
        )
        
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            bot_reply = response_data.get("response", "I'm not sure how to respond.")
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            with st.chat_message("assistant"):
                st.write(bot_reply)
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            logger.error(error_message)
            st.error(error_message)
            
    except requests.exceptions.Timeout:
        error_message = "Request timed out. The server took too long to respond."
        logger.error(error_message)
        st.error(error_message)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        logger.error(error_message)
        st.error(error_message)

