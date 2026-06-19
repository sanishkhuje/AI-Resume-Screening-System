# tests/test_gatekeeper.py

import pytest
from ai_service.core.phase1_gatekeeper import Gatekeeper


def test_gatekeeper_empty_text():
    gatekeeper = Gatekeeper("")
    result = gatekeeper.evaluate()
    assert result["eligible"] is False
    assert "Resume text too short" in result["reason"]


def test_gatekeeper_short_text_no_keywords():
    text = "hello world"
    gatekeeper = Gatekeeper(text)
    result = gatekeeper.evaluate()
    assert result["eligible"] is False
    assert "Resume text too short" in result["reason"] or "No experience or education" in result["reason"]


def test_gatekeeper_missing_skills_section():
    text = "bachelor degree worked in internship"
    gatekeeper = Gatekeeper(text)
    result = gatekeeper.evaluate()
    assert result["eligible"] is False
    assert "No skills section detected" in result["reason"]


def test_gatekeeper_valid_resume():
    text = """
    bachelor degree in computer science
    experience working on projects using python and ml
    skills python, machine learning, sql
    """
    gatekeeper = Gatekeeper(text)
    result = gatekeeper.evaluate()
    assert result["eligible"] is True
    assert "Passed basic resume validation" in result["reason"]
