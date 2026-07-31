"""
Backend package for AI Chat Assistant.

This package contains modules for LLM integration and other backend services.
"""

from backend.llm import (
    GeminiClient,
    create_gemini_client,
    validate_user_input,
    Message
)

__all__ = [
    "GeminiClient",
    "create_gemini_client", 
    "validate_user_input",
    "Message"
]
