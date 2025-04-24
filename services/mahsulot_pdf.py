"""Mahsulot hisoboti dinamic"""

import requests
from datetime import date
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Unicode shriftni ulash
pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))  # Shrift fayli mavjud bo'lishi kerak

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Unicode', fontName='DejaVu', fontSize=10))
styles.add(ParagraphStyle(name='WrapLeft', fontName='DejaVu', fontSize=8, alignment=0))  # TA_LEFT = 0

def get_category(telegram_id):
    # 1. telegram_id f-string bilan qo'shildi
    url = f"https://demo.api-insell.uz/get_categories_for_bot/{telegram_id}/"
    print(f"Requesting URL (categories): {url}")

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # HTTP xatolikni istisno qilish uchun
        data = res.json().get('data', [])

        categories = []
        for branch_data in data:
            items = branch_data.get('items')
            if items:
                # Agar 'items' mavjud bo'lsa, ularning ichidan kategoriya id/nomini olish
                for item in items:
                    categories.append((item['category_id'], item['category_name']))
            else:
                # Aks holda, branch_data o'zi kategoriya obyekti deb qaraymiz
                # (Agar API shunga mos tuzilgan bo'lsa)
                cat_id = branch_data.get('category_id')
                cat_name = branch_data.get('category_name')
                if cat_id and cat_name:
                    categories.append((cat_id, cat_name))

        return categories
    except Exception as e:
        print(f"Kategoriya olishda nomaʼlum xatolik: {e}")

def get_mahsulot(telegram_id):
    base_url = f"https://demo.api-insell.uz/get_statistics_for_bot/mahsulot_hisoboti/{telegram_id}/"
    category_data = {}
    branch = None

    for cat_id, cat_name in get_category(telegram_id):
        params = {
            "from_time": date.today(),
            "to_time": date.today(),
            "category_id": cat_id
        }
        # Quriladigan so‘rov to‘liq URL’sini olish uchun:
        full_url = requests.Request('GET', base_url, params=params).prepare().url
        #print(f"Requesting URL (statistics) for '{cat_name}': {full_url}")

        try:
            res = requests.get(base_url, params=params, timeout=10).json()
            if res.get('data'):
                data_block = res['data'][0]
                if not branch:
                    branch = data_block.get('branch')
                items = data_block.get('items', [])
                if items:
                    category_data[cat_name] = items
        except Exception as e:
            print(f"{cat_name} uchun ma'lumotda xatolik: {e}")

    return {
        "branch": branch or "Filial nomi aniqlanmadi",
        "categories": category_data
    }

def mahsulot_pdf(telegram_id, logo_path=None):
    mahsulotlar = get_mahsulot(telegram_id)
    doc_path = f"mahsulot_hisobot_{date.today()}.pdf"
    doc = SimpleDocTemplate(doc_path, pagesize=A4)
    elements = []

    heading = ParagraphStyle(name="Heading", fontName='DejaVu', fontSize=10, leading=24, alignment=TA_CENTER)

    elements.append(Spacer(1, -60))
    branch_name = Paragraph(f"<b>{mahsulotlar['branch']}</b>", heading)
    elements.append(branch_name)
    elements.append(Spacer(1, 4))

    if logo_path:
        elements.append(Spacer(1, -20))
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))

    elements.append(Paragraph(f"Sana: {date.today()}", styles['Unicode']))
    elements.append(Spacer(1, 12))

    umumiy_summa = 0
    for items in mahsulotlar['categories'].values():
        for item in items:
            try:
                umumiy_summa += int(float(item.get('summa', 0)))
            except:
                pass

    elements.append(Paragraph(
        f"<b><font size=14 color='#ff6a2c'>Mahsulotlar: {umumiy_summa:,} so’m.</font></b>",
        styles['Unicode']
    ))
    elements.append(Spacer(1, 10))

    for category_name, items in mahsulotlar["categories"].items():
        kategoriya_summa = sum([int(float(i.get("summa", 0))) for i in items])
        kategoriya_soni = len(items)

        kategoriya_sarlavha = f"{category_name} : {kategoriya_summa:,} so’m, {kategoriya_soni} xil"
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<font color='black'><b>{kategoriya_sarlavha}</b></font>", styles['Unicode']))
        elements.append(Spacer(1, 4))

        table_data = [[
            "T/R", "Mahsulot", "Kun boshi", "Keldi", "Sotildi",
            "Qoldiq", "Narx", "Summa"
        ]]

        for idx, item in enumerate(items, start=1):
            mahsulot_nomi = Paragraph(item.get('nomi', ''), styles['WrapLeft'])
            table_data.append([
                idx,
                mahsulot_nomi,
                item.get('kun_boshi', 0),
                item.get('keldi', 0),
                item.get('sotildi', 0),
                f"{int(float(item.get('qoldiq', 0))):,}",
                f"{int(float(item.get('narx', 0))):,}",
                f"{int(float(item.get('summa', 0))):,}"
            ])

        table = Table(table_data, repeatRows=1, colWidths=[30, 150, 50, 50, 50, 50, 50, 70])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#ff6a2c'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "<font size=8>Ma'lumotlar insell savdo dasturi yordamida tayyorlandi. "
        "Murojaat uchun: insell.uz +998 33 569 0901</font>", styles['Unicode']
    ))

    doc.build(elements)
    return doc_path