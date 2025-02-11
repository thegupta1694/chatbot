Secure Chat Application with LLaMA
Integration ( Backend - app.py )
Overview
This application is a secure WebSocket-based chat system that integrates with the LLaMA
language model through Ollama. It provides both REST API and WebSocket endpoints for
real-time communication, featuring user authentication, conversation persistence, and chat
history management.

Key Features
● Secure Authentication: JWT-based authentication system with password hashing
● Real-time Communication: WebSocket support for instant messaging
● Conversation Persistence: Chat history storage and retrieval
● User Management: Registration and authentication system
● Chat History Management: Download and reset functionality
● Logging System: Comprehensive conversation logging
● LLaMA Integration: AI-powered responses using the LLaMA model via Ollama

Technical Architecture

Authentication System
● Uses OAuth2 with JWT tokens for secure authentication
● Password hashing using bcrypt
● Token-based session management with configurable expiration
● Secure password storage in SQLite database

Chat System Architecture

REST API Endpoints:
● POST /register: User registration
● POST /token: User authentication and token generation
● POST /chat: Synchronous chat endpoint
● POST /reset_chat: Chat history reset
● GET /download_history/{user_id}: Chat history retrieval

WebSocket Implementation:
● Real-time bidirectional communication
● Connection management with user session tracking
● Authenticated WebSocket connections
● Automatic disconnection handling

Data Persistence
● SQLite database for user management
● JSONL-based logging system for chat history
● In-memory session management for active conversations

Security Features
● Password hashing with bcrypt
● JWT token authentication
● User-specific chat history access
● Secure WebSocket connections
● Input validation using Pydantic models

Implementation Details

Database Schema
CREATE TABLE users (
username TEXT PRIMARY KEY,
email TEXT UNIQUE,
hashed_password TEXT
);

Chat Session Management
● Chat sessions are maintained in memory using a dictionary structure
● Each user has their own conversation history
● Sessions persist until explicitly reset or server restart

Logging System
● Logs stored in JSONL format

● Each log entry contains:
○ Timestamp
○ User ID
○ User query
○ Bot response

● User-specific log retrieval and cleanup
API Endpoints
Authentication Endpoints
POST /register

● Register new user

● Required fields: email, username, password 
POST /token
● Login and get access token
● Required fields: username, password

Chat Endpoints
POST /chat
● Send message and get response
● Requires authentication
● Fields: query

POST /reset_chat
● Reset user's chat history
● Requires authentication
● Fields: user_id

GET /download_history/{user_id}
● Download chat history
● Requires authentication

WebSocket Endpoint
WS /ws
● Real-time chat connection
● Requires token in query parameters

Setup and Configuration
Environment Variables
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

Dependencies
● FastAPI
● Pydantic
● PassLib
● PyJWT
● SQLite3
● Ollama
● python-dotenv

Required Files
● app.py: Main application file
● users.db: SQLite database
● chat_log.jsonl: Chat history logs

Security Considerations
Authentication
● Secure password hashing
● Token-based authentication
● Protected endpoints

Data Protection
● User-specific data access
● Secure WebSocket connections
● Input validation

Error Handling
● Graceful error management
● Secure error responses
● Connection cleanup

Future Improvements
● Rate limiting implementation
● Message encryption
● Enhanced error logging
● User roles and permissions
● Database migration system
● Connection pooling
● Message queue integration
● Enhanced monitoring and analytics

Secure Chat Application with LLaMA
Integration ( Frontend )
Frontend Implementation
Overview
The frontend is built using Streamlit, providing a responsive and interactive web interface for
the chat application. It features:
● Real-time message updates through WebSocket connections
● User authentication
● A clean, intuitive chat interface

Key Frontend Features
● Interactive Chat Interface: Real-time messaging with AI responses
● Authentication UI: Login and registration forms
● WebSocket Integration: Real-time message updates
● Session Management: Secure token-based session handling
● Chat History: Download and reset capabilities
● Responsive Design: Adapts to different screen sizes
● Sidebar Controls: Easy access to user actions

Technical Architecture
Components
Authentication Interface
● Login form with username and password
● Registration form with email validation
● Token-based session management

Chat Interface
● Real-time message display
● Message input system
● Chat history visualization
● WebSocket connection management

Sidebar Controls
● Download chat history
● Reset chat functionality
● Logout option
● User session information

Implementation Details
Session Management
WebSocket Communication
● Asynchronous WebSocket connection handler
● Message queue for managing incoming messages
● Threading for concurrent operations
● Error handling for connection issues
User Interface Components
Authentication Pages
Main Chat Interface
Sidebar Features
Frontend-Backend Communication
Error Handling
Connection Errors

● WebSocket disconnection recovery
● API request failure handling
● Session expiration management

User Input Validation
● Form input validation
● Empty message handling
● File download verification

Session Management
● Token expiration handling
● Automatic logout on session timeout
● Secure session cleanup

Setup Instructions
Environment Setup
pip install streamlit
pip install websockets
pip install requests

Configuration
FASTAPI_URL = "http://127.0.0.1:8000"
WEBSOCKET_URL = "ws://127.0.0.1:8000/ws"

Running the Application
streamlit run frontend.py

User Guide
Getting Started
1. Navigate to the application URL
2. Register a new account or log in
3. Start chatting with the AI
Using the Chat
● Type messages in the input box
● View real-time responses
● Download chat history as needed
● Reset chat to clear history
Managing Sessions
● Use the logout button to end session
● Session automatically expires after inactivity
● Refresh page to reconnect if needed
Security Features
● Secure password handling
● Token-based authentication
● WebSocket connection security
● Session state management
● Input sanitization
Performance Considerations
● Message queuing for smooth operation
● Asynchronous WebSocket handling
● Efficient state management
● Optimized UI updates
● Connection pooling
Known Limitations
● Single server connection
● Limited offline capabilities
● Basic error recovery
● Simple session management
Note :
I attempted to launch my chatbot using Streamlit Community Cloud, but since Ollama
is not supported there, I had to set up a backend on Render. However, the free tier of
Render comes with limitations, which led me to experiment with smaller models such
as TinyLlama, Mistral, and Gemma:2B. Despite these efforts, I was still unable to
successfully host the chatbot. I have attached the link to the GitHub repository, where
my commits document the various attempts I made.
Github Link : https://github.com/thegupta1694/chatbot


