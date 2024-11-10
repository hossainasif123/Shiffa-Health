import requests
from django.conf import settings
from datetime import datetime

DAILY_BASE_URL = "https://api.daily.co/v1/"

def create_daily_room(room_name=None):
    if not room_name:
        room_name = f"room-{datetime.now().strftime('%Y%m%d%H%M%S')}"  # Unique name with timestamp
    url = f"{DAILY_BASE_URL}rooms"
    headers = {
        "Authorization": f"Bearer {settings.DAILY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "name": room_name,
        "privacy": "public",
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error creating room:", response.status_code, response.text)  # Debug info
        return None


def create_host_token(room_name):
    url = f"{DAILY_BASE_URL}meeting-tokens"
    headers = {
        "Authorization": f"Bearer {settings.DAILY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "properties": {
            "room_name": room_name,
            "is_owner": True,  # This makes the token for the host with elevated permissions
        }
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("token")  # Return only the token string
    else:
        print("Error creating host token:", response.status_code, response.text)  # Debug info
        return None

def end_daily_room(room_name):
    url = f"{DAILY_BASE_URL}rooms/{room_name}"
    headers = {
        "Authorization": f"Bearer {settings.DAILY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return True  # Successfully ended the room
    else:
        print("Error ending room:", response.status_code, response.text)  # Debug info
        return False
