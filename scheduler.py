import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
import pytz

# Configure the scheduler for the Asia/Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')
scheduler = BackgroundScheduler(timezone=kolkata_tz)
# Start the scheduler
scheduler.start()

def send_whatsapp_message(to_number: str, text: str):
    """
    Sends a WhatsApp message using the standard Twilio REST API client.
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')  # Format: 'whatsapp:+1234567890'

    if not all([account_sid, auth_token, from_number]):
        print("Error: Twilio credentials not fully set in environment variables.")
        return

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Ensure the to_number is in the correct format for WhatsApp
    recipient = f"whatsapp:{to_number}" if not to_number.startswith("whatsapp:") else to_number

    try:
        message = client.messages.create(
            body=text,
            from_=from_number,
            to=recipient
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def schedule_reminder(task_text: str, target_time: datetime, to_number: str):
    """
    Adds a job to the BackgroundScheduler to execute `send_whatsapp_message`
    at the specified `target_time`.
    """
    try:
        job = scheduler.add_job(
            send_whatsapp_message,
            trigger='date',
            run_date=target_time,
            args=[to_number, task_text]
        )
        print(f"Reminder scheduled successfully. Job ID: {job.id} at {target_time}")
        return job.id
    except Exception as e:
        print(f"Failed to schedule reminder: {e}")
        return None
