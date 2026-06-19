# core/phase5_mitigation.py

from typing import Dict


class BiasMitigator:
    """
    Phase 5: Bias Mitigation Layer (V1)

    Purpose:
    - Prevent extreme penalties
    - Normalize scoring behavior
    - Provide future extension hook
    """

    def __init__(self, score_result: Dict):
        self.score_result = score_result

    def mitigate(self) -> Dict:
        breakdown = self.score_result.get("breakdown", {})
        total_score = self.score_result.get("total_score", 0.0)

        # Guardrail: prevent negative or >100 scores
        total_score = max(0.0, min(100.0, total_score))

        # Guardrail: floor low but non-zero resumes
        if 0 < total_score < 20:
            total_score = 20.0

        return {
            "total_score": round(total_score, 2),
            "breakdown": breakdown
        }
