# WhatsApp AI Assistant

A Python-based AI Assistant for WhatsApp.

## Technologies Used
- **Flask**: Web framework to handle incoming webhooks from Twilio.
- **Twilio**: API service connecting the application to WhatsApp.
- **Gemini (google-generativeai)**: AI model backend for generating intelligent responses.
- **APScheduler**: Task scheduling library to run background jobs or delayed messages.
- **SQLite3**: Lightweight, built-in database to manage state, users, and conversational history.

## Getting Started
1. Clone this repository.
2. Set up a virtual environment and install the requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
3. Set your environment variables in a `.env` file (e.g., Twilio credentials, Gemini API key).
4. Run the Flask application to start the development server.
