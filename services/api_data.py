# import requests
# from datetime import date

# """Category APIdan ma'lumot olish"""
# def get_category():
#     li = []
#     url = f"https://demo.api-insell.uz/get_categories_for_bot/1111/"
#     r = requests.get(url)
#     res = r.json()
#     data = res['data']
#     for item in data:
#         li.append(item['category_id'])
#     return li

# """Category va mahsulot birga qo'llanilishi kerak"""

# """Mahsulot APIdan ma'lumot olish"""
# category = get_category()
# def get_mahsulot():
#     url = f"https://demo.api-insell.uz/get_statistics_for_bot/mahsulot_hisoboti/1111/"
#     category_data = {}

#     for i in category:
#         params = {
#             "from_time": "2025-04-14",
#             "to_time": "2025-04-14",
#             "category_id": i
#         }

#         r = requests.get(url, params=params)
#         res = r.json()
#         data = res['data'][0]['items']

#         if data:  # agar bo‘sh bo‘lmasa
#             category_name = data[0]['kategoriya']  # birinchi itemdan kategoriya nomini olamiz
#             category_data[category_name] = data

#     return category_data

# """Kassa APIdan ma'lumot olish"""
# def get_kassa():

#     url ="https://demo.api-insell.uz/get_statistics_for_bot/kassa/1111/?from_time=2025-04-01&to_time=2025-04-09"
#     r = requests.get(url)

#     res = r.json()
#     data = res['data'][0]['items']
#     return data

# """Nasiya APIdan ma'lumot olish"""
# def get_nasiya():
#     url = f"https://demo.api-insell.uz/get_statistics_for_bot/nasiya/1111/?from_time={date.today()}&to_time={date.today()}"
#     r = requests.get(url)
#     res = r.json()
#     return res['data'][0]['muddati_kelgan']

# """Umumiy_hisobot APIdan ma'lumot olish"""
# def get_umumiy():
#     url = f"https://demo.api-insell.uz/get_statistics_for_bot/umumiy_hisobot/1111/?from_time=2025-04-01&to_time=2025-04-09"
#     r = requests.get(url)
#     res = r.json()
#     data = res['data'][0]

#     return data