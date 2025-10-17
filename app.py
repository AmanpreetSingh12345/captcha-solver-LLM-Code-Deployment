import base64
import io
import time
from typing import Optional

import easyocr
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Initialize the FastAPI app
app = FastAPI(
    title="Captcha Solver API",
    description="A minimal API to solve simple captchas from an image URL.",
    version="1.0.0",
)

# Initialize the EasyOCR reader (English language, CPU only)
print("Initializing EasyOCR reader... (This may take a moment on first run)")
reader = easyocr.Reader(['en'], gpu=False)
print("EasyOCR reader initialized successfully.")

# Default captcha image (Base64-encoded). Text is "2a58n".
DEFAULT_CAPTCHA_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAIwAAAA8CAYAAAAxti+YAAACrElEQVR4nO2dMW7VMBBG"
    "3xQpUqRNkC5B3SAL5A3wBngaZAsUKRIkixBlixQJ0iVoEyhSpEibIH+gQPgKx/LMN2OP"
    "XWOvZL0sS/w4v/Od3ZkdgGma/rFf0g/t7/f7c0wTJAnA9/s9WZZx/s8LAnj+/Xt5PF65"
    "XN4pijg+Pv758u1/gAC+vr52PB53Op0eDge3t7d5nhcEgSgKoihGuVweDAYODw/7/f4z"
    "QBHAdDqVZVkwGLS9vW1ZlpTL5VgsxmazGU3TTCYTrukSiUSMxyM/wDBN3+v1ymQybDYb"
    "m81mNptFUXQ6nZRKpWw2eyYP8K/9ko/HI4oiAEzTgiBwuVwwmUwhk0nJsozP57O+vo7n"
    "eZIk43Q6w8PDoV6vI5lMMJ/Ps1wuH48HrufSNE3TNDzPI5lMMJlMGI1GbDabTqfD8/zW"
    "1tYpP8A0TT+h/qMoiqIoysfjsVwuW5blcrkODg7gOA5FURAEWJblOA4AEARBmmZVVZIk"
    "QRCEYRhFUUxmc4/neTweB4PBW8fHxzDGIAjMZrN8Pk+WZfV6/bXz+bwzBH8BPM/jOA6C"
    "ICiKQqkU5XL5crmUZZlWq3U6nUqlUqvVyuVyKpUKz/POzs5kMglN0xhjPz8/pmmGIAhy"
    "uRzDMIQQrusymQzLsmEYpmmM4ziO4yRJruvSNE2SJMF1lWEYvu9pmqZpmsIYN00LgoBl"
    "WZqmvu+Pj4+zLAvDMCaTuSWEMMZYlvU5j4+P2WwWhmE4jkulUqvVKpVKzWbz9vamKArP"
    "83e+h9/vdzgcHMdxHMehUKjX61ut1nQ6nUqlGIYhCALbtmEYWJaFZVmWZRUKhTAMN5vN"
    "9fX14eHhaDS6e4/n+R3b/4AATtO8n58/P/6NcbwATtO8T0wmk/957P8CDAD78Bv+B/gN"
    "AAD8BfwGAAAA8C/gNwAAAPAa/AYAAADwGvwGAAAA8Br8BgAAAPAa/AYAAADwGvwGAAAA"
    "8Br8BgAAAPCa3wB5EgHE4TsvyAAAAABJRU5ErkJggg=="
)

@app.get("/solve")
async def solve_captcha(url: Optional[str] = None):
    """
    Solves a captcha from an image URL or a default sample image.
    - If 'url' is provided, it downloads the image.
    - If not, uses the embedded sample image.
    """
    start_time = time.time()
    image_bytes: bytes

    if url:
        # Download image from URL
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            image_bytes = response.content
            source_identifier = url
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=f"Failed to download image: {e}")
    else:
        # Use default embedded image
        image_bytes = base64.b64decode(DEFAULT_CAPTCHA_BASE64)
        source_identifier = "default_sample"

    try:
        # EasyOCR for reading text from image
        result = reader.readtext(image_bytes, detail=0)
        solution = "".join(result).replace(" ", "")
        if not solution:
            solution = "No text found"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

    end_time = time.time()
    processing_time_ms = round((end_time - start_time) * 1000)
    return JSONResponse(content={
        "source": source_identifier,
        "solution": solution,
        "processing_time_ms": processing_time_ms,
    })

@app.get("/")
def read_root():
    return {
        "message": "Captcha Solver API is running.",
        "usage": "Go to /solve or /solve?url=YOUR_IMAGE_URL"
    }
