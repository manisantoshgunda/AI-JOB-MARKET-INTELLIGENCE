from __future__ import annotations

from typing import Dict

import pandas as pd


class MarketAnalyzer:
    """
    Job Market Intelligence Analyzer.

    Features:
    - Trending skills
    - Hiring hotspots
    - Top hiring companies
    - Salary statistics
    - Experience distribution
    - Executive summary
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def top_skills(self, top_n: int = 10) -> pd.DataFrame:
        """
        Return the most demanded skills.
        """
        if "skills" not in self.df.columns:
            return pd.DataFrame(columns=["skill", "count"])

        skills = []

        for row in self.df["skills"].dropna():
            skills.extend(
                [
                    skill.strip().lower()
                    for skill in str(row).split(",")
                    if skill.strip()
                ]
            )

        result = (
            pd.Series(skills)
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = ["skill", "count"]

        return result

    def top_locations(self, top_n: int = 10) -> pd.DataFrame:
        """
        Return top hiring locations.
        """
        if "location" not in self.df.columns:
            return pd.DataFrame(columns=["location", "count"])

        result = (
            self.df["location"]
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = ["location", "count"]

        return result

    def top_companies(self, top_n: int = 10) -> pd.DataFrame:
        """
        Return companies with the most openings.
        """
        if "company" not in self.df.columns:
            return pd.DataFrame(columns=["company", "count"])

        result = (
            self.df["company"]
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = ["company", "count"]

        return result

    def salary_statistics(self) -> Dict:
        """
        Compute salary statistics.
        """
        if "salary" not in self.df.columns:
            return {}

        salary = pd.to_numeric(
            self.df["salary"],
            errors="coerce",
        ).dropna()

        if salary.empty:
            return {}

        return {
            "average_salary": round(salary.mean(), 2),
            "median_salary": round(salary.median(), 2),
            "minimum_salary": round(salary.min(), 2),
            "maximum_salary": round(salary.max(), 2),
        }

    def experience_distribution(self) -> pd.DataFrame:
        """
        Return experience level distribution.
        """
        if "experience" not in self.df.columns:
            return pd.DataFrame(
                columns=["experience", "count"]
            )

        result = (
            self.df["experience"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        result.columns = [
            "experience",
            "count",
        ]

        return result

    def demand_score(self) -> float:
        """
        Calculate a simple market demand score.
        """
        total_jobs = len(self.df)

        unique_companies = (
            self.df["company"].nunique()
            if "company" in self.df.columns
            else 0
        )

        unique_locations = (
            self.df["location"].nunique()
            if "location" in self.df.columns
            else 0
        )

        score = (
            total_jobs * 0.5
            + unique_companies * 0.3
            + unique_locations * 0.2
        )

        return round(score, 2)

    def executive_summary(self) -> Dict:
        """
        Generate overall market summary.
        """
        return {
            "total_jobs": len(self.df),
            "top_company":
                self.top_companies(1).iloc[0]["company"]
                if not self.top_companies(1).empty
                else None,
            "top_location":
                self.top_locations(1).iloc[0]["location"]
                if not self.top_locations(1).empty
                else None,
            "market_demand_score":
                self.demand_score(),
            "salary_statistics":
                self.salary_statistics(),
        }