from fpdf import FPDF
from datetime import date

data = {
        "Sana": str(date.today()),
        "Umumiy foydalanuvchilar": 125,
        "Yangi foydalanuvchilar": 8,
        "Faol foydalanuvchilar": 67,
        "Yuborilgan xabarlar": 342
    }

def generate_pdf(data: dict, filename: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Kunlik Hisobot", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf_filename = pdf.output(filename)
    return pdf_filename