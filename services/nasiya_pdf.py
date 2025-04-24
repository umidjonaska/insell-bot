import requests
from datetime import date, datetime
from pprint import pprint as print
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def get_nasiya(telegram_id):
    url = f"https://demo.api-insell.uz/get_statistics_for_bot/nasiya/{telegram_id}/?from_time={date.today()}&to_time={date.today()}"
    r = requests.get(url, timeout=10)
    res = r.json()
    return res['data'][0]


def nasiya_pdf(telegram_id, logo_path=None):
    data = get_nasiya(telegram_id)

    filename = f"hisobot_nasiya_{date.today()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Custom style for branch name
    heading = ParagraphStyle(
        name="Heading",
        fontSize=10,
        leading=24,
        alignment=TA_CENTER
    )

    # Branch name
    elements.append(Spacer(1, -60))
    branch_name = Paragraph(f"<b>{data['branch']}</b>", heading)
    elements.append(branch_name)
    elements.append(Spacer(1, 4))

    # Logo
    if logo_path:
        elements.append(Spacer(1, -20))
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))

    # Sana
    elements.append(Paragraph(f"Sana: {date.today()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Jadval sarlavhasi va umumiy summa
    jadval_data = [['T/R', 'Mijoz', 'Aloqa', 'Summa', 'Qaytarish sanasi', 'Qolgan kun']]
    jami_summa = 0

    if not data['muddati_kelgan']:
        elements.append(Paragraph("Ma'lumot topilmadi.", styles['Normal']))
    else:
        for index, item in enumerate(data['muddati_kelgan'], start=1):
            # Qaytarish sanasidan qolgan kun
            qaytarish_sana_str = item.get('qaytarish_sana', '')
            qolgan_kun = ''
            try:
                qaytarish_sana = datetime.strptime(qaytarish_sana_str, '%Y-%m-%d').date()
                farq = (qaytarish_sana - date.today()).days
                if farq >= 0:
                    qolgan_kun = f"{farq} kun"
                else:
                    qolgan_kun = f"O'tgan {abs(farq)} kun"
            except:
                qolgan_kun = "Xatolik"

            summa = item.get('qoldiq_summa', 0)
            try:
                jami_summa += float(summa)
            except:
                pass

            row = [
                str(index),
                item.get('customer_name', ''),
                item.get('customer_phone', ''),
                summa,
                qaytarish_sana_str,
                qolgan_kun
            ]
            jadval_data.append(row)

        # Jami summani chiqarish (jadval ustida)
        formatted_sum = f"{int(jami_summa):,}".replace(",", " ")
        elements.append(Paragraph(
            f"<b><font color='#ff6a2c'>Jami: {formatted_sum} so’m</font></b>",
            styles['Normal']
        ))
        elements.append(Spacer(1, 10))

        # Jadval
        table = Table(jadval_data, colWidths=[30, 100, 100, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#ff6a2c'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 30))

    # PDF ni build qilish
    doc.build(elements)
    return filename
