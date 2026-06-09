import sys
from pprint import pprint

from utils.pdf_parser import PDFParser
from utils.text_cleaner import TextCleaner

from core.phase1_gatekeeper import Gatekeeper
from core.phase2_extractor import ResumeExtractor
from core.phase3_scorer import ResumeScorer
from core.phase4_xai import ResumeExplainer
from core.phase5_mitigation import BiasMitigator


# -------------------------------------------------
# Example Job Profile (later from DB / UI / API)
# -------------------------------------------------
JOB_PROFILE = {
    "required_skills": ["python", "ml", "docker", "aws"],
    "min_education": ["bachelor", "master"],
    "required_experience_signals": ["experience", "projects"],
    "min_experience": 3
}


def run_pipeline(resume_input: str, is_pdf: bool = False) -> dict:
    """
    Main orchestration pipeline for Talent-Logic-X
    """

    # -------------------------
    # Phase 0: Load & Clean
    # -------------------------
    if is_pdf:
        raw_text = PDFParser(resume_input).extract_text()
    else:
        raw_text = resume_input

    cleaned_text = TextCleaner.clean(raw_text)

    # -------------------------
    # Phase 1: Gatekeeper
    # -------------------------
    gatekeeper = Gatekeeper(cleaned_text)
    gate_result = gatekeeper.evaluate()

    if not gate_result["eligible"]:
        return {
            "status": "REJECTED",
            "reason": gate_result["reason"]
        }

    # -------------------------
    # Phase 2: Extraction
    # -------------------------
    extractor = ResumeExtractor(cleaned_text)
    extracted_data = extractor.extract()

    # -------------------------
    # Phase 3: Scoring
    # -------------------------
    scorer = ResumeScorer(extracted_data, JOB_PROFILE)
    score_result = scorer.score()

    # -------------------------
    # Phase 4: XAI
    # -------------------------
    explainer = ResumeExplainer(
        score_output=score_result,
        resume_data=extracted_data,
        job_profile=JOB_PROFILE
    )
    explanation = explainer.explain()

    # -------------------------
    # Phase 5: Bias Mitigation
    # -------------------------
    mitigator = BiasMitigator(score_result)
    final_score = mitigator.mitigate()

    return {
        "status": "ACCEPTED",
        "final_score": final_score["total_score"],
        "breakdown": final_score["breakdown"],
        "explanation": explanation
    }


# -------------------------------------------------
# CLI Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <resume_text_or_pdf_path>")
        sys.exit(1)

    input_data = sys.argv[1]
    is_pdf = input_data.lower().endswith(".pdf")

    result = run_pipeline(input_data, is_pdf=is_pdf)

    print("\n===== TALENT LOGIC X RESULT =====")
    pprint(result)
