from __future__ import annotations

import re
from typing import List

import pandas as pd


class DataPreprocessor:
    """
    Data preprocessing utilities for job market datasets.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def remove_duplicates(self) -> pd.DataFrame:
        """
        Remove duplicate records.
        """
        self.df = self.df.drop_duplicates()
        return self.df

    def remove_missing_rows(self) -> pd.DataFrame:
        """
        Remove rows where all values are missing.
        """
        self.df = self.df.dropna(how="all")
        return self.df

    def fill_missing_text(
        self,
        columns: List[str],
        value: str = "Unknown",
    ) -> pd.DataFrame:
        """
        Fill missing values in text columns.
        """
        for column in columns:
            if column in self.df.columns:
                self.df[column] = (
                    self.df[column]
                    .fillna(value)
                    .astype(str)
                    .str.strip()
                )

        return self.df

    def normalize_salary(
        self,
        salary_column: str = "salary",
    ) -> pd.DataFrame:
        """
        Convert salary column into numeric values.
        """

        if salary_column not in self.df.columns:
            return self.df

        def clean_salary(value):
            if pd.isna(value):
                return None

            value = str(value)
            value = re.sub(r"[^\d.]", "", value)

            try:
                return float(value)
            except ValueError:
                return None

        self.df[salary_column] = self.df[salary_column].apply(clean_salary)

        return self.df

    def normalize_skills(
        self,
        skills_column: str = "skills",
    ) -> pd.DataFrame:
        """
        Normalize skills formatting.
        """

        if skills_column not in self.df.columns:
            return self.df

        self.df[skills_column] = (
            self.df[skills_column]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.replace(";", ",", regex=False)
            .str.replace("|", ",", regex=False)
            .str.strip()
        )

        return self.df

    def standardize_locations(
        self,
        location_column: str = "location",
    ) -> pd.DataFrame:
        """
        Standardize location names.
        """

        if location_column not in self.df.columns:
            return self.df

        self.df[location_column] = (
            self.df[location_column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

        return self.df

    def standardize_job_titles(
        self,
        title_column: str = "job_title",
    ) -> pd.DataFrame:
        """
        Standardize job titles.
        """

        if title_column not in self.df.columns:
            return self.df

        self.df[title_column] = (
            self.df[title_column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

        return self.df

    def preprocess(self) -> pd.DataFrame:
        """
        Run the complete preprocessing pipeline.
        """

        self.remove_duplicates()
        self.remove_missing_rows()

        self.fill_missing_text(
            [
                "job_title",
                "company",
                "location",
                "experience",
                "skills",
            ]
        )

        self.normalize_salary()
        self.normalize_skills()
        self.standardize_locations()
        self.standardize_job_titles()

        return self.df