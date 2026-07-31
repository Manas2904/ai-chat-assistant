import streamlit as st
import logging
from typing import List, Dict
from backend.llm import GeminiClient, create_gemini_client, validate_user_input


# Configure logging for the UI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_session_state() -> None:
    """
    Initialize session state variables for the chat application.
    
    Sets up the necessary session state variables for maintaining chat history,
    typing status, and API configuration state across user interactions.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Initialized messages in session state")
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
        logger.info("Initialized is_typing in session state")
    
    if "api_key_configured" not in st.session_state:
        st.session_state.api_key_configured = False
        logger.info("Initialized api_key_configured in session state")


def render_sidebar(client: GeminiClient) -> None:
    """
    Render the sidebar with chat controls and information.
    
    Args:
        client: The Gemini client instance for checking API status
    """
    with st.sidebar:
        st.title("AI Chat Assistant")
        st.markdown("---")
        
        st.subheader("Chat Settings")
        
        # API Key Status
        if client.is_configured():
            st.success("✅ API Key Configured")
            logger.debug("API key status: configured")
        else:
            st.warning("⚠️ API Key Not Configured")
            logger.warning("API key status: not configured")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            logger.info("Chat cleared by user")
            st.rerun()
        
        st.markdown("---")
        
        # Chat statistics
        if st.session_state.messages:
            st.metric("Total Messages", len(st.session_state.messages))
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("Your Messages", user_messages)
            st.metric("AI Responses", len(st.session_state.messages) - user_messages)
            logger.debug(f"Chat stats - Total: {len(st.session_state.messages)}, User: {user_messages}")
        
        st.markdown("---")
        st.caption("Built with Streamlit")


def render_message(message: Dict[str, str]) -> None:
    """
    Render a single chat message with appropriate styling.
    
    Args:
        message: Dictionary containing 'role' and 'content' keys
    """
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    logger.debug(f"Rendered message: role={message['role']}, length={len(message['content'])}")


def render_typing_indicator() -> None:
    """
    Render a typing indicator animation.
    
    Displays a visual indicator to show the AI is processing the user's request.
    """
    with st.chat_message("assistant"):
        st.markdown("✨ *Thinking...*")
    logger.debug("Rendered typing indicator")


def handle_user_input(client: GeminiClient, user_input: str) -> None:
    """
    Handle user input and generate AI response using Gemini.
    
    This function validates the user input, manages the typing indicator,
    calls the Gemini API for response generation, and handles any errors
    that occur during the process.
    
    Args:
        client: Configured Gemini client instance
        user_input: The user's message text
    """
    # Validate input
    if not validate_user_input(user_input):
        st.error("Please enter a message.")
        logger.warning("Empty user input rejected")
        return
    
    # Add user message to chat history immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    logger.info(f"User message added: {user_input[:50]}...")
    
    # Show typing indicator
    st.session_state.is_typing = True
    placeholder = st.empty()
    with placeholder:
        render_typing_indicator()
    
    try:
        # Generate AI response using the Gemini client
        response = client.generate_response(
            user_message=user_input,
            conversation_history=st.session_state.messages[:-1]
        )
        
        # Clear typing indicator
        placeholder.empty()
        st.session_state.is_typing = False
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        logger.info(f"AI response generated: {response[:50]}...")
        
    except ValueError as e:
        placeholder.empty()
        st.session_state.is_typing = False
        st.error(f"API Error: {str(e)}")
        logger.error(f"ValueError in handle_user_input: {e}")
    except ConnectionError as e:
        placeholder.empty()
        st.session_state.is_typing = False
        st.error(f"Connection Error: {str(e)}")
        logger.error(f"ConnectionError in handle_user_input: {e}")
    except Exception as e:
        placeholder.empty()
        st.session_state.is_typing = False
        st.error(f"Unexpected error: {str(e)}")
        logger.error(f"Unexpected error in handle_user_input: {e}")


def render_chat_interface(client: GeminiClient) -> None:
    """
    Render the main chat interface with message history.
    
    Args:
        client: Configured Gemini client instance
    """
    st.title("Chat")
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.messages:
        render_message(message)
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        handle_user_input(client, user_input)
        st.rerun()


def main() -> None:
    """
    Main application entry point.
    
    Configures the Streamlit page, initializes session state and the Gemini client,
    and renders the UI components. Handles client initialization errors gracefully.
    """
    st.set_page_config(
        page_title="AI Chat Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize Gemini client
    try:
        client = create_gemini_client()
        st.session_state.api_key_configured = client.is_configured()
        logger.info("Gemini client initialized successfully in main")
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please add your Google API key to the .env file and restart the application.")
        logger.error(f"Failed to initialize Gemini client: {e}")
        st.stop()
    
    # Render UI components
    render_sidebar(client)
    render_chat_interface(client)


if __name__ == "__main__":
    main()
