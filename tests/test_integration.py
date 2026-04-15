import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
import app as app_module

# Mock ai_parser and scheduler for integration testing
def mock_parse_intent(text):
    return {
        "intent": "set_reminder",
        "task": "call Mom",
        "datetime": "2026-04-16T18:00:00+05:30",
        "recurrence": None
    }
app_module.parse_intent = mock_parse_intent

def mock_schedule_reminder(task_text, target_time, to_number):
    print(f"Mock scheduled reminder '{task_text}' for {target_time} to {to_number}")
    return "mock_job_id"
app_module.scheduler.schedule_reminder = mock_schedule_reminder

data = {
    'From': '+1234567890',
    'Body': 'Remind me to call Mom tomorrow at 6 PM'
}

with app.test_client() as client:
    response = client.post('/webhook', data=data)
    print("Response from server:")
    print(response.data.decode('utf-8'))
