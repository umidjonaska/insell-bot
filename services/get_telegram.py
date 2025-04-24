import aiohttp

async def get_telegram_id():
    url = "https://demo.api-insell.uz/get_users_for_telegram/"
    print(f"Yuborilayotgan URL: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
