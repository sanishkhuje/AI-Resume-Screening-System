import pytest
from ai_service.core.phase2_extractor import ResumeExtractor
from ai_service.core.phase3_scorer import ResumeScorer

# -------------------------
# Helper function to create data
# -------------------------
def extract_from_text(text: str):
    extractor = ResumeExtractor(text)
    return extractor.extract()


# -------------------------
# Test cases
# -------------------------

def test_scorer_all_matched():
    text = """
    skills python ml docker aws
    education bachelor
    experience worked on projects for 5 years
    """
    data = extract_from_text(text)

    job_profile = {
        "required_skills": ["python", "ml", "docker", "aws"],
        "min_education": ["bachelor", "master"],
        "required_experience_signals": ["experience", "projects"],
        "min_experience": 5
    }

    scorer = ResumeScorer(data, job_profile)
    result = scorer.score()

    assert result["total_score"] == 100.0
    assert all(score == 100.0 for score in result["breakdown"].values())


def test_scorer_partial_skills():
    text = """
    skills python ml
    education bachelor
    experience worked on projects for 3 years
    """
    data = extract_from_text(text)

    job_profile = {
        "required_skills": ["python", "ml", "docker", "aws"],
        "min_education": ["bachelor", "master"],
        "required_experience_signals": ["experience", "projects"],
        "min_experience": 5
    }

    scorer = ResumeScorer(data, job_profile)
    result = scorer.score()

    # Skills match: 2/4 = 50%
    assert result["breakdown"]["skills"] == 50.0
    # Education full
    assert result["breakdown"]["education"] == 100.0
    # Experience signals full
    assert result["breakdown"]["experience"] == 100.0
    # Years experience 3/5 = 60%
    assert result["breakdown"]["years_experience"] == 60.0


def test_scorer_missing_education():
    text = """
    skills python ml docker
    experience worked on projects for 4 years
    """
    data = extract_from_text(text)

    job_profile = {
        "required_skills": ["python", "ml", "docker", "aws"],
        "min_education": ["bachelor", "master"],
        "required_experience_signals": ["experience", "projects"],
        "min_experience": 3
    }

    scorer = ResumeScorer(data, job_profile)
    result = scorer.score()

    # Education missing → 0%
    assert result["breakdown"]["education"] == 0.0
    # Skills 3/4 = 75%
    assert result["breakdown"]["skills"] == 75.0
    # Experience signals 100%
    assert result["breakdown"]["experience"] == 100.0
    # Years 4/3 capped at 1 → 100%
    assert result["breakdown"]["years_experience"] == 100.0


def test_scorer_empty_resume():
    text = ""
    data = extract_from_text(text)

    job_profile = {
        "required_skills": ["python", "ml", "docker"],
        "min_education": ["bachelor"],
        "required_experience_signals": ["experience", "projects"],
        "min_experience": 2
    }

    scorer = ResumeScorer(data, job_profile)
    result = scorer.score()

    assert result["total_score"] == 0.0
    assert all(score == 0.0 for score in result["breakdown"].values())


def test_scorer_no_job_requirements():
    text = """
    skills python ml docker
    education bachelor
    experience worked on projects for 5 years
    """
    data = extract_from_text(text)

    job_profile = {}  # No requirements

    scorer = ResumeScorer(data, job_profile)
    result = scorer.score()

    # All components should be 100% by default
    assert result["total_score"] == 100.0
    assert all(score == 100.0 for score in result["breakdown"].values())
