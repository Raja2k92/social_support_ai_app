# -------------------------------
# Stage 1: Base Python environment
# -------------------------------
FROM python:3.11-slim

# Set working directory (adjusted for your layout)
WORKDIR /social_support_ai

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV PYTHONPATH=/social_support_ai \
    STREAMLIT_PORT=8501 \
    OLLAMA_BASE=http://host.docker.internal:11434 \
    OLLAMA_MODEL=gemma3:4b \
    USE_LOCAL_LLM=true

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "ui/chat_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
