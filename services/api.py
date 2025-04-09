import requests
from config import BASE_URL

def fetch_report_data():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        print(f"API xatosi: {response.status_code}")
    except Exception as e:
        print(f"API so‘rov xatosi: {e}")
    return None
