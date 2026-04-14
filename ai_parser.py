import os
import json
import logging
from datetime import datetime
import pytz
import google.generativeai as genai

# Setup basic logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def parse_intent(user_text):
    """
    Parses user text to extract intent, task details, datetime, and recurrence
    using the Gemini API, strictly outputting JSON.
    """
    try:
        # Get current time in Asia/Kolkata for relative time context
        tz = pytz.timezone('Asia/Kolkata')
        current_time_str = datetime.now(tz).isoformat()

        system_instruction = f"""
        You are a strict JSON parser. Analyze the user's text and extract the request details. 
        Output ONLY valid JSON. Do not include markdown code blocks, backticks, or conversational text.
        
        The current date and time context for relative times is: {current_time_str} (Asia/Kolkata timezone).
        
        The JSON output must have EXACTLY the following keys:
        - "intent": string (e.g., "set_reminder", "get_tasks", "cancel_reminder", "other")
        - "task": string (the core description of the task without time/recurrence words)
        - "datetime": string (in ISO 8601 format, STRICTLY in the Asia/Kolkata timezone). If no date/time is specified, use null.
        - "recurrence": string or null. MUST be exactly one of "daily", "weekly", "monthly", or null.
        """

        # Configure the model to mandate JSON output
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.0,
            )
        )
        
        # Generate the response from the user text
        response = model.generate_content(user_text)
        
        # Attempt to parse the response as JSON
        if response.text:
            return json.loads(response.text)
        else:
            logger.error("Gemini API returned an empty response.")
            return None
            
    except json.JSONDecodeError as json_err:
        logger.error(f"Failed to parse Gemini response as JSON: {json_err}. Raw text: {response.text}")
        return None
    except Exception as e:
        logger.error(f"Error during Gemini API call: {e}")
        return None
