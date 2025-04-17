import requests
from datetime import date
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Unicode shriftni ulash uchun
pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))  # Shrift faylini shu joyga qo'ying
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Unicode', fontName='DejaVu', fontSize=10))
styles.add(ParagraphStyle(name='WrapLeft', fontName='DejaVu', fontSize=8, alignment=0))

def get_category():
    url = "https://demo.api-insell.uz/get_categories_for_bot/1111/"
    res = requests.get(url).json()
    # Har bir kategoriya: (id, name) ko‘rinishida
    return [(item['category_id'], item['category_name']) for item in res['data']]

def get_mahsulot():
    url = "https://demo.api-insell.uz/get_statistics_for_bot/mahsulot_hisoboti/1111/"
    category_data = {}
    branch = None  # Branchni tashqarida e'lon qilamiz

    for cat_id, cat_name in get_category():
        params = {
            "from_time": str(date.today()),
            "to_time": str(date.today()),
            "category_id": cat_id
        }
        try:
            res = requests.get(url, params=params).json()
            if res['data']:
                data_block = res['data'][0]
                if not branch:
                    branch = data_block.get('branch')
                items = data_block.get('items', [])
                if items:
                    category_data[cat_name] = items
        except requests.exceptions.RequestException as e:
            print(f"Xatolik: {e}")

    return {
        "branch": branch,
        "categories": category_data
    }


def generate_pdf(logo_path=None):
    mahsulotlar = get_mahsulot()
    doc_path = f"mahsulot_hisobot_{date.today()}.pdf"
    doc = SimpleDocTemplate(doc_path, pagesize=A4)
    elements = []

    # Custom style for branch name
    heading = ParagraphStyle(
        name="Heading",
        fontSize=10,
        leading=24,
        alignment=TA_CENTER
    )

    # Branch name
    elements.append(Spacer(1, -60))
    branch_name = Paragraph(f"<b>{mahsulotlar['branch']}</b>", heading)
    elements.append(branch_name)
    elements.append(Spacer(1, 4))

    # Logotip – yuqoriroq joylashtirish
    if logo_path:
        elements.append(Spacer(1, -20))  # manfiy spacer – logoni yuqoriroq suradi
        logo = Image(logo_path, width=60, height=25)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 4))  # logodan keyin kichik masofa

    # Sana
    elements.append(Paragraph(f"Sana: {date.today()}", styles['Unicode']))
    elements.append(Spacer(1, 12))

    # Umumiy summa
    umumiy_summa = 0
    for items in mahsulotlar['categories'].values():
        for item in items:
            try:
                umumiy_summa += int(item.get('summa', 0))
            except:
                pass

    elements.append(Paragraph(
        f"<b><font size=14 color='#ff6a2c'>Mahsulotlar: {umumiy_summa:,} so’m.</font></b>",
        styles['Unicode']
    ))
    elements.append(Spacer(1, 10))

    # Har bir kategoriya uchun jadval
    for category_name, items in mahsulotlar["categories"].items():
        kategoriya_summa = sum([int(i.get("summa", 0)) for i in items])
        kategoriya_soni = len(items)

        kategoriya_sarlavha = f"{category_name} : {kategoriya_summa:,} so’m, {kategoriya_soni} xil"
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<font color='black'><b>{kategoriya_sarlavha}</b></font>", styles['Unicode']))
        elements.append(Spacer(1, 4))

        # Jadval sarlavhasi
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

    # Pastki eslatma
    elements.append(Paragraph(
        "<font size=8>Ma'lumotlar insell savdo dasturi yordamida tayyorlandi. "
        "Murojaat uchun: insell.uz +998 33 569 0901</font>", styles['Unicode']
    ))

    doc.build(elements)
    return doc_path

# PDF faylni yaratish
pdf = generate_pdf("insell.png")
print(f"PDF tayyor: {pdf}")
