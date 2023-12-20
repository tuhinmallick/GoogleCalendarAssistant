import requests
import json
from datetime import datetime, timedelta
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dependencies import get_db


def get_calendar_events(user_email, calendar_id, start_time, end_time):
    db = get_db()
    if user := db.users.find_one({"email": user_email}):
        access_token = user.get("access_token")

        # Create the API endpoint
        endpoint = (
            f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        )

        # Set the parameters
        params = {
            "timeMin": start_time,
            "timeMax": end_time,
        }

        # Set the headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        # Make the request
        response = requests.get(endpoint, headers=headers, params=params)
        events = response.json()

        # List the events
        event_list = []
        for event in events.get("items", []):
            start = event.get("start")
            date_info = start.get("date", start.get("dateTime"))
            event_list.append(f"{event.get('summary')}: {date_info}")

    return event_list


def get_calendar_timezone(user_email, calendar_id):
    db = get_db()
    if user := db.users.find_one({"email": user_email}):
        access_token = user.get("access_token")

        # Google Calendar API endpoint to get calendar details
        endpoint = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        response = requests.get(endpoint, headers=headers)
        calendar_details = response.json()

        # Extract the time zone from the calendar details
        time_zone = calendar_details.get("timeZone")

    return time_zone


def create_event(user_email, calendar_id, event_name, start_datetime, end_datetime):
    db = get_db()
    user = db.users.find_one({"email": user_email})

    timezone = get_calendar_timezone(user_email, calendar_id)

    if user:
        access_token = user.get("access_token")

        endpoint = (
            f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Create the event data
        event_data = {
            "summary": f"{event_name} (created by Calvin)",
            "start": {
                "dateTime": start_datetime,
                "timeZone": timezone,  # Replace with your time zone, e.g., "America/New_York"
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": timezone,  # Replace with your time zone
            },
        }

        response = requests.post(endpoint, headers=headers, json=event_data)
        return response.json()
