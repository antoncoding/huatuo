# Local RAG Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot that uses your local text files as a knowledge base, powered by OpenAI's GPT-4.

## Setup

1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a directory for your text files:
```bash
mkdir text_files
```

3. Copy your text files into the `text_files` directory.

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```
Or create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python rag_chatbot.py
```

2. The server will start on `http://localhost:8000`

3. You can query the chatbot using curl or any HTTP client:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Your question here"}'
```

## How it Works

1. The system loads all text files from the specified directory
2. Documents are split into chunks for better retrieval
3. Text is converted to embeddings using OpenAI's embedding model
4. Vectors are stored in a local Chroma database
5. When you query, the system:
   - Finds relevant chunks from your documents
   - Uses them as context for GPT-4
   - Returns an answer based on your documents

## Notes

- The system uses OpenAI's embedding model for vectorization
- The LLM used is GPT-4 Turbo
- All data is stored locally in the `db` directory
- You'll need an OpenAI API key with access to GPT-4 