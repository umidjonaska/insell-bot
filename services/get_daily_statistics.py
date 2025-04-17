# import requests
# from datetime import date
# from config import BASE_URL

# def fetch_report_data():
#     #response = requests.get(f"{BASE_URL}/get_statistics_for_bot/daily/6723446768/?from_time={date.today()}&to_time={date.today()}")
#     response = requests.get(f"{BASE_URL}/get_statistics_for_bot/daily/6723446768/?from_time=2025-03-25&to_time=2025-03-25")
#     if response.status_code == 200:
#         print(response.json())
#         return response.json()
#     print(f"API xatosi: {response.text}")
#     return response.json()