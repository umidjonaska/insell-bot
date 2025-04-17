"""Asosiy yozilgan funksiya"""
import requests

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from datetime import date
from pprint import pprint as print

def get_kassa():

    url =f"https://demo.api-insell.uz/get_statistics_for_bot/kassa/1111/?from_time={date.today()}&to_time={date.today()}"
    r = requests.get(url)

    res = r.json()
    data = res['data'][0]['items']
    return data

def generate_pdf(logo_path=None):
    filename = f"hisobot_kassa_{date.today()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logotip (yuqori o‘ng burchakda)
    if logo_path:
        elements.append(Spacer(1, -20))  # manfiy spacer – logoni yuqoriroq suradi
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))  # logodan keyin kichik masofa

    # Sana va umumiy summa
    elements.append(Paragraph(f"Sana: {date.today()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    #Mahsulotlar umumiy summasi keladi
    elements.append(Paragraph("<b><font color='#ff6a2c'>Mahsulotlar: 2 650 234 so’m.</font></b>", styles['Normal']))
    elements.append(Spacer(1, 12))

    jadval_data = [
    ['T/R', 'Kassa', 'Kun boshi', 'Kirim', 'Chiqim', 'Qoldiq'],]

    # get_kassa() funksiyasidan ma'lumot olish
    li = get_kassa()
    lis = []

    for item in li:
        for k, v in item.items():
            if k == 'currency' or k == 'kirim_transferdan' or k == 'chiqim_transferdan':
                continue
            elif type(v) == float:
                lis.append(f"{int(v)} so'm")
            elif k == 'name':
                lis.append(v.title())
            else:
                lis.append(v)

    # Raqamli qatorni birinchi qatorning raqamiga qo'shish
    raqam = str(len(jadval_data))  # Har bir yangi qator uchun raqamni avtomatik hisoblash
    lis.insert(0, raqam)  # Raqamni boshida qo'shamiz

    # Yangi qatorni jadvalga qo'shamiz
    jadval_data.append(lis)

    table = Table(jadval_data, colWidths=[30, 100, 100, 100, 100, 100,])
    table.setStyle(TableStyle([
        # Sarlavha
        ('BACKGROUND', (0, 0), (-1, 0), '#ff6a2c'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),

        # Jadval chiziqlari va joylashuv
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    doc.build(elements)
    return filename

# PDF faylni yaratish
pdf = generate_pdf("insell.png")
print(f"PDF tayyor: {pdf}")
