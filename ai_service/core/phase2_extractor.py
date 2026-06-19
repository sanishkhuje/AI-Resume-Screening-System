# core/phase2_extractor.py

import re
from typing import Dict, List


class ResumeExtractor:
    def __init__(self, cleaned_text: str):
        self.text = cleaned_text
        self.sections = self._split_into_sections()

    # -------------------------
    # SECTION SPLITTER
    # -------------------------
    def _split_into_sections(self) -> Dict[str, str]:
        section_titles = [
            "skills", "education", "experience", "projects",
            "internship", "employment"
        ]

        sections = {title: "" for title in section_titles}

        current_section = None
        tokens = self.text.split()

        for word in tokens:
            if word in section_titles:
                current_section = word
                continue

            if current_section:
                sections[current_section] += word + " "

        return sections

    # -------------------------
    # SKILLS EXTRACTION
    # -------------------------
    def extract_skills(self) -> List[str]:
        skill_map = {
    # -------------------------
    # Programming Languages
    # -------------------------
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "go": ["golang", "go"],
    "rust": ["rust"],

    # -------------------------
    # Backend Frameworks
    # -------------------------
    "spring": ["spring"],
    "spring boot": ["spring boot", "springboot"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "nodejs": ["nodejs", "node js"],
    "express": ["express"],

    # -------------------------
    # Frontend Frameworks
    # -------------------------
    "react": ["react", "reactjs"],
    "angular": ["angular"],
    "vue": ["vue", "vuejs"],

    # -------------------------
    # Data & ML
    # -------------------------
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv"],
    "data analysis": ["data analysis", "data analytics"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit", "scikit-learn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],

    # -------------------------
    # Databases
    # -------------------------
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],

    # -------------------------
    # Cloud Platforms
    # -------------------------
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "cloud computing": ["cloud computing"],

    # -------------------------
    # DevOps & MLOps
    # -------------------------
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": ["ci/cd", "continuous integration"],
    "jenkins": ["jenkins"],
    "terraform": ["terraform"],
    "mlops": ["mlops"],

    # -------------------------
    # Version Control & Tools
    # -------------------------
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "linux": ["linux"],
    "bash": ["bash", "shell"],

    # -------------------------
    # APIs & Architecture
    # -------------------------
    "rest api": ["rest", "rest api", "restful"],
    "graphql": ["graphql"],
    "microservices": ["microservices"],
    "system design": ["system design"],

    # -------------------------
    # Security & Testing
    # -------------------------
    "unit testing": ["unit testing", "pytest", "junit"],
    "api security": ["api security"],
    "oauth": ["oauth", "oauth2"],
}


        text = self.sections.get("skills", self.text)

        found_skills = set()
        for skill, variants in skill_map.items():
            for v in variants:
                if v in text:
                    found_skills.add(skill)

        return sorted(found_skills)

    # -------------------------
    # EDUCATION EXTRACTION
    # -------------------------
    def extract_education(self) -> List[str]:
        education_patterns = [
            "bachelor", "master", "phd", "btech", "be",
            "mtech", "msc", "bsc", "degree", "diploma"
        ]

        text = self.sections.get("education", self.text)

        return sorted({edu for edu in education_patterns if edu in text})

    # -------------------------
    # EXPERIENCE EXTRACTION
    # -------------------------
    def extract_experience(self) -> List[str]:
        experience_signals = [
            "experience", "intern", "internship",
            "worked", "employment", "company",
            "project", "projects"
        ]

        text = (
            self.sections.get("experience", "") +
            self.sections.get("projects", "")
        )

        return sorted({kw for kw in experience_signals if kw in text})

    # -------------------------
    # YEARS OF EXPERIENCE
    # -------------------------
    def extract_years_of_experience(self) -> float:
        matches = re.findall(r"(\d+(\.\d+)?)\s+years?", self.text)

        if matches:
            years = [float(m[0]) for m in matches]
            return max(years)

        if "intern" in self.text:
            return 0.5

        return 0.0

    # -------------------------
    # MASTER EXTRACTOR
    # -------------------------
    def extract(self) -> Dict:
        return {
            "skills": self.extract_skills(),
            "education": self.extract_education(),
            "experience": self.extract_experience(),
            "years_experience": self.extract_years_of_experience(),
        }
