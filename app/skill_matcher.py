from __future__ import annotations

from typing import Dict, List, Set

import pandas as pd


class SkillMatcher:
    """
    AI-powered Skill Matching Engine.

    Responsibilities:
    - Extract skills from job postings
    - Compare user skills with market requirements
    - Calculate match percentage
    - Identify missing skills
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    @staticmethod
    def clean_skills(skills: str) -> Set[str]:
        """
        Convert comma-separated skills into a normalized set.
        """
        if pd.isna(skills):
            return set()

        return {
            skill.strip().lower()
            for skill in str(skills).split(",")
            if skill.strip()
        }

    def extract_market_skills(self) -> List[str]:
        """
        Return unique skills available in the dataset.
        """
        market_skills = set()

        if "skills" not in self.df.columns:
            return []

        for row in self.df["skills"].dropna():
            market_skills.update(self.clean_skills(row))

        return sorted(market_skills)

    def skill_frequency(self) -> pd.DataFrame:
        """
        Count occurrences of each skill.
        """
        skills = []

        if "skills" not in self.df.columns:
            return pd.DataFrame(columns=["skill", "count"])

        for row in self.df["skills"].dropna():
            skills.extend(self.clean_skills(row))

        frequency = (
            pd.Series(skills)
            .value_counts()
            .reset_index()
        )

        frequency.columns = [
            "skill",
            "count",
        ]

        return frequency

    def match_skills(
        self,
        user_skills: List[str],
    ) -> Dict:
        """
        Compare user skills with market skills.
        """

        user_skill_set = {
            skill.lower().strip()
            for skill in user_skills
        }

        market_skill_set = set(
            self.extract_market_skills()
        )

        matched = sorted(
            user_skill_set.intersection(
                market_skill_set
            )
        )

        missing = sorted(
            market_skill_set.difference(
                user_skill_set
            )
        )

        percentage = 0.0

        if market_skill_set:
            percentage = round(
                len(matched)
                / len(market_skill_set)
                * 100,
                2,
            )

        return {
            "match_percentage": percentage,
            "matched_skills": matched,
            "missing_skills": missing,
            "user_skill_count": len(user_skill_set),
            "market_skill_count": len(market_skill_set),
        }

    def top_skills(
        self,
        top_n: int = 20,
    ) -> pd.DataFrame:
        """
        Return top N in-demand skills.
        """
        return self.skill_frequency().head(top_n)