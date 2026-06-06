# core/phase1_gatekeeper.py

class Gatekeeper:
    def __init__(self, cleaned_text: str):
        self.text = cleaned_text

    def evaluate(self) -> dict:
        if not self.text or len(self.text.split()) < 50:
            return {
                "eligible": False,
                "reason": "Resume text too short or empty"
            }

        has_experience = any(
            kw in self.text
            for kw in ["experience", "intern", "worked", "employment", "project"]
        )

        has_education = any(
            kw in self.text
            for kw in ["bachelor", "master", "degree", "btech", "be", "education"]
        )

        has_skills_section = any(
            kw in self.text
            for kw in ["skills", "technologies", "expertise"]
        )

        if not (has_experience or has_education):
            return {
                "eligible": False,
                "reason": "No experience or education found"
            }

        if not has_skills_section:
            return {
                "eligible": False,
                "reason": "No skills section detected"
            }

        return {
            "eligible": True,
            "reason": "Passed basic resume validation"
        }
