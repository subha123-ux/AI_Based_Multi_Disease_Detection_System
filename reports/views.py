from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from prediction.models import Prediction
from django.conf import settings
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.utils import timezone
from reportlab.platypus import Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

styles = getSampleStyleSheet()

center_style = ParagraphStyle(
    name="CenterTitle",
    parent=styles["Heading2"],
    alignment=TA_CENTER,
    spaceAfter=20,
)

signature_style = ParagraphStyle(
    name="SignatureStyle",
    fontSize=10,
    alignment=TA_RIGHT,
    fontName="Helvetica-Oblique",
    textColor="black",
)
from reportlab.lib.units import inch

def add_signature(canvas, doc):
    """
    Draw digital signature at bottom-right corner
    """
    canvas.saveState()

    canvas.setFont("Helvetica-Oblique", 9)

    text = [
        "Subhajit Mal",
        "malsubhajit010@gmail.com"
    ]

    x_position = doc.pagesize[0] - 2.5 * inch   
    y_position = 1 * inch                        

    for line in text:
        canvas.drawRightString(x_position + 2*inch, y_position, line)
        y_position -= 12

    canvas.restoreState()

@login_required
def download_report(request, report_id):

    report = get_object_or_404(Prediction, id=report_id)

    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized Access", status=401)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AI_Report_{report.id}.pdf"'


    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    logo_path = os.path.join(settings.BASE_DIR, "static", "logo.jpeg")

    logo = Image(logo_path, width=100, height=60)
    logo.hAlign = "CENTER"
    elements.append(logo)
    elements.append(Spacer(1, 15))


    elements.append(
        Paragraph(
            "AI Based Multi Diseases Detection System",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("<b>Medical Prediction Report</b>", center_style)
    )
    elements.append(Spacer(1, 20))


    local_time = timezone.localtime(report.date)
    report_date = local_time.strftime("%d %B %Y, %I:%M %p")

    data = [
        ["Patient Name", getattr(report, "name", "N/A")],
        ["Age", getattr(report, "age", "N/A")],
        ["Gender", getattr(report, "gender", "N/A")],
        ["Predicted Disease", getattr(report, "predicted_disease", "N/A")],
        ["Confidence", f"{getattr(report, 'confidence', 0):.2f}%"],
        ["Date", report_date],
    ]

    table = Table(data, colWidths=[180, 320])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 40))


    if report.image:
        image_path = os.path.join(settings.MEDIA_ROOT, report.image.name)

        if os.path.exists(image_path):
            img = Image(image_path, width=3*inch, height=3*inch)
            elements.append(img)
            elements.append(Spacer(1, 20))


    elements.append(
        Paragraph(
            "This report is automatically generated using AI based multi disease detection model.",
            styles["Normal"]
        )
    )

    doc.build(elements,
        onFirstPage=add_signature,
        onLaterPages=add_signature
    )

    return response




@login_required
def admin_all_reports(request):
    if request.user.role != "ADMIN":
        return HttpResponse("Unauthorized", status=401)

    reports = Prediction.objects.all().order_by('-date')
    return render(request, "admin_reports.html", {"reports": reports})