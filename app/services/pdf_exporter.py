from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles=getSampleStyleSheet()


class PDFExporter:


    def export_week(self,week,file):

        doc=SimpleDocTemplate(file)

        elements=[]

        elements.append(
            Paragraph("Weekly Plan",styles["Title"])
        )

        for day in week:

            elements.append(
                Paragraph(str(week[day]),styles["Normal"])
            )

        doc.build(elements)