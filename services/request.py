import requests as r
#from config import BASE_URL
BASE_URL="https://demo.api-insell.uz/get_statistics_for_bot/daily/6723446768/?from_time=2025-03-25&to_time=2025-03-25"
def fetch_report_data():
    try:
        response = r.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        print(f"API xatosi: {response.status_code}")
    except Exception as e:
        print(f"API so‘rov xatosi: {e}")
    return None