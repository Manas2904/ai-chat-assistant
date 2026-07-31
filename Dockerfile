# ============================================================================
# AI Chat Assistant - Dockerfile
# ============================================================================
# Production-ready Docker configuration for containerized deployment
# ============================================================================

# Use Python 3.11 slim image for smaller size and security
FROM python:3.11-slim

# Set metadata
LABEL maintainer="your-email@example.com"
LABEL description="AI Chat Assistant with Streamlit and Google Gemini API"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Create a non-root user for security
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY app.py .
COPY backend/ ./backend/

# Create necessary directories and set permissions
RUN mkdir -p /app/.streamlit && \
    chown -R streamlit:streamlit /app

# Switch to non-root user
USER streamlit

# Expose Streamlit default port
EXPOSE 8501

# Health check to ensure the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# ============================================================================
# Build Instructions
# ============================================================================
# Build the Docker image:
#   docker build -t ai-chat-assistant .
#
# Run the container:
#   docker run -p 8501:8501 --env-file .env ai-chat-assistant
#
# Run with volume for development:
#   docker run -p 8501:8501 --env-file .env -v $(pwd):/app ai-chat-assistant
#
# Using Docker Compose:
#   docker-compose up
# ============================================================================
