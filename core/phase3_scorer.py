# core/phase3_scorer.py

from typing import List, Dict

class ResumeScorer:
    def __init__(self, extracted_data: Dict, job_profile: Dict):
        """
        extracted_data: output of ResumeExtractor
        job_profile: dict with keys:
            - required_skills: List[str]
            - min_education: List[str] (e.g., ["bachelor", "master"])
            - min_experience: int (years)
        """
        self.data = extracted_data
        self.job = job_profile

    def score_skills(self) -> float:
        required = set(self.job.get("required_skills", []))
        candidate = set(self.data.get("skills", []))
        if not required:
            return 1.0  # No skills requirement → full score
        return len(required & candidate) / len(required)

    def score_education(self) -> float:
        candidate_edu = set(self.data.get("education", []))
        required_edu = set(self.job.get("min_education", []))
        if not required_edu:
            return 1.0
        return 1.0 if candidate_edu & required_edu else 0.0

    def score_experience(self) -> float:
        signals = set(self.data.get("experience", []))
        required_signals = set(self.job.get("required_experience_signals", []))
        if not required_signals:
            return 1.0
        return len(signals & required_signals) / len(required_signals)

    def score_years_experience(self) -> float:
        candidate_years = self.data.get("years_experience", 0.0)
        min_years = self.job.get("min_experience", 0)
        if min_years == 0:
            return 1.0
        return min(candidate_years / min_years, 1.0)

    def score(self) -> Dict:
        """
        Returns detailed breakdown and total score (0–100)
        """
        weights = {
            "skills": 0.5,
            "education": 0.2,
            "experience": 0.2,
            "years_experience": 0.1
        }

        skill_score = self.score_skills()
        edu_score = self.score_education()
        exp_score = self.score_experience()
        years_score = self.score_years_experience()

        total_score = (
            skill_score * weights["skills"] +
            edu_score * weights["education"] +
            exp_score * weights["experience"] +
            years_score * weights["years_experience"]
        ) * 100  # convert to 0–100

        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "skills": round(skill_score * 100, 2),
                "education": round(edu_score * 100, 2),
                "experience": round(exp_score * 100, 2),
                "years_experience": round(years_score * 100, 2)
            }
        }
