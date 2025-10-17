# FastAPI Captcha Solver

A minimal FastAPI application for solving simple captchas using EasyOCR from an image URL or a default sample image.

## Features

- **API endpoint**: `/solve` — accepts `?url=...` to solve captchas from external images.
- **Default fallback**: Uses an embedded base64 image when no URL is provided.
- **OCR Engine**: Uses the EasyOCR library (PyTorch-based, open-source).
- **Minimal & fast**: Built with FastAPI for performance and clarity.

## Setup

### 1. Clone the repository

git clone https://github.com/AmanpreetSingh12345/captcha-solver-yourtaskid.git
cd captcha-solver-LLM-Code-Deployment

### 2. Install dependencies
python -m venv venv
source venv/bin/activate # Use venv\Scripts\activate on Windows
pip install fastapi uvicorn requests easyocr
sudo apt install tesseract-ocr # Required for EasyOCR

### 3. Run the server

uvicorn app:app --reload

## Usage

- **Default sample captcha:**
http://127.0.0.1:8000/solve

text

- **Captcha from image URL:**
http://127.0.0.1:8000/solve?url=https://i.imgur.com/pfin023.png

- Example curl:
curl "http://127.0.0.1:8000/solve?url=https://i.imgur.com/pfin023.png"

text 

## Code Structure

- `app.py` — Main FastAPI application
  - `/solve` — GET endpoint, accepts optional `url` parameter, returns JSON with solved captcha text.
  - Embedded base64 image used as fallback.
  - Uses EasyOCR for robust captcha recognition.

## License

MIT License — see LICENSE file for details.

## Contact

For any queries or feedback, reach out via [24f2008747@ds.study.iitm.ac.in].
