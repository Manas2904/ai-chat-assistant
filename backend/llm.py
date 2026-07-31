"""
LLM module for Gemini AI integration.

This module handles all interactions with the Google Gemini API, including
client initialization, response generation, and error handling. It provides
a clean interface for the Streamlit UI to interact with AI capabilities.
"""

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Message:
    """
    Represents a chat message with role and content.
    
    Attributes:
        role: The role of the message sender ('user' or 'assistant')
        content: The text content of the message
    """
    role: str
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert the message to a dictionary format."""
        return {"role": self.role, "content": self.content}
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        """Create a Message instance from a dictionary."""
        return cls(role=data["role"], content=data["content"])


class GeminiClient:
    """
    Client for interacting with Google Gemini AI API.
    
    This class handles API authentication, request formatting, and response
    generation with proper error handling and logging.
    
    Attributes:
        client: The underlying Google GenAI client instance
        model: The Gemini model to use for generating responses
        api_key_configured: Boolean indicating if API key is properly configured
    """
    
    DEFAULT_MODEL: str = "models/gemini-flash-latest"
    API_KEY_ENV_VAR: str = "GOOGLE_API_KEY"
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Optional API key. If not provided, will load from environment
            model: Optional model name. Defaults to DEFAULT_MODEL
            
        Raises:
            ValueError: If API key is not found or invalid
        """
        self.model = model or self.DEFAULT_MODEL
        self.api_key_configured = False
        
        try:
            self.client = self._initialize_client(api_key)
            self.api_key_configured = True
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def _initialize_client(self, api_key: Optional[str] = None) -> genai.Client:
        """
        Initialize the underlying Google GenAI client.
        
        Args:
            api_key: Optional API key. If not provided, loads from environment
            
        Returns:
            Configured genai.Client instance
            
        Raises:
            ValueError: If API key is not found or invalid
        """
        # Load environment variables if no API key provided
        if not api_key:
            load_dotenv()
            api_key = os.getenv(self.API_KEY_ENV_VAR)
        
        # Validate API key
        if not api_key or api_key == "your_google_api_key_here":
            error_msg = (
                f"Google API key not found. Please set {self.API_KEY_ENV_VAR} "
                f"in .env file or pass it directly."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            client = genai.Client(api_key=api_key)
            logger.debug("GenAI client created successfully")
            return client
        except Exception as e:
            error_msg = f"Failed to create GenAI client: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _format_conversation_history(
        self, 
        conversation_history: List[Dict[str, str]]
    ) -> List[types.Content]:
        """
        Format conversation history for Gemini API consumption.
        
        Args:
            conversation_history: List of message dictionaries with 'role' and 'content'
            
        Returns:
            List of formatted Content objects for the Gemini API
        """
        contents = []
        
        for msg in conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            content = types.Content(
                parts=[types.Part(text=msg["content"])],
                role=role
            )
            contents.append(content)
            logger.debug(f"Formatted message: role={role}, content_length={len(msg['content'])}")
        
        return contents
    
    def _handle_api_error(self, error: Exception) -> None:
        """
        Handle and classify API errors into appropriate exception types.
        
        Args:
            error: The original exception from the API call
            
        Raises:
            ValueError: For API key issues, rate limits, and API errors
            ConnectionError: For network-related failures
        """
        error_msg = str(error).lower()
        logger.error(f"API error occurred: {error_msg}")
        
        # Classify error types
        if any(keyword in error_msg for keyword in ["api key", "authentication", "unauthorized"]):
            raise ValueError(
                "Invalid API key. Please check your GOOGLE_API_KEY in .env file."
            )
        elif any(keyword in error_msg for keyword in ["quota", "rate limit", "429"]):
            raise ValueError(
                "Rate limit exceeded. Please wait a moment and try again."
            )
        elif any(keyword in error_msg for keyword in ["network", "connection", "timeout"]):
            raise ConnectionError(
                "Network error. Please check your internet connection and try again."
            )
        else:
            raise ValueError(f"Error generating response: {str(error)}")
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response from Gemini AI based on user input and conversation history.
        
        Args:
            user_message: The user's current message
            conversation_history: Optional list of previous messages for context
            
        Returns:
            Generated AI response text
            
        Raises:
            ValueError: For invalid API keys, rate limits, or other API errors
            ConnectionError: For network-related failures
            ValueError: If user_message is empty or only whitespace
        """
        # Validate input
        if not user_message or not user_message.strip():
            error_msg = "User message cannot be empty"
            logger.warning(error_msg)
            raise ValueError(error_msg)
        
        conversation_history = conversation_history or []
        logger.info(f"Generating response for message: {user_message[:50]}...")
        
        try:
            # Build conversation context for Gemini
            contents = self._format_conversation_history(conversation_history)
            
            # Add current user message
            contents.append(
                types.Content(
                    parts=[types.Part(text=user_message)],
                    role="user"
                )
            )
            
            logger.debug(f"Sending request to Gemini with {len(contents)} messages")
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            logger.info("Response generated successfully")
            return response.text
            
            logger.info("Response generated successfully")
            return response.text
            
        except Exception as e:
            self._handle_api_error(e)
    
    def is_configured(self) -> bool:
        """
        Check if the client is properly configured with a valid API key.
        
        Returns:
            True if API key is configured and valid, False otherwise
        """
        return self.api_key_configured
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current configuration.
        
        Returns:
            Dictionary containing configuration details
        """
        return {
            "model": self.model,
            "api_key_configured": self.api_key_configured,
            "api_key_env_var": self.API_KEY_ENV_VAR
        }


def create_gemini_client(
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> GeminiClient:
    """
    Factory function to create a Gemini client with optional configuration.
    
    Args:
        api_key: Optional API key. If not provided, loads from environment
        model: Optional model name. Defaults to gemini-2.0-flash-exp
        
    Returns:
        Configured GeminiClient instance
        
    Raises:
        ValueError: If API key is not found or invalid
    """
    logger.info("Creating Gemini client")
    return GeminiClient(api_key=api_key, model=model)


def validate_user_input(user_input: str) -> bool:
    """
    Validate user input before sending to the API.
    
    Args:
        user_input: The user's message to validate
        
    Returns:
        True if input is valid, False otherwise
    """
    if not user_input or not user_input.strip():
        logger.warning("Empty user input received")
        return False
    return True
