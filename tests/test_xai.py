import pytest
from core.phase4_xai import ResumeExplainer


# -------------------------
# Helper function
# -------------------------
def explain(score_output, resume_data, job_profile):
    explainer = ResumeExplainer(score_output, resume_data, job_profile)
    return explainer.explain()


# -------------------------
# TEST CASES
# -------------------------

def test_xai_all_matched():
    score_output = {
        "total_score": 100.0,
        "breakdown": {
            "skills": 100.0,
            "education": 100.0,
            "experience": 100.0,
            "years_experience": 100.0,
        }
    }

    resume_data = {
        "skills": ["python", "ml", "docker", "aws"],
        "education": ["bachelor"],
        "experience": ["experience", "projects"],
        "years_experience": 5,
    }

    job_profile = {
        "required_skills": ["python", "ml", "docker", "aws"],
        "min_education": ["bachelor"],
        "required_experience_signals": ["experience", "projects"],
        "min_experience": 5,
    }

    result = explain(score_output, resume_data, job_profile)

    assert result["total_score"] == 100.0
    assert "Relevant skills found" in " ".join(result["positive_factors"])
    assert result["negative_factors"] == []


def test_xai_missing_skills():
    score_output = {
        "total_score": 70.0,
        "breakdown": {
            "skills": 50.0,
            "education": 100.0,
            "experience": 100.0,
            "years_experience": 80.0,
        }
    }

    resume_data = {
        "skills": ["python", "ml"],
        "education": ["bachelor"],
        "experience": ["projects"],
        "years_experience": 4,
    }

    job_profile = {
        "required_skills": ["python", "ml", "docker", "aws"],
        "min_education": ["bachelor"],
        "required_experience_signals": ["projects"],
        "min_experience": 5,
    }

    result = explain(score_output, resume_data, job_profile)

    assert "Missing required skills" in " ".join(result["negative_factors"])
    assert "Matched 2 out of 4 required skills" in result["explanations"]["skills"]


def test_xai_insufficient_experience_years():
    score_output = {
        "total_score": 60.0,
        "breakdown": {
            "skills": 100.0,
            "education": 100.0,
            "experience": 100.0,
            "years_experience": 40.0,
        }
    }

    resume_data = {
        "skills": ["python", "ml"],
        "education": ["bachelor"],
        "experience": ["experience"],
        "years_experience": 2,
    }

    job_profile = {
        "required_skills": ["python", "ml"],
        "min_education": ["bachelor"],
        "required_experience_signals": ["experience"],
        "min_experience": 5,
    }

    result = explain(score_output, resume_data, job_profile)

    assert "below the required" in result["explanations"]["years_experience"]
    assert "Insufficient years of experience" in result["negative_factors"]


def test_xai_no_job_requirements():
    score_output = {
        "total_score": 100.0,
        "breakdown": {
            "skills": 100.0,
            "education": 100.0,
            "experience": 100.0,
            "years_experience": 100.0,
        }
    }

    resume_data = {
        "skills": ["python"],
        "education": ["bachelor"],
        "experience": ["projects"],
        "years_experience": 1,
    }

    job_profile = {}

    result = explain(score_output, resume_data, job_profile)

    assert "not restricted" in " ".join(result["positive_factors"])
    assert result["negative_factors"] == []


def test_xai_empty_resume():
    score_output = {
        "total_score": 0.0,
        "breakdown": {
            "skills": 0.0,
            "education": 0.0,
            "experience": 0.0,
            "years_experience": 0.0,
        }
    }

    resume_data = {
        "skills": [],
        "education": [],
        "experience": [],
        "years_experience": 0.0,
    }

    job_profile = {
        "required_skills": ["python"],
        "min_education": ["bachelor"],
        "required_experience_signals": ["experience"],
        "min_experience": 2,
    }

    result = explain(score_output, resume_data, job_profile)

    assert result["total_score"] == 0.0
    assert len(result["negative_factors"]) >= 1
