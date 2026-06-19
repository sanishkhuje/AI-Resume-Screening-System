# tests/test_extractor.py

import pytest
from ai_service.core.phase2_extractor import ResumeExtractor


def test_resume_extraction_basic():
    text = """
    skills python ml sql
    education bachelor degree
    experience worked on projects for 3 years
    """
    extractor = ResumeExtractor(text)
    data = extractor.extract()

    assert "python" in data["skills"]
    assert "machine learning" in data["skills"]
    assert "sql" in data["skills"]

    assert "bachelor" in data["education"]
    assert data["years_experience"] == 3.0


def test_resume_extraction_internship():
    text = """
    internship experience working on python projects
    """
    extractor = ResumeExtractor(text)
    data = extractor.extract()

    assert data["years_experience"] == 0.5
    assert "python" in data["skills"]


def test_resume_extraction_no_skills_section():
    text = """
    education master degree
    experience worked on java projects for 2 years
    """
    extractor = ResumeExtractor(text)
    data = extractor.extract()

    # Skills fallback to empty set if section missing
    assert isinstance(data["skills"], list)
    # Education detected
    assert "master" in data["education"]
    assert data["years_experience"] == 2.0


def test_resume_extraction_empty_resume():
    text = ""
    extractor = ResumeExtractor(text)
    data = extractor.extract()

    assert data["skills"] == []
    assert data["education"] == []
    assert data["experience"] == []
    assert data["years_experience"] == 0.0


def test_resume_extraction_full_sections():
    text = """
    skills python java docker aws
    education bachelor mtech
    experience worked on projects for 5 years
    projects machine learning project, deep learning project
    """
    extractor = ResumeExtractor(text)
    data = extractor.extract()

    assert set(["python", "java", "docker", "aws"]).issubset(set(data["skills"]))
    assert "bachelor" in data["education"]
    assert "mtech" in data["education"]
    assert "experience" in data["experience"] or "project" in data["experience"]
    assert data["years_experience"] == 5.0
