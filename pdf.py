from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date

from services.request import fetch_report_data

data = fetch_report_data()

def generate_pdf(logo_path=None):
    doc = SimpleDocTemplate(f"hisobot{date.today()}.pdf", pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logotip (yuqori o‘ng burchakda)
    if logo_path:
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)

    # Sana va umumiy summa
    elements.append(Paragraph(f"Sana: {date.today()}", styles['Normal']))
    elements.append(Spacer(1, 12))
    #Mahsulotlar umumiy summasi keladi
    elements.append(Paragraph("<b><font color='orange'>Mahsulotlar: 2 650 234 so’m.</font></b>", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Jadval ma'lumotlari
    #Bu aslida apidan keladigan malumotlar bo'lishi kerak
    jadval_data = [
        ['T/R', 'Mahsulot', 'Kun boshi', 'Keldi', 'Sotildi', 'Qoldiq', 'Narx', 'Summa'],
        ['Suv : 801 900 so’m, 2 xil'] + [''] * 7,
        ['1', 'Coca-Cola 0.5 L', '100', '50', '77', '73', '3 300', '240 900'],
        ['2', 'Coca-Cola 1 L', '220', '50', '100', '170', '3 300', '561 000'],
        ['Shirinliklar : 1 801 900 so’m, 12 xil'] + [''] * 7,
        ['3', 'Napaleon', '', '', '', '', '', ''],
        ['4', 'Medovik', '', '', '', '', '', ''],
    ]

    table = Table(jadval_data, colWidths=[30, 110, 60, 50, 50, 50, 50, 70])
    table.setStyle(TableStyle([
        # Sarlavha
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Jadval chiziqlari va joylashuv
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

        # Suv sarlavhasini birlashtirish va markazlash
        ('SPAN', (0, 1), (-1, 1)),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),

        # Shirinliklar sarlavhasini birlashtirish va markazlash
        ('SPAN', (0, 4), (-1, 4)),
        ('ALIGN', (0, 4), (-1, 4), 'CENTER'),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 30))

    # Pastki izoh
    elements.append(Paragraph("<font size=8>Ma'lumotlar insell savdo dasturi yordamida tayyorlandi. "
                              "Murojaat uchun: insell.uz +998 33 569 0901</font>", styles['Normal']))

    doc.build(elements)

# PDF yaratish
generate_pdf(logo_path="insell.jpg")
