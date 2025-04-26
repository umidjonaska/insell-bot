import os

USER_SETTINGS_FILE = "user_settings.txt"

def set_user_report_time(user_id, hour, minute):
    try:
        # Fayldan mavjud foydalanuvchilarni o'qib olish
        settings = []
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = file.readlines()

        # Yangi faylga yozish (yangi ma'lumotni yangilash yoki qo'shish)
        user_found = False
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as file:
            for line in settings:
                if line.startswith(str(user_id)):
                    file.write(f"{user_id},{hour},{minute}\n")
                    user_found = True
                else:
                    file.write(line)
            if not user_found:
                file.write(f"{user_id},{hour},{minute}\n")

        print(f"✅ {user_id} uchun vaqt sozlandi: {hour}:{minute}")

    except Exception as e:
        print(f"❌ Sozlamalarni saqlashda xato: {e}")
