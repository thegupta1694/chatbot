# from fastapi import FastAPI
# from pydantic import BaseModel
# import ollama
# import datetime
# import json
# from typing import Dict, List

# app = FastAPI()

# # Log file path
# LOG_FILE = "chat_log.jsonl"

# # Store conversation history (session-based)
# chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# class ChatRequest(BaseModel):
#     user_id: str  # Unique user identifier
#     query: str  # User's query

# def log_conversation(user_id, user_query, bot_response):
#     """Logs user queries and bot responses to a JSONL file with timestamps."""
#     log_entry = {
#         "timestamp": datetime.datetime.now().isoformat(),
#         "user_id": user_id,
#         "user_query": user_query,
#         "bot_response": bot_response
#     }
#     with open(LOG_FILE, "a", encoding="utf-8") as log_file:
#         log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     """Handles user queries, remembers conversation context, and returns AI-generated responses."""
#     try:
#         user_id = request.user_id  # Unique user identifier
#         query = request.query

#         # Retrieve chat history for the user
#         if user_id not in chat_sessions:
#             chat_sessions[user_id] = []
        
#         # Format conversation history for context
#         conversation_history = chat_sessions[user_id] + [{"role": "user", "content": query}]

#         # Generate response using LLaMA 3
#         response = ollama.chat(model="llama3", messages=conversation_history)
#         bot_reply = response.get("message", {}).get("content", "I'm not sure how to respond.")

#         # Update the chat history with the new response
#         chat_sessions[user_id].append({"role": "user", "content": query})
#         chat_sessions[user_id].append({"role": "assistant", "content": bot_reply})

#         log_conversation(user_id, query, bot_reply)  # Log the chat

#         return {"status": "success", "query": query, "response": bot_reply}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.post("/reset_chat")
# async def reset_chat(user_id: str):
#     """Clears the chat history for a given user."""
#     if user_id in chat_sessions:
#         del chat_sessions[user_id]
#     return {"status": "success", "message": "Chat history reset for user."}

from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import datetime
import json
from typing import Dict, List
from fastapi.responses import JSONResponse

app = FastAPI()

# Log file path
LOG_FILE = "chat_log.jsonl"

# Store conversation history (session-based)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

class ChatRequest(BaseModel):
    user_id: str  # Unique user identifier
    query: str  # User's query

def log_conversation(user_id, user_query, bot_response):
    """Logs user queries and bot responses to a JSONL file with timestamps."""
    if not user_id:  # Prevent empty user_id entries
        print(f"Skipping log entry due to missing user_id: {user_query}")
        return
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "user_query": user_query,
        "bot_response": bot_response
    }
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def clear_user_logs(user_id):
    """Clears logs for a specific user while keeping other users' logs."""
    try:
        if not os.path.exists(LOG_FILE):
            print("Log file does not exist, nothing to clear.")
            return  # If the log file doesn't exist, there's nothing to clear

        with open(LOG_FILE, "r", encoding="utf-8") as file:
            all_logs = [json.loads(line) for line in file]

        # Debug: Print log count before filtering
        print(f"Total logs before filtering: {len(all_logs)}")

        # Keep only logs that do NOT belong to the user
        filtered_logs = [log for log in all_logs if log["user_id"] != user_id]

        # Debug: Print log count after filtering
        print(f"Total logs after filtering: {len(filtered_logs)}")

        # Overwrite the file with filtered logs
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            for log in filtered_logs:
                file.write(json.dumps(log, ensure_ascii=False) + "\n")

        # Debug: Print confirmation
        print(f"Logs for user {user_id} cleared successfully.")

    except Exception as e:
        print(f"Error clearing logs for {user_id}: {str(e)}")


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles user queries, remembers conversation context, and returns AI-generated responses."""
    try:
        logger.info(f"Received chat request from user {request.user_id}")
        user_id = request.user_id
        query = request.query

        # Log the incoming request
        logger.debug(f"Query: {query}")

        # Check if Ollama is responsive
        try:
            models = ollama.list()
            logger.info(f"Available models: {models}")
        except Exception as e:
            logger.error(f"Error connecting to Ollama: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to connect to Ollama service")

        # Retrieve chat history
        if user_id not in chat_sessions:
            chat_sessions[user_id] = []
        
        # Format conversation history
        conversation_history = chat_sessions[user_id] + [{"role": "user", "content": query}]
        
        logger.debug(f"Conversation history: {conversation_history}")

        try:
            # Generate response using Ollama
            logger.info("Sending request to Ollama")
            response = ollama.chat(
                model="llama3",
                messages=conversation_history,
                stream=False
            )
            logger.debug(f"Ollama response: {response}")
            
            bot_reply = response.get("message", {}).get("content", "I'm not sure how to respond.")
            
            # Update chat history
            chat_sessions[user_id].append({"role": "user", "content": query})
            chat_sessions[user_id].append({"role": "assistant", "content": bot_reply})
            
            logger.info("Successfully generated response")
            return {"status": "success", "query": query, "response": bot_reply}

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/reset_chat")
async def reset_chat(user_id: str):
    """Clears the chat history and logs for a given user."""
    try:
        # Clear in-memory chat history
        if user_id in chat_sessions:
            del chat_sessions[user_id]

        # Debug: Print before clearing logs
        print(f"Before Clearing: {user_id} logs exist in chat_log.jsonl")

        # Clear user's logs from file
        clear_user_logs(user_id)

        # Debug: Check after clearing logs
        print(f"After Clearing: Checking if {user_id} logs still exist")

        return {"status": "success", "message": "Chat history and logs reset for user."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to reset chat: {str(e)}"}


@app.get("/download_history/{user_id}")
async def download_history(user_id: str):
    """Returns the chat history for a specific user in JSON format."""
    try:
        chat_history = []
        with open(LOG_FILE, "r", encoding="utf-8") as log_file:
            for line in log_file:
                try:
                    entry = json.loads(line)
                    if "user_id" not in entry:
                        print(f"Skipping entry: {entry}")  # Debugging
                        continue  # Skip malformed entries
                    if entry["user_id"] == user_id:
                        chat_history.append(entry)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")  # Debugging

        return JSONResponse(
            content=chat_history,
            headers={
                "Content-Disposition": f"attachment; filename=chat_history_{user_id}.json"
            }
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health")
async def health_check():
    try:
        # Test Ollama connection
        response = ollama.list()
        logger.info(f"Ollama models available: {response}")
        return {"status": "healthy", "ollama_status": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}
