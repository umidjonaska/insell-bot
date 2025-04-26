import requests
from datetime import date
from pprint import pprint as print
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet


def get_kassa(telegram_id):
    url = (
        f"https://demo.api-insell.uz/get_statistics_for_bot/kassa/"
        f"{telegram_id}/?from_time={date.today()}&to_time={date.today()}"
    )
    print(f"Yuborilayotgan URL: {url}")
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    res = r.json()
    return res['data'][0]['items']

def kassa_pdf(telegram_id, category_id=0, logo_path=None):
    filename = f"hisobot_kassa_{telegram_id}_{date.today()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logotip
    if logo_path:
        elements.append(Spacer(1, -20))
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))

    elements.append(Paragraph(f"Sana: {date.today()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    jadval_data = [['T/R', 'Kassa', 'Kun boshi', 'Kirim', 'Chiqim', 'Qoldiq']]

    try:
        li = get_kassa(telegram_id)
    except Exception as e:
        print(f"API dan ma’lumot olishda xato: {e}")
        return ""

    total_kirim = 0
    total_qoldiq = 0
    currency = li[0].get('currency', 'so‘m') if li else 'so‘m'

    for idx, item in enumerate(li, 1):
        currency = item.get('currency', 'so‘m')
        row = [str(idx)]

        for k in ['name', 'kassa_qoldiq_kun_boshi', 'kirim', 'chiqim', 'balance']:
            v = item.get(k, 0.0)
            if k == 'name':
                row.append(v.title())
            elif isinstance(v, float):
                if k == 'kirim':
                    total_kirim += v
                elif k == 'balance':
                    total_qoldiq += v
                formatted = f"{int(v):,}".replace(",", " ")
                row.append(f"{formatted} {currency}")
            else:
                row.append(str(v))
        jadval_data.append(row)

    formatted_qoldiq = f"{int(total_qoldiq):,}".replace(',', ' ')
    elements.append(
        Paragraph(
            f"<b><font color='#ff6a2c'>Umumiy qoldiq: {formatted_qoldiq} {currency}.</font></b>",
            styles['Normal']
        )
    )
    elements.append(Spacer(1, 12))

    table = Table(jadval_data, colWidths=[30, 100, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#ff6a2c'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))
    doc.build(elements)
    return filename
