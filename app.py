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
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse incoming form data from Twilio
    incoming_msg = request.values.get('Body', '').strip()
    sender_number = request.values.get('From', '')

    print(f"Received message: '{incoming_msg}' from {sender_number}")

    # Create a Twilio MessagingResponse object
    resp = MessagingResponse()
    msg = resp.message()

    # Echo back the exact text sent by the user
    if incoming_msg:
        msg.body(incoming_msg)
    else:
        msg.body("I didn't receive any text!")

    # Return the TwiML response as a string, which Twilio expects
    return str(resp)

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
