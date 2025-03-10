from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from django.http import HttpResponse
from datetime import datetime

def generate_pdf_token(token):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="token_{token.token_number}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # 🔹 **Header Title (Similar to the Image)**
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Title'],
        fontSize=16,
        textColor=colors.black,
        alignment=1,
        spaceAfter=12,
    )
    header = Paragraph("Medical Clinic Token", header_style)
    elements.append(header)
    elements.append(Spacer(1, 20))

    # 📌 **Token Information (Formatted Like a Receipt)**
    token_data = [
        ["Date", token.date.strftime('%d-%m-%Y')],
        ["Patient Name", token.patient_name],
        ["Token Number", token.token_number]
    ]
    
    token_table = Table(token_data, colWidths=[150, 250])
    token_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(token_table)
    elements.append(Spacer(1, 30))

    # ⏰ **Reminder**
    reminder = Paragraph("🔔 Please arrive on time.", styles["BodyText"])
    elements.append(reminder)

    # 📅 **Generated Timestamp**
    timestamp = Paragraph(
        f"<font size=9 color='gray'>Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}</font>",
        styles["BodyText"]
    )
    elements.append(Spacer(1, 20))
    elements.append(timestamp)

    # 📍 **Footer - Clinic Information (Matching Image Style)**
    footer_data = [
        ["📍 Address:", "123 Healthcare Street, Downtown, YourCity - 567890"],
        ["📞 Contact:", "(123) 456-7890"],
        ["✉ Email:", "info@citycare.com"],
        ["🌍 Website:", "www.citycarehospital.com"]
    ]

    footer_table = Table(footer_data, colWidths=[100, 300])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))

    elements.append(Spacer(1, 40))
    elements.append(footer_table)

    # 🚀 **Build PDF**
    doc.build(elements)
    return response
