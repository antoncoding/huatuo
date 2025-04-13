FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for text files if it doesn't exist
RUN mkdir -p text_files

# Create a directory for the vector database
RUN mkdir -p db

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "rag_chatbot:app", "--host", "0.0.0.0", "--port", "8000"] 