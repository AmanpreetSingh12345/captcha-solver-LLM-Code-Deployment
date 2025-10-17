import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_SECRET = os.getenv("API_SECRET", "defaultSecret")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

class AttachmentModel(BaseModel):
    name: str
    url: str

class AppBuildRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: List[str]
    evaluation_url: str
    attachments: Optional[List[AttachmentModel]] = None

def generate_code(brief: str) -> str:
    prompt = (
        "Generate a minimal FastAPI Python app named 'captcha solver' that accepts a '?url=' parameter for an image URL, "
        "downloads and solves the captcha image at that URL, and returns the solved text in 15 seconds or less. "
        "If no URL is given, use the default attached sample image. "
        "Include code for all requirements, such as parsing the captcha and returning results as JSON. "
        "Use open-source libraries and explain how to run the app in comments."
    )
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    code = response.text
    return code

@app.post("/api/llm-build")
async def build_app(request: AppBuildRequest):
    if request.secret != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    code = generate_code(request.brief)
    return {
        "message": "App generated!",
        "brief": request.brief,
        "generated_code_preview": code[:500] + " ... [truncated]",
	"generated_code": code
    }
