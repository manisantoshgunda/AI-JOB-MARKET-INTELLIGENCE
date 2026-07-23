from pydantic import BaseModel
from typing import List, Dict


class ResumeAnalysisRequest(BaseModel):
    job_description: str


class ResumeAnalysisResponse(BaseModel):
    ats_score: float
    match_percentage: float
    missing_skills: List[str]
    strengths: List[str]
    recommendations: List[str]
    summary: str


class AnalyticsResponse(BaseModel):
    total_jobs: int
    top_skills: Dict[str, int]
    average_salary: float
    top_locations: Dict[str, int]