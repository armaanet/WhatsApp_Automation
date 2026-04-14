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

import db_ops
from ai_parser import parse_intent

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
            return str(MessagingResponse())

        logger.info(f"Received message: '{incoming_msg}' from {sender_number}")

        # 1. Register or get user
        user_id = db_ops.add_user(sender_number)
        
        # Create a Twilio MessagingResponse object
        resp = MessagingResponse()
        msg = resp.message()

        if not user_id:
            msg.body("Sorry, there was an issue verifying your account.")
            return str(resp)

        # 2. Parse Intent with Gemini
        parsed_data = parse_intent(incoming_msg)

        if not parsed_data:
            msg.body("I had trouble understanding that. Could you rephrase your request?")
            return str(resp)

        intent = parsed_data.get('intent')
        task = parsed_data.get('task')
        dt = parsed_data.get('datetime')
        recurrence = parsed_data.get('recurrence')

        # 3. Route logic based on intent
        if intent == "set_reminder":
            if not dt:
                msg.body(f"Got it. What time would you like to be reminded about '{task}'?")
            else:
                reminder_id = db_ops.insert_reminder(user_id, task, dt, recurrence)
                if reminder_id:
                    msg.body(f"Done! I've set a reminder for '{task}'.")
                else:
                    msg.body("Sorry, I couldn't save that reminder due to a database error.")
        elif intent == "get_tasks":
            # Pass the user_id to ensure we only get tasks for the sender
            tasks = db_ops.get_active_tasks(user_id=user_id)
            if tasks:
                tasks_text = "\n".join([f"- {t['task']} at {t['datetime']}" for t in tasks])
                msg.body(f"Here are your active tasks:\n{tasks_text}")
            else:
                msg.body("You have no pending tasks right now.")
        else:
            msg.body("I'm not sure how to handle that intent yet. Try asking me to set a reminder!")

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
