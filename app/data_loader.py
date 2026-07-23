from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


class DataLoader:
    """
    Utility class for loading job market datasets.
    Supports CSV, Excel, and JSON files.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def validate_file(self) -> None:
        """
        Validate whether the file exists and is supported.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        if self.file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {self.file_path.suffix}"
            )

    def load_data(self) -> pd.DataFrame:
        """
        Load dataset based on file extension.
        """
        self.validate_file()

        extension = self.file_path.suffix.lower()

        if extension == ".csv":
            return pd.read_csv(self.file_path)

        if extension in [".xlsx", ".xls"]:
            return pd.read_excel(self.file_path)

        if extension == ".json":
            return pd.read_json(self.file_path)

        raise ValueError("Unsupported file format.")

    @staticmethod
    def preview_data(
        dataframe: pd.DataFrame,
        rows: int = 5
    ) -> pd.DataFrame:
        """
        Return the first few rows of the dataset.
        """
        return dataframe.head(rows)

    @staticmethod
    def dataset_info(
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Return dataset metadata.
        """
        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": dataframe.columns.tolist(),
            "missing_values": dataframe.isnull().sum().to_dict(),
        }

    @staticmethod
    def save_data(
        dataframe: pd.DataFrame,
        output_path: str
    ) -> None:
        """
        Save processed data as CSV.
        """
        dataframe.to_csv(output_path, index=False)