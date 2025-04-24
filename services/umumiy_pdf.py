import requests
from pprint import pprint as print
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

def get_umumiy(telegram_id):
    url = f"https://demo.api-insell.uz/get_statistics_for_bot/umumiy_hisobot/{telegram_id}/?from_time={date.today()}&to_time={date.today()}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # HTTP status xatoliklarini aniqlash
        res = r.json()
        return res['data'][0] if 'data' in res else None
    except Exception as e:
        print(f"Xatolik: {e}")
        return None


def draw_footer(canvas, doc):
    footer_text = "Ma'lumotlar insell savdo dasturi yordamida tayyorlandi. Murojaat uchun: insell.uz +998 33 569 0901"
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 20, footer_text)
    canvas.restoreState()

# Agar bir nechta foydalanuvchiga parallel hisobot yaratilsa
#filename = f"umumiy_hisobot_{telegram_id}_{date.today()}.pdf"

def umumiy_pdf(telegram_id, logo_path=None):
    info = get_umumiy(telegram_id)
    filename = f"umumiy_hisobot_{date.today()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Custom style for heading and text
    heading = ParagraphStyle(name="Heading", fontSize=10, leading=24, alignment=TA_CENTER)
    centered_style = ParagraphStyle(name='Center', parent=styles['Normal'], alignment=TA_CENTER)
    right_aligned_style = ParagraphStyle(name='Right', parent=styles['Normal'], alignment=TA_RIGHT)

    # Header
    elements.append(Spacer(1, -60))
    branch_name = Paragraph(f"<b>{info['branch']}</b>", heading)
    elements.append(branch_name)
    elements.append(Spacer(1, 4))

    # Logo
    if logo_path:
        elements.append(Spacer(1, -20))
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))

    # Date
    elements.append(Paragraph(f"Sana: {date.today()}", centered_style))
    elements.append(Spacer(1, 12))

    # Statistika
    mahsulot = info['jami_mahsulot_summasi']
    nasiya = info['jami_nasiya_summasi']
    kassa = info['jami_kassa_balance']
    taminotchi = info['jami_taminotchi_balance']
    maosh = info['jami_hodimlar_balance']
    xarajat = info['jami_harajatlar']

    aktiv = mahsulot + nasiya + kassa
    passiv = taminotchi + maosh + xarajat
    balans = aktiv - passiv

    elements.append(Paragraph(
        f"<b><font color='#ff6a2c'>Umumiy hisobot: {balans:,.0f} so’m.</font></b>".replace(",", " "),
        centered_style))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Do’konda bor mahsulot", f"{mahsulot:,.0f} so’m".replace(",", " "), "Ta’minotchilar bilan hisob", f"{taminotchi:,.0f} so’m".replace(",", " ")],
        ["Nasiya summalari", f"{nasiya:,.0f} so’m".replace(",", " "), "Hodimlar maoshi", f"{maosh:,.0f} so’m".replace(",", " ")],
        ["Kassadagi summalar", f"{kassa:,.0f} so’m".replace(",", " "), "Qilingan harajatlar", f"{xarajat:,.0f} so’m".replace(",", " ")],
    ]

    table = Table(table_data, colWidths=[130, 120, 130, 120])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    table_data_2 = [
        [Paragraph(f"<font color='#ff6a2c'><b>{aktiv:,.0f} so’m</b></font>".replace(",", " "), right_aligned_style),
         Paragraph(f"<font color='#ff6a2c'><b>{passiv:,.0f} so’m</b></font>".replace(",", " "), right_aligned_style)],
        [Paragraph(f"<font color='#ff6a2c' size=14><b>{balans:,.0f} so’m</b></font>".replace(",", " "), centered_style), ''],
    ]

    table_2 = Table(table_data_2, colWidths=[250, 250])
    table_2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'RIGHT'),
        ('SPAN', (0, 1), (-1, 1)),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
    ]))

    elements.append(table_2)
    elements.append(Spacer(1, 30))
    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return filename
