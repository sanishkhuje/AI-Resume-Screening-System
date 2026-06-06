import re
class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        if not text or not text.strip():
            return ""

        # lowercase
        text = text.lower()

        # remove emails
        text = re.sub(r"\S+@\S+", " ", text)

        # remove phone numbers
        text = re.sub(r"\+?\d[\d\s\-]{8,}\d", " ", text)

        # remove special characters
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # normalize spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()
