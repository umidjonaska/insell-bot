import requests
from pprint import pprint as print
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

def get_umumiy():
    url = f"https://demo.api-insell.uz/get_statistics_for_bot/umumiy_hisobot/1111/?from_time={date.today()}&to_time={date.today()}"
    r = requests.get(url)
    res = r.json()
    data = res['data'][0]

    return data

def draw_footer(canvas, doc):
    footer_text = "Ma'lumotlar insell savdo dasturi yordamida tayyorlandi. Murojaat uchun: insell.uz +998 33 569 0901"
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 20, footer_text)  # Sahifaning markazi, pastdan 20 pt yuqorida
    canvas.restoreState()


def generate_pdf(logo_path=None):
    info = get_umumiy()
    filename = f"umumiy_hisobot_{date.today()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading1"]

    # Custom style for branch name
    heading = ParagraphStyle(
    name="Heading",
    fontSize=10,
    leading=24,
    alignment=TA_CENTER
)
    elements.append(Spacer(1, -60))
    branch_name = Paragraph(f"<b>{info['branch']}</b>", heading)
    elements.append(branch_name)
    elements.append(Spacer(1, 4))

    # Logotip – yuqoriroq joylashtirish
    if logo_path:
        elements.append(Spacer(1, -20))  # manfiy spacer – logoni yuqoriroq suradi
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))  # logodan keyin kichik masofa

    # Custom center-aligned style
    centered_style = ParagraphStyle(
        name='Center',
        parent=styles['Normal'],
        alignment=TA_CENTER
    )

    # Custom RIGHT-aligned style
    right_aligned_style = ParagraphStyle(
        name='Right',
        parent=styles['Normal'],
        alignment=TA_RIGHT
    )


    # Sana va umumiy summa (MARKAZGA hizalangan)
    elements.append(Paragraph(f"Sana: {date.today()}", centered_style))
    elements.append(Spacer(1, 12))



    info = get_umumiy()

    mahsulot = info['jami_mahsulot_summasi']
    nasiya = info['jami_nasiya_summasi']
    kassa = info['jami_kassa_balance']
    taminotchi = info['jami_taminotchi_balance']
    maosh = info['jami_hodimlar_balance']
    xarajat = info['jami_harajatlar']

    aktiv = mahsulot + nasiya + kassa
    passiv = taminotchi + maosh + xarajat
    balans = aktiv - passiv

    elements.append(Paragraph(f"<b><font color='#ff6a2c'>Umumiy hisobot: {balans:,.0f} so’m.</font></b>".replace(",", " "), centered_style))
    elements.append(Spacer(1, 12))

    # Bosh jadval
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

    # 4- va 5-qatorlarni alohida jadvalga olib o'tish
    table_data_2 = [
        [Paragraph(f"<font color='#ff6a2c'><b>{aktiv:,.0f} so’m</b></font>".replace(",", " "), right_aligned_style),Paragraph(f"<font color='#ff6a2c'><b>{passiv:,.0f} so’m</b></font>".replace(",", " "), right_aligned_style)],
        [Paragraph(f"<font color='#ff6a2c' size=14><b>{balans:,.0f} so’m</b></font>".replace(",", " "), centered_style), ''],

    ]

    table_2 = Table(table_data_2, colWidths=[250, 250])

    table_2.setStyle(TableStyle([
        # Jadval chegaralari va o‘rtadan vertikal hizalash
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # 1-qator (aktiv va passiv) – o‘ng tarafga hizalash
        #('ALIGN', (0, 0), (-1, 0), 'RIGHT'),
        ('ALIGN', (0, 0), (-1, 0), 'RIGHT'),


        # 2-qator (balans) – ustunlarni birlashtirib markazga hizalash
        ('SPAN', (0, 1), (-1, 1)),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
    ]))


    elements.append(table_2)
    elements.append(Spacer(1, 30))

    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return filename

# Test qilish
# generate_pdf(logo_path="insell.jpg")
pdf_path = generate_pdf('insell.png')
if pdf_path:
    print(f"PDF fayl yaratildi: {pdf_path}")
else:
    print("PDF yaratib bo‘lmadi.")
