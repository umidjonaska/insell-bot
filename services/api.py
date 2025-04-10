import requests
from config import BASE_URL

def fetch_report_data():
    try:
        r = requests.get("https://demo.api-insell.uz/get_statistics_for_bot/daily/6723446768/?from_time=2025-03-25&to_time=2025-03-25")
        if r.status_code == 200:
            print(r.json())
            return r.json()
        print(r.text)
        print(f"API xatosi: {r.status_code}")
    except Exception as e:
        print(f"API so‘rov xatosi: {e}")
    return None
