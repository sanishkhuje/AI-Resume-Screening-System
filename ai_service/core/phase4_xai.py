from typing import Dict, List
class ResumeExplainer:
    def __init__(
        self,
        score_output: Dict,
        resume_data: Dict,
        job_profile: Dict
    ):
        self.score_output = score_output
        self.resume_data = resume_data
        self.job_profile = job_profile

        self.explanations = {}
        self.positive_factors = []
        self.negative_factors = []

    # -------------------------
    # SKILLS EXPLANATION
    # -------------------------
    def explain_skills(self):
        required = set(self.job_profile.get("required_skills", []))
        found = set(self.resume_data.get("skills", []))

        if not required:
            self.explanations["skills"] = "No specific skill requirements defined."
            self.positive_factors.append("Skills not restricted by job profile")
            return

        matched = required & found
        missing = required - found

        self.explanations["skills"] = (
            f"Matched {len(matched)} out of {len(required)} required skills. "
            f"Matched: {', '.join(matched) if matched else 'None'}. "
            f"Missing: {', '.join(missing) if missing else 'None'}."
        )

        if matched:
            self.positive_factors.append(
                f"Relevant skills found: {', '.join(matched)}"
            )

        if missing:
            self.negative_factors.append(
                f"Missing required skills: {', '.join(missing)}"
            )

    # -------------------------
    # EDUCATION EXPLANATION
    # -------------------------
    def explain_education(self):
        min_edu = set(self.job_profile.get("min_education", []))
        candidate_edu = set(self.resume_data.get("education", []))

        if not min_edu:
            self.explanations["education"] = "No minimum education requirement specified."
            self.positive_factors.append("Education not restricted")
            return

        if min_edu & candidate_edu:
            self.explanations["education"] = (
                "Candidate meets the minimum education requirement."
            )
            self.positive_factors.append("Meets education requirement")
        else:
            self.explanations["education"] = (
                "Candidate does not meet the minimum education requirement."
            )
            self.negative_factors.append("Required education not found")

    # -------------------------
    # EXPERIENCE KEYWORDS
    # -------------------------
    def explain_experience(self):
        required_signals = set(
            self.job_profile.get("required_experience_signals", [])
        )
        found_signals = set(self.resume_data.get("experience", []))

        if not required_signals:
            self.explanations["experience"] = "No experience keyword constraints."
            self.positive_factors.append("Experience keywords not restricted")
            return

        matched = required_signals & found_signals

        if matched:
            self.explanations["experience"] = (
                f"Relevant experience indicators found: {', '.join(matched)}."
            )
            self.positive_factors.append(
                f"Experience indicators present: {', '.join(matched)}"
            )
        else:
            self.explanations["experience"] = (
                "No required experience indicators found."
            )
            self.negative_factors.append("Experience indicators missing")

    # -------------------------
    # YEARS OF EXPERIENCE
    # -------------------------
    def explain_years(self):
        min_years = self.job_profile.get("min_experience", 0)
        years_found = self.resume_data.get("years_experience", 0.0)

        if not min_years:
            self.explanations["years_experience"] = (
                "Years of experience not restricted."
            )
            self.positive_factors.append("Years of experience not restricted")
            return

        if years_found >= min_years:
            self.explanations["years_experience"] = (
                f"{years_found} years of experience meets the minimum requirement "
                f"of {min_years} years."
            )
            self.positive_factors.append("Sufficient years of experience")
        else:
            self.explanations["years_experience"] = (
                f"{years_found} years of experience is below the required "
                f"{min_years} years."
            )
            self.negative_factors.append("Insufficient years of experience")

    # -------------------------
    # MASTER EXPLAIN METHOD
    # -------------------------
    def explain(self) -> Dict:
        self.explain_skills()
        self.explain_education()
        self.explain_experience()
        self.explain_years()

        return {
            "total_score": self.score_output.get("total_score", 0.0),
            "breakdown": self.score_output.get("breakdown", {}),
            "explanations": self.explanations,
            "positive_factors": self.positive_factors,
            "negative_factors": self.negative_factors,
        }
