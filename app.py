"""
Basic Flask Application for Twilio WhatsApp Webhook
===================================================

Setup instructions for environment variables:
1. Ensure `python-dotenv` is installed (it's in your requirements.txt).
2. Create a file named `.env` in the root directory of your project.
3. Add your environment variables to the `.env` file, for example:
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   GEMINI_API_KEY=your_gemini_API_key_here
4. The `load_dotenv()` function below will automatically read these variables
   so they can be accessed in your code via `os.environ.get('VARIABLE_NAME')` or `os.getenv('VARIABLE_NAME')`.
"""

import os
import logging
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse incoming form data from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')

        if not incoming_msg and not sender_number:
            logger.warning("Received an empty request or missing Twilio form fields.")

        logger.info(f"Received message: '{incoming_msg}' from {sender_number}")

        # Create a Twilio MessagingResponse object
        resp = MessagingResponse()
        msg = resp.message()

        # Echo back the exact text sent by the user
        if incoming_msg:
            msg.body(incoming_msg)
        else:
            msg.body("I didn't receive any text!")

        return str(resp)

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        # Still return a valid TwiML response to Twilio so it doesnt break on their end
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an internal error while processing your request.")
        # We can return an error string with a 500 status code
        return str(resp), 500

if __name__ == '__main__':
    # Run the Flask app
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
