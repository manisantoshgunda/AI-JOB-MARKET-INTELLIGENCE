from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

from app.analytics import JobMarketAnalytics
from app.data_loader import DataLoader
from app.market_analyzer import MarketAnalyzer
from app.preprocessing import DataPreprocessor
from app.recommendation_engine import RecommendationEngine
from app.skill_matcher import SkillMatcher


class Dashboard:

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.df: pd.DataFrame | None = None

    def initialize(self):

        loader = DataLoader(str(self.dataset_path))
        self.df = loader.load_data()

        preprocessor = DataPreprocessor(self.df)
        self.df = preprocessor.preprocess()

    def analytics(self) -> Dict:

        analytics = JobMarketAnalytics(self.df)
        analytics.validate()

        return analytics.analytics_report()

    def market_summary(self) -> Dict:

        analyzer = MarketAnalyzer(self.df)

        return analyzer.executive_summary()

    def recommend_jobs(
        self,
        skills: List[str],
        location: str | None = None,
        experience: str | None = None,
        minimum_salary: float | None = None,
        top_n: int = 10,
    ):

        engine = RecommendationEngine(self.df)

        return engine.recommend_jobs(
            user_skills=skills,
            preferred_location=location,
            experience=experience,
            minimum_salary=minimum_salary,
            top_n=top_n,
        )

    def skill_match(self, skills: List[str]):

        matcher = SkillMatcher(self.df)

        return matcher.match_skills(skills)