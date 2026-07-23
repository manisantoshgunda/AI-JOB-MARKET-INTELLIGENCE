import re
from PyPDF2 import PdfReader


class ResumeAnalyzer:

    def __init__(self, required_skills):
        self.required_skills = sorted(
            list(set(skill.lower().strip() for skill in required_skills))
        )

    def extract_text_from_pdf(self, uploaded_file):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    def analyze(self, resume_text):

        resume_text = resume_text.lower()

        matched = []

        for skill in self.required_skills:

            if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):

                matched.append(skill)

        matched = sorted(list(set(matched)))

        missing = sorted(
            list(set(self.required_skills) - set(matched))
        )

        score = (
            round(len(matched) / len(self.required_skills) * 100)
            if self.required_skills
            else 0
        )

        if score >= 85:
            rating = "Excellent ⭐⭐⭐⭐⭐"
        elif score >= 70:
            rating = "Good ⭐⭐⭐⭐"
        elif score >= 50:
            rating = "Average ⭐⭐⭐"
        else:
            rating = "Needs Improvement ⭐⭐"

        suggestions = []

        for skill in missing[:10]:
            suggestions.append(f"Add {skill} to your resume if you have experience with it.")

        return {
            "resume_score": score,
            "rating": rating,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": suggestions,
        }