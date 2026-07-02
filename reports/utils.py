from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(prediction):
    file_path='media/reports/prediction_report.pdf'
    doc=SimpleDocTemplate(file_path)
    elements=[]
    styles=getSampleStyleSheet()
    elements.append(Paragraph(f"Predicted Disease: {prediction.disease_name}", styles['Title']))
    elements.append(Paragraph(f'Disease: {prediction.predicted_disease}', styles['Normal']))
    elements.append(Paragraph(f'Confidence Score: {round(prediction.confidence_score*100,2)}%', styles['Normal']))
    doc.build(elements)
    return file_path