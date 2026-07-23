from __future__ import annotations

from typing import Dict, List

import pandas as pd


class RecommendationEngine:
    """
    AI Job Recommendation Engine
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    @staticmethod
    def _normalize_skills(skills: str) -> set[str]:
        if pd.isna(skills):
            return set()

        return {
            skill.strip().lower()
            for skill in str(skills).split(",")
            if skill.strip()
        }

    def recommend_jobs(
        self,
        user_skills: List[str],
        preferred_location: str | None = None,
        experience: str | None = None,
        minimum_salary: float | None = None,
        top_n: int = 10,
    ) -> pd.DataFrame:

        user_skill_set = {
            skill.strip().lower()
            for skill in user_skills
            if skill.strip()
        }

        recommendations = []

        for _, row in self.df.iterrows():

            job_skills = self._normalize_skills(
                row.get("skills", "")
            )

            matched = user_skill_set.intersection(job_skills)

            if len(job_skills) == 0:
                skill_percent = 0
            else:
                skill_percent = (
                    len(matched) / len(job_skills)
                ) * 100

            score = skill_percent

            if preferred_location:

                if (
                    str(row.get("location", "")).lower()
                    == preferred_location.lower()
                ):
                    score += 10

            if experience:

                if (
                    str(row.get("experience", "")).lower()
                    == experience.lower()
                ):
                    score += 10

            salary = pd.to_numeric(
                row.get("salary"),
                errors="coerce"
            )

            if (
                minimum_salary is not None
                and pd.notna(salary)
                and salary >= minimum_salary
            ):
                score += 10

            recommendations.append(
                {
                    "Job Title": row.get("job_title"),
                    "Company": row.get("company"),
                    "Location": row.get("location"),
                    "Experience": row.get("experience"),
                    "Salary": salary,
                    "Required Skills": row.get("skills"),
                    "Matched Skills": ", ".join(sorted(matched)),
                    "Match %": round(skill_percent, 1),
                    "Recommendation Score": round(score, 1),
                }
            )

        result = pd.DataFrame(recommendations)

        if result.empty:
            return result

        result = result.sort_values(
            by="Recommendation Score",
            ascending=False
        )

        result = result[result["Recommendation Score"] > 0]

        return result.head(top_n).reset_index(drop=True)

    def top_recommendation(
        self,
        user_skills: List[str],
    ) -> Dict:

        recommendations = self.recommend_jobs(
            user_skills=user_skills,
            top_n=1,
        )

        if recommendations.empty:
            return {}

        return recommendations.iloc[0].to_dict()