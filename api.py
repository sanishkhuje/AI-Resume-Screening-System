from fastapi import FastAPI
from pydantic import BaseModel
from main import run_pipeline

app = FastAPI()

# -------------------------
# Request Schema
# -------------------------
class ResumeRequest(BaseModel):
    text: str


# -------------------------
# API Endpoint
# -------------------------
@app.post("/screen")
def screen_resume(request: ResumeRequest):
    result = run_pipeline(request.text, is_pdf=False)
    return result