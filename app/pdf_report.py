from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFReport:

    @staticmethod
    def generate(result, filename="resume_analysis.pdf"):

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(filename)

        elements = []

        elements.append(
            Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"])
        )

        elements.append(
            Paragraph(
                f"<b>ATS Score:</b> {result['resume_score']}%",
                styles["BodyText"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Rating:</b> {result['rating']}",
                styles["BodyText"],
            )
        )

        elements.append(
            Paragraph("<b>Matched Skills</b>", styles["Heading2"])
        )

        for skill in result["matched_skills"]:
            elements.append(
                Paragraph(f"• {skill}", styles["BodyText"])
            )

        elements.append(
            Paragraph("<b>Missing Skills</b>", styles["Heading2"])
        )

        for skill in result["missing_skills"]:
            elements.append(
                Paragraph(f"• {skill}", styles["BodyText"])
            )

        elements.append(
            Paragraph("<b>Suggestions</b>", styles["Heading2"])
        )

        for suggestion in result["suggestions"]:
            elements.append(
                Paragraph(f"• {suggestion}", styles["BodyText"])
            )

        document.build(elements)

        return filename