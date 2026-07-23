from __future__ import annotations

from typing import Dict, List

import pandas as pd


class JobMarketAnalytics:
    """
    Analytics engine for job market insights.
    """

    REQUIRED_COLUMNS = [
        "job_title",
        "company",
        "location",
        "salary",
        "experience",
        "skills",
    ]

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def validate(self) -> None:
        """
        Validate required columns.
        """
        missing = [
            col for col in self.REQUIRED_COLUMNS
            if col not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

    def dataset_summary(self) -> Dict:
        """
        Return overall dataset statistics.
        """
        return {
            "total_jobs": len(self.df),
            "unique_companies": self.df["company"].nunique(),
            "unique_locations": self.df["location"].nunique(),
            "unique_job_titles": self.df["job_title"].nunique(),
        }

    def top_job_titles(self, top_n: int = 10) -> pd.DataFrame:
        """
        Most common job titles.
        """
        return (
            self.df["job_title"]
            .value_counts()
            .head(top_n)
            .reset_index(name="count")
            .rename(columns={"index": "job_title"})
        )

    def top_locations(self, top_n: int = 10) -> pd.DataFrame:
        """
        Most common hiring locations.
        """
        return (
            self.df["location"]
            .value_counts()
            .head(top_n)
            .reset_index(name="count")
            .rename(columns={"index": "location"})
        )

    def top_companies(self, top_n: int = 10) -> pd.DataFrame:
        """
        Companies with the most openings.
        """
        return (
            self.df["company"]
            .value_counts()
            .head(top_n)
            .reset_index(name="count")
            .rename(columns={"index": "company"})
        )

    def salary_statistics(self) -> Dict:
        """
        Salary summary statistics.
        """
        salary = pd.to_numeric(
            self.df["salary"],
            errors="coerce"
        )

        return {
            "average_salary": round(salary.mean(), 2),
            "median_salary": round(salary.median(), 2),
            "minimum_salary": round(salary.min(), 2),
            "maximum_salary": round(salary.max(), 2),
        }

    def experience_distribution(self):
        """
        Experience level distribution.
        """
        return (
            self.df["experience"]
            .fillna("Unknown")
            .value_counts()
        )

    def skill_frequency(self) -> pd.DataFrame:
        """
        Count frequency of skills.
        """
        skills: List[str] = []

        for row in self.df["skills"].dropna():
            parts = [
                s.strip()
                for s in str(row).split(",")
                if s.strip()
            ]
            skills.extend(parts)

        skill_df = (
            pd.Series(skills)
            .value_counts()
            .reset_index()
        )

        skill_df.columns = [
            "skill",
            "count"
        ]

        return skill_df

    def missing_values(self):
        """
        Missing value count.
        """
        return self.df.isnull().sum()

    def analytics_report(self) -> Dict:
        """
        Combined analytics report.
        """
        return {
            "summary": self.dataset_summary(),
            "salary": self.salary_statistics(),
            "top_jobs": self.top_job_titles().to_dict(
                orient="records"
            ),
            "top_locations": self.top_locations().to_dict(
                orient="records"
            ),
            "top_companies": self.top_companies().to_dict(
                orient="records"
            ),
        }