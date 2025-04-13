# Huato - Telegram Chatbot with RAG

A Python-based Telegram chatbot that uses Retrieval-Augmented Generation (RAG) for enhanced responses.

## Features

- FastAPI web server
- Telegram bot integration
- PostgreSQL database
- RAG capabilities for improved responses

## Deployment on Railway

1. **Prerequisites**
   - Railway account
   - Telegram bot token

2. **Environment Variables**
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `DATABASE_URL`: Automatically provided by Railway
   - `PORT`: Automatically set by Railway

3. **Deployment Steps**
   - Create a new project on Railway
   - Connect your GitHub repository
   - Add a PostgreSQL database
   - Set the required environment variables
   - Deploy!

## Local Development

1. **Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file with:
   ```
   TELEGRAM_TOKEN=your_token_here
   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
   ```

3. **Run**
   ```bash
   python -m app.main
   ```

## Project Structure

```
.
├── app/
│   ├── main.py           # Application entry point
│   ├── config/           # Configuration files
│   ├── handlers/         # API and Telegram handlers
│   ├── models/           # Database models
│   └── services/         # Business logic
├── requirements.txt      # Python dependencies
├── Procfile             # Railway process file
├── runtime.txt          # Python version
└── Dockerfile           # Container configuration
```

## License

MIT 